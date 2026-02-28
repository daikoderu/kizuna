import datetime
import os
from pathlib import Path

import PyInstaller.__main__
import click

from kizuna.management.exceptions import SettingsValidationError, ManagementError
from kizuna.management.setup import initialize

LAUNCH_TEMPLATE = """#!/usr/bin/env python
from pathlib import Path

from kizuna.management.setup import bootstrap


if __name__ == '__main__':
    bootstrap(Path(__file__).parent, standalone=True)
"""


@click.command()
def command():
    """Generate a stand-alone executable.
    """
    # Initialize the project as if we are not in standalone mode, to ensure the configuration is OK.
    base_directory = Path(os.getcwd())
    try:
        initialize(base_directory, standalone=False)
    except SettingsValidationError as e:
        raise click.ClickException(str(e) + '\n' + '\n'.join(
            f'- {setting}: {validation_error}' for setting, validation_error in e.errors.items()
        ))
    except ManagementError as e:
        raise click.ClickException(str(e))

    # Create a temporary file to write the launch script.
    launch_file = base_directory / 'bundled_launch.py'
    with open(launch_file, 'w+') as fp:
        fp.write(LAUNCH_TEMPLATE)

    # Create output directory.
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    build_directory = base_directory / 'builds' / timestamp
    work_files_directory = build_directory / 'workfiles'
    os.makedirs(build_directory, exist_ok=True)
    os.makedirs(work_files_directory, exist_ok=True)

    try:
        # Launch PyInstaller.
        project_name = base_directory.name
        PyInstaller.__main__.run([
            str(launch_file), '--onefile', '--windowed',
            '-n', project_name,
            '-p', str(base_directory),
            '--add-data', 'assets:assets',
            '--collect-submodules', 'src',
            '--hidden-import', 'settings',
            '--distpath', str(build_directory),
            '--workpath', str(work_files_directory),
        ])
    finally:
        # Clean up.
        os.remove(launch_file)
