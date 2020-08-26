import click

import re
import pprint

from terratalk.bitbucket_server import BitbucketServer

# https://bitbucket.org/tutorials/markdowndemo/issues/15/how-can-you-insert-comments-in-the#comment-22433250
# [comment]: # (terratalk: backoffice)

@click.group()
def cli():
    pass

@cli.command()
def comment():
    bs = BitbucketServer(base_url='https://stash.wimpmusic.com', username='gunter.grodotzki@tidal.com', password='MDE5NzEwNzcwMjgxOtGsHPIhHjGY54d6QxsQjVbRR4/L')
    pprint.pprint(bs.comments(project_key='TER', repository_slug='foundation-workspaces', pull_request_id=22))

if __name__ == '__main__':
    cli()
