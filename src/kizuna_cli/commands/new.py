import os
from pathlib import Path

import click

from kizuna.core.validation import validate_identifier


@click.command()
@click.argument('project-name')
@click.option(
    '-p', '--parent',
    type=click.Path(exists=False, file_okay=False, resolve_path=True, writable=True),
    help='Create the project at the specified directory.',
)
def command(project_name: str, parent: str | None):
    """Create a new Kizuna project with the specified name.
    """
    # Validate the ``project_name`` argument.
    try:
        project_name = validate_identifier(project_name)
    except ValueError as e:
        raise click.BadParameter(str(e), param_hint='project_name')

    # Validate the ``--parent`` option.
    if parent is None:
        parent = os.getcwd()
    project_path = Path(parent) / project_name
    if os.path.exists(project_path):
        raise click.BadOptionUsage(option_name='parent', message='File or directory already exists with that name.')

    # Create the project root.
    os.makedirs(project_path, exist_ok=True)

    # Show success message and return.
    click.echo(f'Created new project at directory "{project_path}".')
