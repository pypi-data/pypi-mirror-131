from .image_classifier import ImageClassifier
from .image_classifier import ImageClassifierOptions
import os

class Classify():
    def __init__(self, model=None, max_results=1):
        options = ImageClassifierOptions(
            max_results=max_results)
        if model is None:
            model = os.path.join(os.path.dirname(__file__), 'efficientnet_lite0.tflite')
        self.classifier = ImageClassifier(model, options)
    
    def classify(self, image):
        """
        image: np array (cv2.imread)
        """
        categories = self.classifier.classify(image)
        return categories[0].label, round(categories[0].score, 2)