import os

from keras import backend as K
from keras.applications.vgg16 import VGG16
from keras.layers import Dense
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.vis_utils import plot_model as plot
import matplotlib.pyplot as plt

from source import TEST_PATH
from source import TRAIN_PATH

VALIDATION_PATH = TEST_PATH
img_width, img_height = 224, 224
batch_size = 32
number_of_epoch = 20


def colour_channel_swapping(x, dim_ordering):
    """ Colour channel swapping from RGB to BGR """
    if dim_ordering == 'th':
        x = x[::-1, :, :]
    elif dim_ordering == 'tf':
        x = x[:, :, ::-1]
    else:
        raise Exception("Ordering not allowed. Use one of these: 'tf' or 'th'")
    return x


def mean_subtraction(x, dim_ordering):
    """ Mean subtraction for VGG16 model re-training

    :param x matrix with the first index following the BGR convention
    :param dim_ordering th for theano and tf for tensorflow
    """
    if dim_ordering == 'th':
        # Zero-center by mean pixel
        x[0, :, :] -= 103.939
        x[1, :, :] -= 116.779
        x[2, :, :] -= 123.68
    elif dim_ordering == 'tf':
        # Zero-center by mean pixel
        x[:, :, 0] -= 103.939
        x[:, :, 1] -= 116.779
        x[:, :, 2] -= 123.68
    else:
        raise Exception("Ordering not allowed. Use one of these: 'tf' or 'th'")
    return x


def preprocess_input(x, dim_ordering='default'):
    """ Colour space swapping and data normalization

    From RGB to BGR swapping.
    Apply a mean subtraction (the mean comes from VGG16 model
    """
    # Get type of ordering (Tensorflow or Theanos)
    if dim_ordering == 'default':
        dim_ordering = K.image_dim_ordering()
    assert dim_ordering in {'tf', 'th'}

    x = colour_channel_swapping(x, dim_ordering)
    x = mean_subtraction(x, dim_ordering)
    return x


def get_base_model():
    """ create the base pre-trained model """
    base_model = VGG16(weights='imagenet')
    plot(base_model,
         to_file='results/session4/modelVGG16a.png',
         show_shapes=True,
         show_layer_names=True)
    return base_model


def modify_model_for_eight_classes(base_model):
    """ Modify to classify 8 classes.

    Get the XXX layer and add a FC to classify scenes (8-class classifier)
    """
    x = base_model.layers[-2].output
    x = Dense(8, activation='softmax', name='predictions')(x)

    model = Model(inputs=base_model.input, outputs=x)
    plot(model,
         to_file='results/session4/modelVGG16b.png',
         show_shapes=True,
         show_layer_names=True)

    for layer in base_model.layers:
        layer.trainable = False

    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])
    return model


def do_plotting(history):
    # summarize history for accuracy
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.savefig('results/session4/accuracy.jpg')
    plt.close()

    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.savefig('results/session4/loss.jpg')


def main():
    base_model = get_base_model()
    model = modify_model_for_eight_classes(base_model)
    for layer in model.layers:
        print(layer.name, layer.trainable)

    # preprocessing_function=preprocess_input,
    datagen = ImageDataGenerator(featurewise_center=False,
                                 samplewise_center=False,
                                 featurewise_std_normalization=False,
                                 samplewise_std_normalization=False,
                                 preprocessing_function=preprocess_input,
                                 rotation_range=0.,
                                 width_shift_range=0.,
                                 height_shift_range=0.,
                                 shear_range=0.,
                                 zoom_range=0.,
                                 channel_shift_range=0.,
                                 fill_mode='nearest',
                                 cval=0.,
                                 horizontal_flip=False,
                                 vertical_flip=False,
                                 rescale=None)

    train_generator = datagen.flow_from_directory(TRAIN_PATH,
                                                  target_size=(
                                                      img_width, img_height),
                                                  batch_size=batch_size,
                                                  class_mode='categorical')

    test_generator = datagen.flow_from_directory(TEST_PATH,
                                                 target_size=(
                                                     img_width, img_height),
                                                 batch_size=batch_size,
                                                 class_mode='categorical')

    validation_generator = datagen.flow_from_directory(VALIDATION_PATH,
                                                       target_size=(
                                                           img_width,
                                                           img_height),
                                                       batch_size=batch_size,
                                                       class_mode='categorical')
    history = model.fit_generator(train_generator,
                                  steps_per_epoch=(int(
                                      400 * 1881 / 1881 // batch_size) + 1),
                                  epochs=number_of_epoch,
                                  validation_data=validation_generator,
                                  validation_steps=807)

    result = model.evaluate_generator(test_generator, val_samples=807)
    print(result)

    # list all data in history
    if False:
        do_plotting(history)


if __name__ == '__main__':
    try:
        os.makedirs('results/session4')
    except OSError as expected:
        # Expected when the folder already exists
        pass

    main()
