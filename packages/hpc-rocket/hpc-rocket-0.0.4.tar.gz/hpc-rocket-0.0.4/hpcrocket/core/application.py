from typing import Any, Callable, Dict, Type

import hpcrocket.core.workflows as workflows
from hpcrocket.core.errors import get_error_message
from hpcrocket.core.executor import CommandExecutor
from hpcrocket.core.filesystem import FilesystemFactory
from hpcrocket.core.launchoptions import (LaunchOptions, MonitoringOptions,
                                          Options, StatusOptions, WatchOptions)
from hpcrocket.core.slurmcontroller import SlurmController
from hpcrocket.core.workflows.workflow import Workflow
from hpcrocket.ui import UI


class WorkflowFactory:

    def __init__(self, filesystem_factory: FilesystemFactory) -> None:
        self._fs_factory = filesystem_factory
        MonitoringWorkflowBuilder = Callable[[SlurmController, Any], Workflow]
        self._monitoring_workflows: Dict[Type[MonitoringOptions],
                                         MonitoringWorkflowBuilder] = {
            StatusOptions: workflows.statusworkflow,
            WatchOptions: workflows.watchworkflow
        }

    def __call__(self, controller: SlurmController, options: Options) -> Workflow:
        if isinstance(options, LaunchOptions):
            return workflows.launchworkflow(self._fs_factory, controller, options)

        option_type = type(options)
        monitoring_workflow_builder = self._monitoring_workflows[option_type]
        return monitoring_workflow_builder(controller, options)


class Application:

    def __init__(self, executor: CommandExecutor, filesystem_factory: FilesystemFactory, ui: UI) -> None:
        self._executor = executor
        self._workflow_factory = WorkflowFactory(filesystem_factory)
        self._ui = ui
        self._workflow: Workflow

    def run(self, options: Options) -> int:
        try:
            return self._run_workflow(options)
        except Exception as err:
            self._ui.error(get_error_message(err))
            return 1

    def _run_workflow(self, options: Options) -> int:
        with self._executor as executor:
            self._workflow = self._get_workflow(executor, options)
            success = self._workflow.run(self._ui)
            return 0 if success else 1

    def _get_workflow(self, executor: CommandExecutor, options: Options) -> Workflow:
        controller = SlurmController(executor)
        return self._workflow_factory(controller, options)

    def cancel(self) -> int:
        self._workflow.cancel(self._ui)
        return 130
