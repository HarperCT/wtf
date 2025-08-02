import abc

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