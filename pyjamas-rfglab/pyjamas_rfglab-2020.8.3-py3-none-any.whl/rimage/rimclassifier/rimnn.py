"""
    PyJAMAS is Just A More Awesome Siesta
    Copyright (C) 2018  Rodrigo Fernandez-Gonzalez (rodrigo.fernandez.gonzalez@utoronto.ca)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from typing import List, Tuple, Callable

import keras.layers as kl
import keras.models as km
import numpy

from pyjamas.rimage.rimclassifier.rimclassifier import rimclassifier
from pyjamas.rimage.rimutils import rimutils
import pyjamas.rimage.rimclassifier.nn.cnn as cnn


class DeepCNN_4Conv2D(rimclassifier):
    CONV_FILTER_NUMBER: int = 32
    FULLY_CONNECTED_NEURON_NUMBER: int = 500

    CONV_FILTER_SIZE: List[int] = [5, 5]
    ACTIVATION_FN: Callable = cnn.tanh
    POOL_SIZE: List[int] = [2, 2]
    OUTPUT_CLASSES: int = 2
    MINI_BATCH_SIZE: int = 16
    EPOCHS: int = 60
    LEARNING_RATE: float = 0.001
    GPU: bool = False

    def __init__(self, parameters: dict = None):
        super().__init__(parameters)

        mini_batch_size: int = parameters.get('mini_batch_size', DeepCNN_4Conv2D.MINI_BATCH_SIZE)
        epochs: int = parameters.get('epochs', DeepCNN_4Conv2D.EPOCHS)
        learning_rate: float = parameters.get('learning_rate', DeepCNN_4Conv2D.LEARNING_RATE)

        # These parameters have standard values for DeepCNN_4Conv2D and do not need to be modified.
        # This code is here in case in the future we want to allow changes.
        conv_filter_size: List[int] = parameters.get('conv_filter_size', DeepCNN_4Conv2D.CONV_FILTER_SIZE)
        conv_filter_number: List[int] = parameters.get('conv_filter_number', DeepCNN_4Conv2D.CONV_FILTER_NUMBER)
        activation_fn: Callable = parameters.get('activation_fn', DeepCNN_4Conv2D.ACTIVATION_FN)
        pool_size: List[int] = parameters.get('pool_size', DeepCNN_4Conv2D.POOL_SIZE)
        fully_connected_neuron_number = parameters.get('fully_connected_neuron_number', DeepCNN_4Conv2D.FULLY_CONNECTED_NEURON_NUMBER)
        output_classes: int = parameters.get('output_classes', DeepCNN_4Conv2D.OUTPUT_CLASSES)
        gpu: bool = parameters.get('GPU', DeepCNN_4Conv2D.GPU)

        conv_layer_2_size: List[int] = [(self.train_image_size[0]-conv_filter_size[0]+1)//pool_size[0],
                                        (self.train_image_size[1]-conv_filter_size[1]+1)//pool_size[1]]

        fully_connected_size: List[int] = [(conv_layer_2_size[0]-conv_filter_size[0]+1)//pool_size[0],
                                           (conv_layer_2_size[1]-conv_filter_size[1]+1)//pool_size[1]]

        self.classifier = parameters.get('classifier', self.get_4conv2D_model(DeepCNN_4Conv2D.CONV_FILTER_NUMBER,
                                                                              DeepCNN_4Conv2D.FULLY_CONNECTED_NEURON_NUMBER))
        #HERE RODRIGO!!!! WORK ON CALL TO get_4conv2D_model
    def get_4conv2D_model(self, numfm: int, numnodes: int, input_shape: Tuple[int] = (28, 28, 1),
              output_size: int = 10) -> km.Sequential:
        """
        This function returns a convolutional neural network Keras model,
        with numfm feature maps in the first convolutional layer,
        2 * numfm in the second convolutional layer, 3* numfm in the third and fourth
        and numnodes neurons in the fully-connected layer.

        Inputs:
        - numfm: int, the number of feature maps in the first convolutional layer.

        - numnodes: int, the number of nodes in the fully-connected layer.

        - intput_shape: Tuple[int], the shape of the input data,
        default = (28, 28, 1).

        - output_size: int, the number of nodes in the output layer,
          default = 10.

        Output: km.Sequential, the constructed Keras model.

        """

        # Initialize the model.
        model: km.Sequential = km.Sequential()

        # Add a 2D convolution layer, with numfm feature maps.
        model.add(kl.Conv2D(numfm, kernel_size=(5, 5),
                            input_shape=input_shape,
                            activation='relu'))

        # Adding batch normalization here  accelerates convergence during training, and improves the accuracy on the test set by 2-5%.
        model.add(kl.BatchNormalization())

        # Add a max pooling layer.
        model.add(kl.MaxPooling2D(pool_size=(2, 2)))

        # Second convolutional layer.
        model.add(kl.Conv2D(numfm * 2, kernel_size=(3, 3), activation='relu'))

        # Add a max pooling layer.
        model.add(kl.MaxPooling2D(pool_size=(2, 2),
                                  strides=(2, 2)))

        # Third convolutional layer.
        model.add(kl.Conv2D(numfm * 3, kernel_size=(3, 3),
                            activation='relu'))

        # Add a max pooling layer.
        model.add(kl.MaxPooling2D(pool_size=(2, 2),
                                  strides=(2, 2)))

        # Fourth convolutional layer.
        model.add(kl.Conv2D(numfm * 3, kernel_size=(3, 3),
                            activation='relu'))

        # Add a max pooling layer.
        model.add(kl.MaxPooling2D(pool_size=(2, 2),
                                  strides=(2, 2)))

        # Convert the network from 2D to 1D.
        model.add(kl.Flatten())

        # Add a fully-connected layer.
        model.add(kl.Dense(numnodes, activation='relu'))

        # Add the output layer.
        model.add(kl.Dense(output_size, activation='softmax'))

        # Return the model.
        return model

    def predict(self, image: numpy.ndarray) -> (numpy.ndarray, numpy.ndarray):
        if self.fc is None or self.fc is False or image is None or image is False:
            return False

        image = numpy.squeeze(image)

        row_rad = int(numpy.floor(self.train_image_size[0] / 2))
        col_rad = int(numpy.floor(self.train_image_size[1] / 2))

        self.object_positions: list = []
        self.object_map: numpy.ndarray = numpy.zeros(image.shape)
        box_list: list = []
        prob_list: list = []

        subimages = rimutils.generate_subimages(image, self.train_image_size, self.step_sz)

        row_ims = int(numpy.ceil((image.shape[0]-self.train_image_size[0]+1) / self.step_sz[0]))
        col_ims = int(numpy.ceil((image.shape[1]-self.train_image_size[1]+1) / self.step_sz[1]))

        n_iter = (row_ims * col_ims) // self.classifier.mini_batch_size

        for _ in range(n_iter):
            im_batch = []
            rows = []
            cols = []

            for _ in range(self.classifier.mini_batch_size):
                asubim, row, col = next(subimages)
                self.fc.calculate_features(asubim)
                im_batch.append(self.fc.gimme_features().squeeze())
                rows.append(row)
                cols.append(col)

            output = self.classifier.predict_batch(numpy.asarray(im_batch))

            theclass = output[0]
            theP = output[1]

            # If there is an object, store the position of the bounding box.
            for aclass, aP, arow, acol in zip(theclass, theP, rows, cols):
                if aclass == 1:
                    minrow = arow - row_rad
                    maxrow = arow + row_rad
                    if self.train_image_size[0] % 2 == 1:
                        maxrow += 1

                    mincol = acol - col_rad
                    maxcol = acol + col_rad
                    if self.train_image_size[1] % 2 == 1:
                        maxcol += 1

                    self.object_positions.append([arow, acol])
                    self.object_map[arow, acol] = 1
                    box_list.append([minrow, mincol, maxrow, maxcol])
                    prob_list.append(aP)  # theP[0][0] contains the probability of the other class (-1)

                # print(f"{arow}, {acol}: class - {aclass}, prob - {aP}")

        self.box_array = numpy.asarray(box_list)
        self.prob_array = numpy.asarray(prob_list)

        return self.box_array.copy(), self.prob_array.copy()
