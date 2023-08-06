from typing import Optional

import click

from grid.cli import rich_click
from grid.cli import observables
from grid.cli.client import Grid
from grid.cli.types import ObservableType
from grid.cli.utilities import is_experiment
from grid.sdk.rest.exceptions import GridException


def _check_is_experiment(ctx, _param, value):
    """Callback that checks if a value is an experiment."""
    if not value:
        return value

    if is_experiment(value):
        raise click.BadArgumentUsage(f"Must pass a Run name, not Experiment: {value}")

    return value


@rich_click.command()
@rich_click.argument('run', type=str, nargs=1, required=False, callback=_check_is_experiment)
@click.option(
    '--global', 'is_global', type=bool, is_flag=True, help='Fetch status from all collaborators when flag is passed'
)
def status(run: Optional[str] = None, export: Optional[str] = None, is_global: Optional[bool] = False) -> None:
    """Checks the status of Runs, Experiments, and Sessions."""
    # TODO - move the logic to this function and remove observables after session is fully migrated
    try:
        observables.Run().get(is_global=is_global, run_name=run)
    except GridException as e:
        raise click.ClickException(str(e))
    # If we have a Run, then don't print the global
    # interactive nodes table.
    if not run:
        client = Grid()
        client.status(kind=ObservableType.INTERACTIVE, identifiers=[], export=export, is_global=is_global)
