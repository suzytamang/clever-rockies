import os
import subprocess
from abc import ABC, abstractmethod
from typing import Any, Generic, List
from common.parameters.sequencer_parameter import (
    SequencerParameters,
    StepMethod,
    StepParameters,
    TStepParameters,
)
from loguru import logger


class StepRunner(ABC, Generic[TStepParameters]):

    def __init__(
        self,
        step_name: str,
        config: TStepParameters,
        dry_run: bool = False,
    ):

        assert step_name is not None
        self._step_name = step_name

        assert config is not None
        self._config: TStepParameters = config

        self._dry_run = dry_run

    @abstractmethod
    def _run(self):
        raise NotImplementedError()

    def run(self):
        target = self._config.get("main_targets")
        logger.debug(f"Processing {self._step_name} {target}...")
        results_stdout, results_stderr = self._run()

        logger.debug(f"STDOUT for {target} sequencer: {results_stdout}")
        if results_stderr:
            logger.warning(f"STDERR for {target} sequencer: {results_stderr}")
            return False
        return True


class DirectStepRunner(StepRunner):

    def __init__(
        self,
        step_name: str,
        config: StepParameters,
        step: StepMethod,
        dry_run: bool = False,
    ):
        assert step is not None
        self._step: StepMethod = step
        super().__init__(step_name, config, dry_run)

    def _run(self):
        self._step(self._config)


class SubprocessStepRunner(StepRunner):

    def __init__(
        self,
        step_path: str,
        step_name: str,
        config: SequencerParameters,
        dry_run: bool = False,
    ):
        assert step_path is not None, "step path cannot be None"
        assert os.path.exists(step_path), f"step path ({self._step_path}) does not exit"
        self._step_path = step_path
        super().__init__(step_name, config, dry_run)

    def _run(self):

        subprocess_params = self._build_subprocess_params()

        if self._dry_run is not True:
            result = subprocess.run(
                *subprocess_params,
                capture_output=True,
                text=True,
            )

            result_stdout = result.stdout
            results_stderr = result.stderr
        else:
            import json

            result_stdout = json.dumps(subprocess_params, indent=4)
            results_stderr = ""

        return result_stdout, results_stderr

    def _build_subprocess_params(self):
        subprocess_params: List[Any] = ["python", self._step_path]
        subprocess_switches = []
        for switch, value in self._config.items():
            switch = "--" + switch.replace("_", "-")
            subprocess_switches.append(switch)
            if value is not None:
                subprocess_switches.append(value)
        subprocess_params.append(subprocess_switches)
        return subprocess_params
