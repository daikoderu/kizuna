from pathlib import Path

import click


@click.group()
def cli():
    pass


def register_command_names(commands_directory: Path):
    command_names = []

    # Get a list of the available commands.
    for file in commands_directory.iterdir():
        if not file.name.endswith('.py') or file.name.startswith('_'):
            continue
        command_names.append(file.name[:-3])
    command_names.sort()

    # Register them.
    for name in command_names:
        namespace = {}
        code_filename = commands_directory / f'{name}.py'
        with open(code_filename, 'r') as f:
            module = compile(f.read(), code_filename, 'exec')
            eval(module, namespace, namespace)
        command = namespace.get('command')
        if command is not None:
            cli.add_command(command, name)


def main():
    commands_directory = Path(__file__).parent / 'commands'
    register_command_names(commands_directory)
    cli()


if __name__ == '__main__':
    main()
