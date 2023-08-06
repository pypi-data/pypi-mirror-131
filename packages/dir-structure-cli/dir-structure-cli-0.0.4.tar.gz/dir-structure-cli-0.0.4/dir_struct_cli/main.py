import os
from posixpath import abspath, join

import click
from .helpers import skeleton_router

__version__ = "0.0.4"

TEMPLATES = list(
    [
        "flask",
        "django",
        "node-base",
        "node-cms",
        "react-base",
        "react-cms",
        "next-base",
        "next-cms",
    ]
)


@click.command(options_metavar="<options>")
@click.argument("app_name", type=click.STRING)
@click.option(
    "-t",
    "--template",
    default=list,
    type=click.Choice(TEMPLATES),
    multiple=True,
    help="""Supported frameworks for auto generate directory structure 
    """,
)
@click.option(
    "-p",
    "--path",
    help="Where to create your app. Defaults to the current directory.",
    type=str,
    default=None,
)
@click.version_option(__version__, "-v", "--version")
@click.help_option("-h", "--help")
def main(app_name, template, path):
    """
    Directory sturcture CLI DOCs
    """
    full_path = abspath(path or os.path.curdir)

    if not os.path.isdir(full_path):
        click.secho(f"'{full_path}' is no a valid directory path", fg="red")
        return False

    if not template:
        click.secho("--template was not provided", fg="red")
        exit(1)
    else:
        skeleton_router(template, app_name, full_path)

    app_path = join(full_path, app_name)

    # if env:
    #     create_env(app_path)


if __name__ == "__main__":
    main()
