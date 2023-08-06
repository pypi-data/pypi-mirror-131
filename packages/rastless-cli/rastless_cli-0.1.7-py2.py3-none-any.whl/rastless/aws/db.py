import boto3
from boto3.dynamodb.conditions import Key
from rastless.schemas.db import WqLayerModel, StepModel, ColorMap
from pydantic import parse_obj_as
from botocore.exceptions import ClientError
from typing import List


class Database:
    def __init__(self, table_name, resource=None):
        if not resource:
            resource = boto3.resource('dynamodb')  # only for testing

        self.table_name = table_name
        self.resource = resource
        self.table = self.resource.Table(table_name)

    def scan_table(self, pk_startswith, sk_startswith=None):
        filter_expression = Key("pk").begins_with(pk_startswith)
        if sk_startswith:
            filter_expression &= Key("sk").begins_with(sk_startswith)

        scan_kwargs = {
            "FilterExpression": filter_expression
        }

        items_list = []

        done = False
        start_key = None

        while not done:
            if start_key:
                scan_kwargs['ExclusiveStartKey'] = start_key
            response = self.table.scan(**scan_kwargs)
            if items := response.get("Items"):
                items_list.extend(items)
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None

        return items_list

    def list_layers(self):
        return self.scan_table("layer", "layer")

    def list_permissions(self):
        items = self.scan_table("permission")
        permissions = set([item["pk"] for item in items])
        return list(permissions)

    def add_permission_to_wq_layer(self, layer: WqLayerModel, permission: str):
        self.table.put_item(Item={"pk": f"permission#{permission}", "sk": f"layer#{layer.name}",
                                  **layer.dict(by_alias=True, exclude_unset=True, exclude={"layer_permissions"})})

    def delete_layer(self, layer_name: str):
        response = self.table.query(
            IndexName="gsi1",
            KeyConditionExpression=Key('sk').eq(f"layer#{layer_name}")
        )
        items = response.get("Items", [])

        with self.table.batch_writer() as writer:
            for item in items:
                writer.delete_item(
                    Key={"sk": item["sk"], "pk": item["pk"]}
                )

    def delete_permission(self, permission: str):
        response = self.table.query(
            KeyConditionExpression=Key('pk').eq(f"permission#{permission}")
        )
        items = response.get("Items", [])

        with self.table.batch_writer() as writer:
            for item in items:
                writer.delete_item(
                    Key={"pk": item["pk"], "sk": item["sk"]}
                )

    def delete_layer_from_layer_permission(self, layer_name: str, permission: str):
        self.table.delete_item(
            Item={"pk": f"permission#{permission}", "sk": f"layer#{layer_name}"}
        )

    def add_wq_layer(self, layer: WqLayerModel) -> bool:
        try:
            self.table.put_item(
                Item={
                    "pk": f"layer#{layer.name}",
                    "sk": f"layer#{layer.name}",
                    **layer.dict(by_alias=True, exclude_unset=True)
                },
                ConditionExpression="attribute_not_exists(pk) AND attribute_not_exists(sk)"
            )
            return True
        except ClientError:
            return False

    def get_layer_step(self, layer_name: str, step: str):
        response = self.table.get_item(Key={"pk": f"step#{step}", "sk": f"layer#{layer_name}"})
        return response.get("Items")

    def get_layer_steps(self, layer_name: str) -> List[StepModel]:
        response = self.table.query(
            IndexName="gsi1",
            KeyConditionExpression=Key("sk").eq(f"layer#{layer_name}") & Key("pk").begins_with("step")
        )
        return parse_obj_as(List[StepModel], response.get("Items", []))

    def add_layer_step(self, layer_name: str, layer_step: StepModel):
        try:
            self.table.put_item(
                Item={
                    "pk": f"step#{layer_step.datetime}",
                    "sk": f"layer#{layer_name}",
                    **layer_step.dict(by_alias=True, exclude_unset=True, exclude={"filename", "filedir"})
                },
                ConditionExpression="attribute_not_exists(pk) AND attribute_not_exists(sk)"
            )
            return True
        except ClientError:
            return False

    def get_layers(self, layer_names: set):
        response = self.resource.batch_get_item(
            RequestItems={
                self.table_name: {
                    "Keys": [{"pk": f"layer#{layer_name}", "sk": f"layer#{layer_name}"} for layer_name in layer_names]
                }
            }
        )

        return response["Responses"][self.table_name]

    def add_color_map(self, color_map: ColorMap):
        self.table.put_item(
            Item={
                "pk": f"colorMap#{color_map.name}",
                "sk": f"colorMap",
                **color_map.dict(by_alias=True, exclude_unset=True)
            }
        )

    def delete_color_map(self, name: str):
        self.table.delete_item(
            Key={"pk": f"colorMap#{name}", "sk": f"colorMap#{name}"}
        )


if __name__ == '__main__':
    db = Database("rastless")
    print(db.get_layers({"layer1", "layer2"}))
