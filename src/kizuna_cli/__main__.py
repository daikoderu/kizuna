"""Module entrypoint for Kizuna CLI.

This allows running the CLI as a module, e.g. ``python -m kizuna_cli run``.
"""

from kizuna_cli.entrypoint import main


if __name__ == '__main__':
    main()
