import cv2
import os

from detector import ThresholdBlurDetector, MorphologyTransformDetector
from utils.loader import load_images, get_images_from_dir
from utils.display import display_rectangles, show_image, multi_plot
from utils.transform import deskew_lines, deskew_text
from utils.segment import segment_contours
from recognizer import TextRecognizer


def main():
    """
    Load images from a directory and process them to extract the license plate numbers
    """

    print('OpenCV version: %s' % cv2.__version__)

    # image_names = sorted(get_images_from_dir('images'))
    # image_names = ['images' + os.sep + '16.jpg']
    # image_names = ['images' + os.sep + '25.jpg']
    # image_names = ['images' + os.sep + '27.jpg']
    # image_names = ['images' + os.sep + '29.jpg']
    # image_names = ['images' + os.sep + '11.jpg']
    image_names = ['images' + os.sep + 'yy.jpg']

    images = load_images(image_names)
    for i, src in enumerate(images):
        detector = ThresholdBlurDetector(src, image_names[i])
        # detector = MorphologyTransformDetector(src, image_names[i])

        # plates[i] = (plate, rectangle_in_original_picture)
        plates = detector.find_rectangles()

        display_rectangles(src, [plates[i][1] for i in range(len(plates))])

        for plate, original_rectangle in plates:
            show_image(plate, resize=True)

            # Skew correction using lines detection
            # deskew_line = transform.deskew_lines(processing_plate)

            # Skew correction using contours
            img = deskew_text(plate)

            # Cut the picture letter by letter
            boxes = segment_contours(img)

            labels = []
            for box in boxes:
                # box_mod = image.hq2x_zoom(cv2.cvtColor(box, cv2.COLOR_GRAY2BGR))
                # box_mod = cv2.cvtColor(box, cv2.COLOR_GRAY2BGR)
                tr = TextRecognizer(box)
                text, conf = tr.find_text()
                text = text.strip()

                t2 = ""
                for idx in range(len(text)):
                    if ord(text[idx]) in range(128):
                        t2 += text[idx]
                labels.append(t2)

                print t2, conf
                # display.show_image(box_mod)
            multi_plot(boxes, labels, 1, len(boxes))

if __name__ == '__main__':
    main()