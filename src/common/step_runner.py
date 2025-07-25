import os
import subprocess
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class StepRunner(ABC):

    def __init__(
        self,
        step_path: str,
        step_name: str,
        logger,
        config: Dict[str, str | None],
        dry_run: bool = False,
    ):
        assert step_path is not None, "step path cannot be None"
        assert os.path.exists(step_path), f"step path ({self._step_path}) does not exit"
        self._step_path = step_path

        assert step_name is not None
        self._step_name = step_name

        assert config is not None
        self._config = config

        assert logger is not None
        self._logger = logger
        self._dry_run = dry_run

    @abstractmethod
    def run(self, target):
        raise NotImplementedError()


class SubprocessStepRunner(StepRunner):

    def run(self, target) -> bool:
        self._logger.debug(f"Processing {self._step_name} {target}...")
        subprocess_params = self._build_subprocess_params()

        if self._dry_run is False:
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

        self._logger.debug(f"STDOUT for {target} sequencer: {result_stdout}")
        if result.stderr:
            self._logger.warning(f"STDERR for {target} sequencer: {results_stderr}")
            return False
        return True

    def _build_subprocess_params(self):
        subprocess_params: List[Any] = ["python", self._step_path]
        subprocess_switches = []
        for switch, value in self._config.items():
            subprocess_switches.append(f"--{switch}")
            if value is not None:
                subprocess_switches.append(value)
        subprocess_params.append(subprocess_switches)
        return subprocess_params
