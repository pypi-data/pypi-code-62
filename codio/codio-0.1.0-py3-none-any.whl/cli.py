# -*- coding: utf-8 -*-

import click


@click.group("codio")
@click.pass_context
def cli(*args, **kwargs):
    """You can now play code!"""
    pass
