from abc import ABC, abstractmethod

class Plugin(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def run(self) -> str:
        """
            # TODO not returning str... something else but can't be None... i mean it could be i guess haven't thought what I want out of it yet
            Expectation is that this will run the command and it will save to an output file
            Should save to the parent temp_dir made in the main runner
        """
        pass