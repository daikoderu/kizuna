import os
from pathlib import Path

import click

from kizuna.management.exceptions import ManagementError, SettingsValidationError
from kizuna.management.setup import bootstrap


@click.command()
def command():
    """Run the project.
    """
    try:
        bootstrap(Path(os.getcwd()), standalone=False)
    except SettingsValidationError as e:
        raise click.ClickException(str(e) + '\n' + '\n'.join(
            f'- {setting}: {validation_error}' for setting, validation_error in e.errors.items()
        ))
    except ManagementError as e:
        raise click.ClickException(str(e))
