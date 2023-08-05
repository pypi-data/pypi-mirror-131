#  Copyright (c) ZenML GmbH 2021. All Rights Reserved.
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
"""CLI for manipulating ZenML local and global config file."""

from typing import Optional

import click

from zenml.cli import utils as cli_utils
from zenml.cli.cli import cli
from zenml.core.repo import Repository
from zenml.stacks.base_stack import BaseStack


# Stacks
@cli.group()
def stack() -> None:
    """Stacks to define various environments."""


@stack.command("register", context_settings=dict(ignore_unknown_options=True))
@click.argument("stack_name", type=str)
@click.option("-m", "--metadata-store", type=str, required=True)
@click.option("-a", "--artifact-store", type=str, required=True)
@click.option("-o", "--orchestrator", type=str, required=True)
@click.option("-c", "--container_registry", type=str, required=False)
def register_stack(
    stack_name: str,
    metadata_store: str,
    artifact_store: str,
    orchestrator: str,
    container_registry: Optional[str] = None,
) -> None:
    """Register a stack."""

    service = Repository().get_service()
    stack = BaseStack(
        artifact_store_name=artifact_store,
        orchestrator_name=orchestrator,
        metadata_store_name=metadata_store,
        container_registry_name=container_registry,
    )
    service.register_stack(stack_name, stack)
    cli_utils.declare(f"Stack `{stack_name}` successfully registered!")


@stack.command("list")
def list_stacks() -> None:
    """List all available stacks from service."""
    service = Repository().get_service()
    cli_utils.title("Stacks:")
    # TODO [ENG-144]: once there is a common superclass for Stack/ArtifactStore etc.,
    #  remove the mypy ignore
    cli_utils.echo_component_list(service.stacks)  # type: ignore[arg-type]


@stack.command("delete")
@click.argument("stack_name", type=str)
def delete_stack(stack_name: str) -> None:
    """Delete a stack."""
    service = Repository().get_service()
    cli_utils.declare(f"Deleting stack: {stack_name}")
    service.delete_stack(stack_name)
    cli_utils.declare("Deleted!")


@stack.command("set")
@click.argument("stack_name", type=str)
def set_active_stack(stack_name: str) -> None:
    """Sets a stack active."""
    repo = Repository()
    repo.set_active_stack(stack_name)
    cli_utils.declare(f"Active stack: {stack_name}")


@stack.command("get")
def get_active_stack() -> None:
    """Gets the active stack."""
    repo = Repository()
    key = repo.get_active_stack_key()
    cli_utils.declare(f"Active stack: {key}")


@stack.command("up")
def up_stack() -> None:
    """Provisions resources for the stack."""
    active_stack = Repository().get_active_stack()
    orchestrator_name = active_stack.orchestrator_name

    cli_utils.declare(
        f"Bootstrapping resources for orchestrator: `{orchestrator_name}`. "
        f"This might take a few seconds..."
    )
    active_stack.orchestrator.up()
    cli_utils.declare(f"Orchestrator: `{orchestrator_name}` is up.")


@stack.command("down")
def down_stack() -> None:
    """Tears down resources for the stack."""
    active_stack = Repository().get_active_stack()
    orchestrator_name = active_stack.orchestrator_name

    cli_utils.declare(
        f"Tearing down resources for orchestrator: `{orchestrator_name}`."
    )
    active_stack.orchestrator.down()
    cli_utils.declare(
        f"Orchestrator: `{orchestrator_name}` resources are now torn down."
    )
