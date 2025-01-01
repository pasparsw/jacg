import subprocess

from subprocess import CompletedProcess
from logging import getLogger

from test.integration.shell_command_execution_failed import ShellCommandExecutionFailed

LOGGER = getLogger('ShellCommandRunner')


class ShellCommandRunner:
    @staticmethod
    def execute(command: str) -> None:
        LOGGER.info(f'Running {command}')

        result: CompletedProcess = subprocess.run([command], shell=True)

        if result.returncode != 0:
            if result.stderr:
                LOGGER.error(f'{result.stderr.decode()}')
            if result.stdout:
                LOGGER.error(f'{result.stdout.decode()}')

            raise ShellCommandExecutionFailed(f'Failed to execute command "{command}"! Return code: '
                                               f'{result.returncode}')
