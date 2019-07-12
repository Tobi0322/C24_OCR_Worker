import cv2

from Preprocessing import PreprocessingStep

class Denoising(PreprocessingStep):
    name = "Denoising"
    def execute(self, image):
        return cv2.fastNlMeansDenoising(image, None, 50, 7, 21)
