import click
import json

@click.command()
@click.argument('appname', envvar='APPNAME')
@click.argument('branch', envvar='BRANCH')
@click.argument('revision', envvar='REVISION')
@click.argument('version', envvar='VERSION')
def make_build_info(appname, branch, revision, version):
    buildinfo= {
        "appname": appname,
        "branch": branch,
        "revision": revision,
        "version": version
    }
    with open('build_info.json', 'w') as buildinfo_file:
        buildinfo_file.write(json.dumps(buildinfo, indent=4, sort_keys=True))
    click.echo("BuildInfo updated")