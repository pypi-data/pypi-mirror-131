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
"""Base ZenML repository"""

import os
from typing import List, Optional

from git import InvalidGitRepositoryError  # type: ignore[attr-defined]

from zenml.core.constants import ZENML_DIR_NAME
from zenml.core.git_wrapper import GitWrapper
from zenml.core.local_service import LocalService
from zenml.exceptions import InitializationException
from zenml.io import fileio
from zenml.logger import get_logger
from zenml.post_execution.pipeline import PipelineView
from zenml.stacks.base_stack import BaseStack
from zenml.utils.analytics_utils import GET_PIPELINES, SET_STACK, track

logger = get_logger(__name__)


class Repository:
    """ZenML repository definition.

    Every ZenML project exists inside a ZenML repository.
    """

    def __init__(self, path: Optional[str] = None):
        """
        Construct reference to a ZenML repository.

        Args:
            path (str): Path to root of repository
        """
        if path is None:
            try:
                path = fileio.get_zenml_dir()
            except InitializationException:
                # If there isn't a zenml.config, use the cwd
                path = os.getcwd()

        if not fileio.is_dir(path):
            raise FileNotFoundError(f"{path} does not exist or is not a dir!")
        self.path = path
        self.service = LocalService()

        # Hook up git, path needs to have a git folder.
        try:
            self.git_wrapper = GitWrapper(self.path)
        except InvalidGitRepositoryError:
            # We only need to raise exception in the `init_repo`, not in the
            #  constructor here. This makes it more relaxed in remote
            #  orchestration scenarios. We might want to revisit this.
            self.git_wrapper = None  # type: ignore[assignment]

    @staticmethod
    def init_repo(
        repo_path: str = os.getcwd(),
        stack: Optional[BaseStack] = None,
    ) -> None:
        """
        Initializes a git repo with zenml.

        Args:
            repo_path (str): path to root of a git repo
            stack: Initial stack.

        Raises:
            InvalidGitRepositoryError: If repository is not a git repository.
            NoSuchPathError: If the repo_path does not exist.
        """
        # First check whether it already exists or not
        if fileio.is_zenml_dir(repo_path):
            raise AssertionError(f"{repo_path} is already initialized!")

        try:
            GitWrapper(repo_path)
        except InvalidGitRepositoryError:
            raise InitializationException(
                f"{repo_path} is not a valid git repository. Please initialize"
                f" the repository with `git init`."
            )

        # Create the base dir
        zen_dir = os.path.join(repo_path, ZENML_DIR_NAME)
        fileio.create_dir_recursive_if_not_exists(zen_dir)

        # Set up metadata and artifact store defaults
        artifact_dir = os.path.join(zen_dir, "local_store")
        metadata_dir = os.path.join(artifact_dir, "metadata.db")

        # Create stack if not specified
        if stack is None:
            from zenml.artifact_stores.local_artifact_store import (
                LocalArtifactStore,
            )
            from zenml.metadata.sqlite_metadata_wrapper import (
                SQLiteMetadataStore,
            )
            from zenml.orchestrators.local.local_orchestrator import (
                LocalOrchestrator,
            )

            service = LocalService()

            service.register_artifact_store(
                "local_artifact_store", LocalArtifactStore(path=artifact_dir)
            )

            service.register_metadata_store(
                "local_metadata_store", SQLiteMetadataStore(uri=metadata_dir)
            )

            service.register_orchestrator(
                "local_orchestrator", LocalOrchestrator()
            )

            service.register_stack(
                "local_stack",
                BaseStack(
                    metadata_store_name="local_metadata_store",
                    artifact_store_name="local_artifact_store",
                    orchestrator_name="local_orchestrator",
                ),
            )

            service.set_active_stack_key("local_stack")

    def get_git_wrapper(self) -> GitWrapper:
        """Returns the git wrapper for the repo."""
        return self.git_wrapper

    def get_service(self) -> LocalService:
        """Returns the active service. For now, always local."""
        return self.service

    @track(event=SET_STACK)
    def set_active_stack(self, stack_key: str) -> None:
        """Set the active stack for the repo. This change is local for the
        machine.

        Args:
            stack_key: Key of the stack to set active.
        """
        self.service.set_active_stack_key(stack_key)

    def get_active_stack_key(self) -> str:
        """Get the active stack key from global config.

        Returns:
            Currently active stacks key.
        """
        return self.service.get_active_stack_key()

    def get_active_stack(self) -> BaseStack:
        """Get the active stack from global config.

        Returns:
            Currently active stack.
        """
        return self.service.get_stack(self.get_active_stack_key())

    @track(event=GET_PIPELINES)
    def get_pipelines(
        self, stack_key: Optional[str] = None
    ) -> List[PipelineView]:
        """Returns a list of all pipelines.

        Args:
            stack_key: If specified, pipelines in the metadata store of the
                given stack are returned. Otherwise pipelines in the metadata
                store of the currently active stack are returned.
        """
        stack_key = stack_key or self.get_active_stack_key()
        metadata_store = self.service.get_stack(stack_key).metadata_store
        return metadata_store.get_pipelines()

    def get_pipeline(
        self, pipeline_name: str, stack_key: Optional[str] = None
    ) -> Optional[PipelineView]:
        """Returns a pipeline for the given name or `None` if it doesn't exist.

        Args:
            pipeline_name: Name of the pipeline.
            stack_key: If specified, pipelines in the metadata store of the
                given stack are returned. Otherwise pipelines in the metadata
                store of the currently active stack are returned.
        """
        stack_key = stack_key or self.get_active_stack_key()
        metadata_store = self.service.get_stack(stack_key).metadata_store
        return metadata_store.get_pipeline(pipeline_name)

    def clean(self) -> None:
        """Deletes associated metadata store, pipelines dir and artifacts"""
        raise NotImplementedError
