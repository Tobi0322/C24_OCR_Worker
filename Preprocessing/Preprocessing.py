from abc import ABC, abstractmethod

class PreprocessingStep(ABC):
    """ Defines the layout of a preprocessing step.
    """
    name = "Preprocessing Step"
    @abstractmethod
    def execute(self, image):
        """ Method that executes the preprocessing step. Override in subclasses.

        :param image: The image that is supposed to be processed.
        :return: The processed image.
        """
        pass

