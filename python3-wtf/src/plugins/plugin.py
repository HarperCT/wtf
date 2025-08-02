import abc
import subprocess

class Plugin(abc.ABC):

    @abc.abstractmethod
    def is_applicable(self) -> bool:
        """
            Should run a check to see if this plugin can be used or not
            i.e. file {path} exists
        """
        pass


    @abc.abstractmethod
    def run(self) -> str:
        """
            # TODO not returning str... something else but can't be None... i mean it could be i guess haven't thought what I want out of it yet
            Expectation is that this will run the command and it will save to an output file
            Should save to the parent temp_dir made in the main runner
        """
        pass

    def subprocess_helper(self, command: list[str], timeout: float):
        try:
            proc = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True  # decode bytes to str automatically
            )

            try:
                # Wait for completion with timeout
                stdout, stderr = proc.communicate(timeout=timeout)
                return stdout, stderr, False

            except subprocess.TimeoutExpired:
                proc.kill()  # kill the process
                # Still collect whatever output is available
                stdout, stderr = proc.communicate()
                return stdout, stderr, True

        except Exception as e:
            return '', f'[Exception running command: {e}]', True
