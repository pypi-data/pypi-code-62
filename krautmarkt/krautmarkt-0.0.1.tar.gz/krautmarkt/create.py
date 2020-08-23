import os
from krautmarkt.extensions.source_s3 import SourceS3
from krautmarkt.extensions.save_hugo import SaveHugo
from loguru import logger
import click


def generate_datasets(remote, project, source, target):

    if source == "s3":
        model = SourceS3(remote)
        ms = model.fetch_metadata()
    else:
        raise ValueError(f"Source type {source} is not supported!")

    if target == "hugo":
        sh = SaveHugo(ms, project_path=project)
        sh.save_all()
    else:
        raise ValueError(f"Taget type {target} is not supported!")


@click.group(invoke_without_command=True)
@click.pass_context
def krautmarkt(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("Hello {}".format(os.environ.get("USER", "")))
        click.echo("Welcome to Krautmarkt, your Kraut management system.")
    else:
        click.echo(f"Loading Service: {ctx.invoked_subcommand}")


@krautmarkt.command()
@click.option("--remote", "-r", type=str, required=True)
@click.option(
    "--project", "-p", type=click.Path(), required=True, help="Directory of the project"
)
@click.option(
    "--source",
    "-s",
    type=str,
    required=False,
    default="s3",
    help="The type of the source, e.g., s3",
)
@click.option(
    "--target",
    "-t",
    type=str,
    required=False,
    default="hugo",
    help="The type of the target, e.g., hugo",
)
def create(remote, project, source, target):
    if not os.path.exists(project):
        raise Exception(f"path {project} does not exist!")

    if not isinstance(remote, str):
        raise TypeError(f"remote option has type {type(remote)} where str is required!")

    generate_datasets(remote, project, source, target)


if __name__ == "__main__":

    default_path_to_datasets = "krautmarkt-test/krautmarkt"
    generate_datasets(default_path_to_datasets, "cache", "s3", "hugo")

    pass
