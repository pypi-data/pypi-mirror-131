from typing import List

import cv2
from .image_segmenter import ColoredLabel
from .image_segmenter import ImageSegmenter
from .image_segmenter import ImageSegmenterOptions
import numpy as np
import os
from os_tflite_simple_cv import utils

_LEGEND_TEXT_COLOR = (0, 0, 255)  # red
_LEGEND_BACKGROUND_COLOR = (255, 255, 255)  # white
_LEGEND_FONT_SIZE = 1
_LEGEND_FONT_THICKNESS = 1
_LEGEND_ROW_SIZE = 20  # pixels
_LEGEND_RECT_SIZE = 16  # pixels
_LABEL_MARGIN = 10
_OVERLAY_ALPHA = 0.5
_PADDING_WIDTH_FOR_LEGEND = 150

class Segment():
    def __init__(self, model=None):
        if model is None:
            model = os.path.join(os.path.dirname(__file__), 'deeplabv3.tflite')
        options = ImageSegmenterOptions()
        self.segmenter = ImageSegmenter(model_path=model, options=options)
    def segment(self, image):
        segmentation_result = self.segmenter.segment(image)
        return segmentation_result
    def get_overlay_image(self, image, segmentation_result, display_mode='overlay'):
        if display_mode not in ['overlay', 'side-by-side']:
            display_mode = 'overlay'
        seg_map_img, found_colored_labels = utils.segmentation_map_to_image(segmentation_result)

        # Resize the segmentation mask to be the same shape as input image.
        seg_map_img = cv2.resize(
            seg_map_img,
            dsize=(image.shape[1], image.shape[0]),
            interpolation=cv2.INTER_NEAREST)

        # Visualize segmentation result on image.
        overlay = visualize(image, seg_map_img, display_mode, found_colored_labels)
        return overlay

def visualize(input_image: np.ndarray, segmentation_map_image: np.ndarray,
            display_mode: str, colored_labels: List[ColoredLabel]) -> np.ndarray:
    if display_mode == 'overlay':
        overlay = cv2.addWeighted(input_image, _OVERLAY_ALPHA,
                                segmentation_map_image, _OVERLAY_ALPHA, 0)
    else:
        overlay = cv2.hconcat([input_image, segmentation_map_image])

    # Initialize the origin coordinates of the label.
    legend_x = overlay.shape[1] + _LABEL_MARGIN
    legend_y = overlay.shape[0] // _LEGEND_ROW_SIZE + _LABEL_MARGIN

    # Expand the frame to show the label.
    overlay = cv2.copyMakeBorder(overlay, 0, 0, 0, _PADDING_WIDTH_FOR_LEGEND, cv2.BORDER_CONSTANT, None, _LEGEND_BACKGROUND_COLOR)

    # Show the label on right-side frame.
    for colored_label in colored_labels:
        rect_color = colored_label.color
        start_point = (legend_x, legend_y)
        end_point = (legend_x + _LEGEND_RECT_SIZE, legend_y + _LEGEND_RECT_SIZE)
        cv2.rectangle(overlay, start_point, end_point, rect_color, -_LEGEND_FONT_THICKNESS)

        label_location = legend_x + _LEGEND_RECT_SIZE + _LABEL_MARGIN, legend_y + _LABEL_MARGIN
        cv2.putText(overlay, colored_label.label, label_location,
                    cv2.FONT_HERSHEY_PLAIN, _LEGEND_FONT_SIZE, _LEGEND_TEXT_COLOR,
                    _LEGEND_FONT_THICKNESS)
        legend_y += (_LEGEND_RECT_SIZE + _LABEL_MARGIN)

    return overlay