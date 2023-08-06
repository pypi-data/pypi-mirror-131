import json
from typing import Union
from datetime import datetime
import os
import re
from rasterio.io import MemoryFile
from rio_cogeo.cogeo import cog_translate
from rastless.aws.db import Database
from rio_cogeo.profiles import cog_profiles
from rastless.main import RastlessCfg
from rastless.schemas.db import WqLayerModel, StepModel
from pydantic import parse_obj_as
from typing import List

product_is_32bit = {
    "abs": True,
    "aot": True,
    "cdm": True,
    "chl": True,
    "hab": True,
    "quc": False,
    "qut": False,
    "sdd": True,
    "sia": True,
    "soa": True,
    "rgb": False,
    "tur": True,
    "tsc": True,
    "sdb": True
}


class WqFilename:
    wq_naming_convention = '(?P<product>\w{3})_(?P<country>\w{2,3})-(?P<region>[a-zA-Z0-9]+)_?(\w+)?_EOMAP_' \
                           '(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})_' \
                           '(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})_' \
                           '(?P<sensor>\w+)_m(?P<resolution>\w{4})_?(?P<bit>\w{5})?.(?P<format>\w+$)'

    regex = re.compile(wq_naming_convention)

    def __init__(self, filename):
        self.match = self.regex.match(filename)

    def check_name_condition(self, layer_entry: WqLayerModel) -> bool:
        bit = "32bit" if product_is_32bit[layer_entry.product] else None
        name_conditions = {"product": layer_entry.product.upper(), "country": layer_entry.country,
                           "region": layer_entry.region, "format": "tif", "bit": bit}
        if self.match:
            return all([self.match.group(key) == value for key, value in name_conditions.items()])

        return False

    @property
    def sensor(self):
        return self.match.group("sensor")

    @property
    def resolution(self):
        return int(self.match.group("resolution"))

    @property
    def iso_datetime(self):
        return datetime(int(self.match.group("year")), int(self.match.group("month")), int(self.match.group("day")),
                        int(self.match.group("hour")), int(self.match.group("minute")),
                        int(self.match.group("second"))).isoformat()


def read_layer_json(filepath: str) -> List[WqLayerModel]:
    with open(filepath) as fobj:
        data = json.load(fobj)

    return parse_obj_as(List[WqLayerModel], data)


def get_layer_steps(file_path: Union[str, tuple], layer_entry: WqLayerModel) -> list[StepModel]:
    if isinstance(file_path, str):
        file_path = (file_path,)
    relevant_files = []

    for path in file_path:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                wq_filename = WqFilename(filename)
                if wq_filename.check_name_condition(layer_entry):
                    relevant_files.append(StepModel(
                        datetime=wq_filename.iso_datetime,
                        resolution=wq_filename.resolution,
                        sensor=wq_filename.sensor,
                        filedir=dirpath,
                        filename=filename
                    ))

    return relevant_files


def layer_step_not_exists(db: Database, layer_name: str, step: StepModel) -> bool:
    if db.get_layer_step(layer_name, step.datetime):
        return False

    return True


def create_upload_cog(cfg: RastlessCfg, layer_step: StepModel, layer_entry: WqLayerModel) -> None:
    filepath = os.path.join(layer_step.filedir, layer_step.filename)
    s3_filepath = os.path.join(layer_entry.s3_file_dir, layer_step.filename)

    dst_profile = cog_profiles.get("jpeg") if layer_entry.product == "RGB" else cog_profiles.get("deflate")

    with MemoryFile() as mem_dst:
        cog_translate(filepath, mem_dst.name, dst_profile, in_memory=True, quiet=True, web_optimized=True)
        cfg.s3_bucket.s3_client.upload_fileobj(mem_dst, cfg.s3_bucket_name, s3_filepath)


def create_wq_s3_filepath(s3_bucket: str, layer: WqLayerModel, step: StepModel):
    return f"s3://{s3_bucket}/{layer.s3_file_dir}{step.filename}"
