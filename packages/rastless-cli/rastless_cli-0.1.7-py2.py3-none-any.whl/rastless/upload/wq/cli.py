import time

import click
from rastless.main import RastlessCfg
from rastless.upload.wq import utils


@click.command()
@click.argument('search_path', type=click.Path(exists=True), nargs=-1)
@click.option("-o", "--overwrite-layers", is_flag=True, help="Set flag if you want to override existing layers")
@click.option("-j", "--json", type=click.Path(exists=True),
              help="Define parameters via json file")
@click.pass_obj
def upload_wq(cfg: RastlessCfg, search_path, overwrite_layers, json):
    layer_entries = utils.read_layer_json(json)

    for layer_entry in layer_entries:
        created = cfg.db.add_wq_layer(layer_entry)

        for permission in layer_entry.layer_permissions:
            cfg.db.add_permission_to_wq_layer(layer_entry, permission)

        if not created:
            click.echo(f"Layer {layer_entry.name} already in database. Layer info not updated.")

        layer_steps = utils.get_layer_steps(search_path, layer_entry)

        if not overwrite_layers:
            layer_steps = list(
                filter(lambda step: utils.layer_step_not_exists(cfg.db, layer_entry.name, step), layer_steps))

        if len(layer_steps) > 0:
            with click.progressbar(layer_steps,
                                   label=f"Upload layer {layer_entry.name} as Cloud Optimized Geotiff") as bar:
                for layer_step in bar:
                    layer_step.cog_filepath = utils.create_wq_s3_filepath(cfg.s3_bucket_name, layer_entry, layer_step)
                    utils.create_upload_cog(cfg, layer_step, layer_entry)
                    cfg.db.add_layer_step(layer_entry.name, layer_step)

        else:
            click.echo(f"No steps were uploaded for {layer_entry.name}")

    click.echo("Done!")
