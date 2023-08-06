""" command line of nob visualizee"""

import click
import nobvisual as nobv


@click.group()
def main_cli():
    """---------------    NOB VISUAL  --------------------

You are now using the Command line interface of Nob Visual
a Python3 helper to explore Nested Objects, created at CERFACS (https://cerfacs.fr).

This package is mean to be used as a dependency of other packages,
to provide a tkinker canvas rendering the nested structure of nesteds objects.

This is a python package currently installed in your python environement.
"""
    pass


@click.command()
@click.option('--max-recursion', '-l', type=int, default=3)
@click.option('--debug', is_flag=True, hidden=True)
def tree(max_recursion, debug):
    """Show current wkdir visually.
    """
    nobv.visual_tree(max_recursion=max_recursion,
                     start_mainloop=not debug)


main_cli.add_command(tree)


@click.command()
@click.argument("filename", nargs=1)
@click.option('--debug', is_flag=True, hidden=True)
def treefile(filename, debug):
    """Show the content of a serialization file.

    supports JSON, YAML, NML
    """
    nobv.visual_treefile(filename, start_mainloop=not debug)


main_cli.add_command(treefile)


@click.command()
@click.argument("file_left", nargs=1)
@click.argument("file_right", nargs=1)
@click.option('--debug', is_flag=True, hidden=True)
def cmpfile(file_left, file_right, debug):
    """Compare the content of two serialization files.

    supports JSON, YAML, NML
    """
    nobv.visual_comparefile(file_left, file_right,
                            start_mainloop=not debug)


main_cli.add_command(cmpfile)
