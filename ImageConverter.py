import cv2 as cv
from enum import Enum
from pdf2image import convert_from_path
import pytesseract
import os
import sys


from Utils import load_ocr_config
from Preprocessing import Binarization, Denoising, Deskewing
from Exceptions import NoValidPreprocessingStepError
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

class FileFormat(Enum):
    """ PDF is regular pdf format
        Image format checks for either .jpg or .png
    """
    PDF = ".pdf"
    IMAGE = "IMAGE"

class ImageConverter():
    def __init__(self, task_id, preprocessing=[Binarization(), Denoising()], input_format=FileFormat.PDF, show_processing_steps=False):
        ''' A class that converts an text image file to text.

        :param task_id: The id of the task at hand.
        :param preprocessing: The preprocessing pipeline as an array. Steps are defined in Preprocessing.py
        :param input_format: The input format for the image converter.
        :param show_processing_steps: If true, the intermediate preprocessing steps are shown.
        '''
        self._input_format = input_format
        self.preprocessing = preprocessing
        self.show_processing_steps = show_processing_steps

        # Load the ocr config
        source, destination = load_ocr_config()

        # Get the filename of the document
        self.file_name = "\\".join(str(task_id).split('/'))
        working_directory = os.getcwd()
        image_path = os.path.join(working_directory, source, self.file_name)
        self._image_path = image_path

        # Set the destination for the .txt to be saved to
        text_file_name = self.file_name.split('.')[0] + '.txt'
        self._destination_path = os.path.join(working_directory, destination, text_file_name)

        self._pdf_conversion_format = '.jpg'

    def _preprocess(self, image):
        for step in self.preprocessing:
            try:
                image = step.execute(image)
            except AttributeError:
                raise NoValidPreprocessingStepError
            if self.show_processing_steps:
                cv.imwrite("Preprocessingstep-" + step.name +".jpg", image)
        return image

    def _convert_to_image(self):
        print(self.file_name)
        print("Converting pdf to image.")
        images = []
        print(self.file_name)
        print(self._image_path)
        pages = convert_from_path(self._image_path, dpi=300, fmt='JPEG', use_cropbox=True)
        for page in pages:
            file_name = self._image_path.split('.')[0]
            page.save(file_name, 'JPEG')
            images.append(cv.imread(file_name, 0))
        print(images)
        return images

    def _get_image(self):
        img = cv.imread(self._image_path + '.jpg', 0)
        if img is not None:
            return img
        img = cv.imread(self._image_path + '.png', 0)
        if img is not None:
            return img
        else:
            raise FileNotFoundError
        
    def setImagePath(self, folder):
        working_directory = os.getcwd()
        source, destination = load_ocr_config()
        image_path = os.path.join(working_directory, source, folder, self.file_name)
        self._image_path = image_path


    def read_text_from_image(self):
        """ Reads the text from the image file configured.

        :return: The text as string.
        """
        print("Entering the converter")
        if self._input_format == FileFormat.PDF:
            images = self._convert_to_image()
        else:
            images = self._get_image()

        text = ""
        print(images)
        for image in images:
            print(image)
            config = ('-l deu --oem 1 --psm 1')
            image_processed = self._preprocess(image)
            byte_text = pytesseract.image_to_string(image_processed, config=config)
            text += byte_text
        
        # Remove the file used to convert the pdf
        conversion_file = os.path.join(os.getcwd(), self.file_name + self._pdf_conversion_format)
        if os.path.exists(conversion_file):
            os.remove(conversion_file)

        return text

    def save_to_txt(self, text):
        """ Write the string to a .txt file

        :param text: The text as string.
        """
        conversion_file = os.path.join(os.getcwd(), self.file_name + self._pdf_conversion_format)
        if os.path.exists(conversion_file):
            os.remove(conversion_file)

        with open(self._destination_path, "w", encoding='utf-8') as text_file:
            print('#'*30)
            print("Saving the file to text")
            print(text, file=text_file)

        return self._destination_path



if __name__ == "__main__":
    imageConverter = ImageConverter(10)
    text = imageConverter.read_text_from_image()
    imageConverter.save_to_txt(text)