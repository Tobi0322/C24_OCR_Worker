import cv2

from Preprocessing import PreprocessingStep

class Binarization(PreprocessingStep):
    name = "Binarization"
    """ Binarization of the image passed to the execute method.
    """
    def execute(self, image):
        _, binary_image = cv2.threshold(image, 177, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary_image
