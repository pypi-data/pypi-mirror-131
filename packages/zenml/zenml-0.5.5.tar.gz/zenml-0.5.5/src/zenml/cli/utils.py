#  Copyright (c) ZenML GmbH 2020. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
import datetime
import functools
import subprocess
import sys
from datetime import timedelta
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    TypeVar,
    cast,
)

import click
from dateutil import tz
from tabulate import tabulate

from zenml.logger import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from zenml.core.base_component import BaseComponent


def title(text: str) -> None:
    """Echo a title formatted string on the CLI.

    Args:
      text: Input text string.
    """
    click.echo(click.style(text.upper(), fg="cyan", bold=True, underline=True))


def confirmation(text: str, *args: Any, **kwargs: Any) -> bool:
    """Echo a confirmation string on the CLI.

    Args:
      text: Input text string.
      *args: Args to be passed to click.confirm().
      **kwargs: Kwargs to be passed to click.confirm().

    Returns:
        Boolean based on user response.
    """
    return click.confirm(click.style(text, fg="yellow"), *args, **kwargs)


def question(text: str, *args: Any, **kwargs: Any) -> Any:
    """Echo a question string on the CLI.

    Args:
      text: Input text string.
      *args: Args to be passed to click.prompt().
      **kwargs: Kwargs to be passed to click.prompt().

    Returns:
        The answer to the question of any type, usually string.
    """
    return click.prompt(text=text, *args, **kwargs)  # type: ignore[misc]


def declare(text: str) -> None:
    """Echo a declaration on the CLI.

    Args:
      text: Input text string.
    """
    click.echo(click.style(text, fg="green"))


def error(text: str) -> None:
    """Echo an error string on the CLI.

    Args:
      text: Input text string.

    Raises:
        click.ClickException when called.
    """
    raise click.ClickException(message=click.style(text, fg="red", bold=True))


def warning(text: str) -> None:
    """Echo a warning string on the CLI.

    Args:
      text: Input text string.
    """
    click.echo(click.style(text, fg="yellow", bold=True))


def pretty_print(obj: Any) -> None:
    """Pretty print an object on the CLI.

    Args:
      obj: Any object with a __str__ method defined.
    """
    click.echo(str(obj))


def echo_component_list(component_list: Mapping[str, "BaseComponent"]) -> None:
    """Echoes a list of components in a pretty style."""
    list_of_dicts = []
    for key, c in component_list.items():
        # TODO [ENG-143]: This will break if component has element called `key`
        data = {"key": key}
        data.update(c.dict(exclude={"_superfluous_options"}))
        list_of_dicts.append(data)
    click.echo(tabulate(list_of_dicts, headers="keys"))


def format_date(
    dt: datetime.datetime, format: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """Format a date into a string.

    Args:
      dt: Datetime object to be formatted.
      format: The format in string you want the datetime formatted to.

    Returns:
        Formatted string according to specification.
    """
    if dt is None:
        return ""
    # make sure this is UTC
    dt = dt.replace(tzinfo=tz.tzutc())

    if sys.platform != "win32":
        # On non-windows get local time zone.
        local_zone = tz.tzlocal()
        dt = dt.astimezone(local_zone)
    else:
        logger.warning("On Windows, all times are displayed in UTC timezone.")

    return dt.strftime(format)


def format_timedelta(td: timedelta) -> str:
    """Format a timedelta into a string.

    Args:
      td: datetime.timedelta object to be formatted.

    Returns:
        Formatted string according to specification.
    """
    if td is None:
        return ""
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))


def parse_unknown_options(args: List[str]) -> Dict[str, Any]:
    """Parse unknown options from the CLI.

    Args:
      args: A list of strings from the CLI.

    Returns:
        Dict of parsed args.
    """
    warning_message = (
        "Please provide args with a proper "
        "identifier as the key and the following structure: "
        '--custom_argument="value"'
    )

    assert all(a.startswith("--") for a in args), warning_message
    assert all(len(a.split("=")) == 2 for a in args), warning_message

    p_args = [a.lstrip("--").split("=") for a in args]

    assert all(k.isidentifier() for k, _ in p_args), warning_message

    r_args = {k: v for k, v in p_args}
    assert len(p_args) == len(r_args), "Replicated arguments!"

    return r_args


F = TypeVar("F", bound=Callable[..., Any])


def activate_integrations(func: F) -> F:
    """Decorator that activates all ZenML integrations."""

    @functools.wraps(func)
    def _wrapper(*args: Any, **kwargs: Any) -> Any:
        """Inner decorator function"""
        from zenml.integrations.registry import integration_registry

        integration_registry.activate_integrations()
        return func(*args, **kwargs)

    return cast(F, _wrapper)


def install_package(package: str) -> None:
    """Installs pypi package into the current environment with pip"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def uninstall_package(package: str) -> None:
    """Uninstalls pypi package from the current environment with pip"""
    subprocess.check_call(
        [sys.executable, "-m", "pip", "uninstall", "-y", package]
    )
