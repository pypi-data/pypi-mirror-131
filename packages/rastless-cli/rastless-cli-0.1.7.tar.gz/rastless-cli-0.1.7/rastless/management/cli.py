import click
from rastless.main import RastlessCfg
from rastless.aws.s3 import delete_layer_step
from pydantic import parse_obj_as
from rastless.schemas.db import WqLayerModel
from typing import List
import os
from . import utils


@click.command()
@click.pass_obj
def list_layers(cfg: RastlessCfg):
    """List all layers."""
    layers = cfg.db.list_layers()
    click.echo_via_pager(utils.generate_layer_output(layers))


@click.command()
@click.pass_obj
def list_permissions(cfg: RastlessCfg):
    """List all roles."""
    roles = cfg.db.list_permissions()
    click.echo_via_pager(utils.generate_role_output(roles))


@click.command()
@click.option('-r', '--permission', help='Role e.g role#<client>:<client_role>, user#<username>', required=True,
              type=str)
@click.option('-l', '--layer', help='Layer name e.g wq_xylem_us_newyork_rgb', required=True, type=str, multiple=True)
@click.pass_obj
def add_permission_to_layers(cfg: RastlessCfg, permission, layer):
    """Add a role to one or multiple layers."""
    layers = set(layer)
    layer_items = cfg.db.get_layers(layers)
    layer_models = parse_obj_as(List[WqLayerModel], layer_items)

    for layer in layer_models:
        cfg.db.add_permission_to_wq_layer(layer, permission)
    click.echo("Role was successfully added to layers")


@click.command()
@click.option('-l', '--layer', help='Layer name e.g wq_xylem_us_newyork_rgb', required=True, type=str, multiple=True)
@click.pass_obj
def delete_layers(cfg: RastlessCfg, layer):
    """Delete one or multiple layers."""
    layers = set(layer)
    for layer_name in layers:
        layer_steps = cfg.db.get_layer_steps(layer_name)
        for layer_step in layer_steps:
            delete_layer_step(cfg.s3_bucket, layer_step)

        cfg.db.delete_layer(layer_name)

    click.echo("Layers were successfully removed")


@click.command()
@click.option('-p', '--permission', help='Permission name e.g role#<client>:<client_role>, user#<username>',
              required=True, type=str, multiple=True)
@click.pass_obj
def delete_permissions(cfg: RastlessCfg, permission):
    """Delete one or multiple permissions."""
    permissions = set(permission)

    for permission in permissions:
        cfg.db.delete_permission(permission)

    click.echo("Roles were successfully removed")


@click.command()
@click.argument('sld_file', type=click.Path(exists=True))
@click.option("-n", "--name", help="Name the colormap, otherwise take the filename")
@click.pass_obj
def add_colormap(cfg: RastlessCfg, sld_file, name):
    """Add a SLD file"""
    if not name:
        name = os.path.basename(sld_file.split(".")[0])
    try:
        color_map = utils.create_colormap(name, sld_file)
        cfg.db.add_color_map(color_map)
    except Exception as e:
        click.echo(f"SLD File could not be converted. Reason: {e}")


@click.command()
@click.option("-n", "--name", help="Name the colormap, otherwise take the filename", required=True)
@click.pass_obj
def delete_colormap(cfg: RastlessCfg, name):
    """Remove a SLD file"""
    cfg.db.delete_color_map(name)
