from preprocess import preprocess_input


class DataGeneratorConfig(object):
    """ Contains dictionaries of configurations """

    NORMALISE = dict(featurewise_center=False,
                     samplewise_center=False,
                     featurewise_std_normalization=True,
                     samplewise_std_normalization=True,
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

    NORM_AND_TRANSFORM = dict(featurewise_center=False,
                              samplewise_center=False,
                              featurewise_std_normalization=True,
                              samplewise_std_normalization=True,
                              preprocessing_function=preprocess_input,
                              rotation_range=15,
                              width_shift_range=0.9,
                              height_shift_range=0.,
                              shear_range=0.,
                              zoom_range=0.3,
                              channel_shift_range=0.,
                              fill_mode='reflect',
                              cval=0.,
                              horizontal_flip=True,
                              vertical_flip=False,
                              rescale=None)

    TRANSFORM = dict(preprocessing_function=preprocess_input,
                     rotation_range=15,
                     width_shift_range=0.9,
                     height_shift_range=0.,
                     shear_range=0.,
                     zoom_range=0.3,
                     channel_shift_range=0.,
                     fill_mode='reflect',
                     cval=0.,
                     horizontal_flip=True,
                     vertical_flip=False,
                     rescale=None)
