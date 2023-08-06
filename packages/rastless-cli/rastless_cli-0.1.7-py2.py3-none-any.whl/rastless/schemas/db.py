from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime as dt


def camel_case(string: str) -> str:
    return ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(string.split('_')))


class LayerModel(BaseModel):
    name: str
    title: str
    cmap: Optional[str]
    bands: Optional[dict]
    layer_permissions: set = None
    background_layer: str = None
    product_unit: str = None

    class Config:
        alias_generator = camel_case


class WqLayerModel(LayerModel):
    product: str
    client: str
    country: str
    region: str

    @property
    def name(self):
        return f"{self.client}_{self.country}_{self.region}_{self.product}"

    @property
    def s3_file_dir(self):
        return f"{self.client}/{self.country}/{self.region}/{self.product}/"


class StepModel(BaseModel):
    datetime: str
    resolution: int
    sensor: str
    filename: str = None
    filedir: str = None
    cog_filepath: str = None


class LayerPermissionModel(BaseModel):
    layers: set


class ColorMap(BaseModel):
    name: str
    levels: List[Decimal]
    colors: List[List[Decimal]]
