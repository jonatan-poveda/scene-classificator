from __future__ import print_function

import os

import cv2
import numpy as np
from typing import List, Type

from source import DATA_PATH


class BaseFeatureExtractor(object):
    def extract_from(self, train_images, train_labels=['no_label']):
        """ Compute descriptors given a list of images and labels """
        # type: (List, List) -> Type[NotImplementedError]
        return NotImplementedError

    def _compute(self, image):
        """ Compute an image descriptor """
        # type: (np.array) -> Type[NotImplementedError]
        return NotImplementedError


class SIFT(BaseFeatureExtractor):
    def __init__(self, number_of_features):
        # type: (int) -> None
        # FIXME: remove number_of_features if they are not explicity needed
        self.number_of_features = number_of_features
        self.detector = cv2.SIFT(nfeatures=self.number_of_features)

    def _compute(self, image):
        # type: (np.array) -> List
        """ Extract descriptor from an image """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Do not mind of descriptor key-points
        _, descriptors = self.detector.detectAndCompute(gray, None)
        return descriptors

    def extract_from(self, train_images, train_labels=['no_label']):
        # type: (List, List) -> (np.array, np.array)
        """ Compute descriptors using SIFT

        Read the just 30 train images per class.
        Extract SIFT keypoints and descriptors.
        Store descriptors in a python list of numpy arrays.

        :param train_images: list of images
        :param train_labels: list of labels of the given images
        :return: descriptors and labels
        """
        train_descriptors = []
        train_label_per_descriptor = []

        for filename, train_label in zip(train_images, train_labels):
            filename_path = os.path.join(DATA_PATH, filename)
            if train_label_per_descriptor.count(train_label) < 30:
                print('Reading image {}'.format(os.path.basename(filename)),
                      end=' ')
                image = cv2.imread(filename_path)
                descriptor = self._compute(image)
                train_descriptors.append(descriptor)
                train_label_per_descriptor.append(train_label)
                print('{} extracted keypoints and descriptors'.format(
                    len(descriptor)))

        # Transform everything to numpy arrays

        descriptors = train_descriptors[0]
        labels = np.array(
            [train_label_per_descriptor[0]] * train_descriptors[0].shape[0])

        for i in range(1, len(train_descriptors)):
            descriptors = np.vstack((descriptors, train_descriptors[i]))
            labels = np.hstack((labels, np.array(
                [train_label_per_descriptor[i]] * train_descriptors[i].shape[
                    0])))

        return descriptors, labels
