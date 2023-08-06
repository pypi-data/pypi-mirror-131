import click
from rastless.management import cli as general_cli
from rastless.aws import cli as aws_cli
from rastless.main import RastlessCfg
from rastless.upload.wq import cli as wq_cli


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj = RastlessCfg(debug)


# General Commands
cli.add_command(general_cli.list_layers)
cli.add_command(general_cli.list_permissions)
cli.add_command(general_cli.add_permission_to_layers)
cli.add_command(general_cli.delete_layers)
cli.add_command(general_cli.delete_permissions)
cli.add_command(general_cli.add_colormap)
cli.add_command(general_cli.delete_colormap)

# Connection Checks
cli.add_command(aws_cli.check_aws_connection)

# Upload
cli.add_command(wq_cli.upload_wq)


if __name__ == '__main__':
    cli()