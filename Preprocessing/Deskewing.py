import cv2
import math
import numpy as np

from Preprocessing import PreprocessingStep

class Deskewing(PreprocessingStep):
    name = "Deskewing"

    def execute(self, image):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, 30, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        image = cv2.resize(result, None, fx=10, fy=10, interpolation= cv2.INTER_CUBIC)
        cv2.imwrite("rotatedImage.jpg", image)

        img_edges = cv2.Canny(image, 100, 100, apertureSize=3)
        lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)

        angles = []

        for x1, y1, x2, y2 in lines[0]:
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 3)
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
            angles.append(angle)

        median_angle = np.median(angles)
        #img_rotated = ndimage.rotate(img_before, median_angle)
        print('_'*30)
        print("Angle is {}".format(median_angle))
        #cv2.imwrite('rotated.jpg', img_rotated)
        return image
