import click
from rastless.main import RastlessCfg
from rastless.aws import aws_connection


@click.command()
@click.pass_obj
def check_aws_connection(cfg: RastlessCfg):
    """Check if cli can connect to aws"""
    has_bucket_access, bucket_error = aws_connection.check_bucket_connection(cfg.s3_bucket_name)
    has_db_access, db_error = aws_connection.check_dynamodb_table_connection(cfg.db_table_name)

    if all([has_bucket_access, has_db_access]):
        click.echo("You have access to aws resources!")
    else:
        if not has_db_access:
            click.echo(f"ERROR: {db_error}")
        if not has_bucket_access:
            click.echo(f"ERROR: {bucket_error}")
