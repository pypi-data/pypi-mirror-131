import os
import re
import numpy as np
import pandas as pd
from skimage import color, io
import matplotlib.pyplot as plt
import sklearn
from tqdm import tqdm
from sklearn import preprocessing
from keras.preprocessing import image
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

from keras.applications.vgg16 import VGG16
from tensorflow.keras.optimizers import Adam

from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import Conv2D, MaxPooling2D

modelImages = Sequential()
shape = (28, 28, 3)
images = pd.DataFrame()
le = preprocessing.LabelEncoder()
re_image = re.compile(r'.jpg$|.png$')


def load_test_data(training_file):
    """Load the test file and build a model from sample images.

    Parameters
    ----------
    training_file : str
        Path to CSV training file containing 2 columns, 'path' and 'category'.

    Returns
    -------
    """
    global images
    images = pd.read_csv(training_file)

    le.fit(images['category'])
    images['class'] = le.transform(images['category'])

    images.head()

    train_image = []

    for i in tqdm(range(images.shape[0])):
        img = image.load_img(images['path'][i], target_size=shape)
        img = image.img_to_array(img)
        img = img/255
        train_image.append(img)

    x = np.array(train_image)
    y = images['class'].values

    build_model_manual(x, to_categorical(y))


def build_model_manual(x, y):
    """Build the model using the images produced in the load step.

    Parameters
    ----------
    x : ndarray
        numpy array of image data
    y : Series.array
        numeric categories for each image

    Returns
    -------
    """
    global modelImages
    classes = len(y[0])

    modelImages = Sequential()
    modelImages.add(Conv2D(32, (3, 3), activation="relu", input_shape=shape))
    modelImages.add(Conv2D(64, (3, 3), activation="relu"))
    modelImages.add(MaxPooling2D(pool_size=(2, 2)))
    modelImages.add(Flatten())
    modelImages.add(Dense(128, activation="relu"))
    modelImages.add(Dense(classes, activation="softmax"))

    modelImages.compile("Adam", "categorical_crossentropy", ["accuracy"])
    modelImages.fit(x, y, epochs=10)


def build_model_vgg16(x, y):
    """For future use...

    Parameters
    ----------
    x : ndarray
        numpy array of image data
    y : Series.array
        numeric categories for each image

    Returns
    -------
    """
    global modelImages

    classes = len(y[0])
    lr = 1e-6
    modelImages = VGG16(weights=None, input_shape=shape, classes=classes)
    modelImages.compile(Adam(lr=lr), "categorical_crossentropy", ["accuracy"])
    modelImages.fit(x, y, epochs=20, batch_size=256, verbose=2)


def predict(path):
    """Given an image path, produce a prediction of probability for each class

    Parameters
    ----------
    path : str
        Path to a test image

    Returns
    -------
    """
    test_image = []
    test = image.load_img(path, target_size=shape)
    test_image.append(image.img_to_array(test)/255)
    return modelImages.predict(np.array(test_image))


def predict_print(path, categories):
    """Prints the probability for each category

    Parameters
    ----------
    path : str
        Path to an image
    categories : array
        array of categories to display

    Returns
    -------
    """
    prediction = predict(path)
    for category in categories:
        print_category(prediction, category)


def print_category(prediction, category):
    """Print the probability of a single category

    Parameters
    ----------
    prediction : keras prediction

    category : str
        category to test

    Returns
    -------
    """
    classification = class_from_category(category)
    print(f"{category}: {prediction[0][classification] * 100:.0f}%")


def predict_category(path):
    """Get the category predicted by the model

    Parameters
    ----------
    path : str
        Path to an image

    Returns
    -------
    category : str
        Predicted category
    """
    prediction = np.argmax(predict(path), axis=1)
    return images[images['class'] == prediction[0]]['category'].unique()[0]


def class_from_category(category):
    """Get the class ID given category string

    Parameters
    ----------
    category : str
        Text description of category as listed in training data

    Returns
    -------
    class : int
        numeric index of category
    """
    return images[images['category'] == category]['class'].unique()[0]


def find_category(path, category, blacklist="$^"):
    """Given a directory, find all images predicted for a given category

    Parameters
    ----------
    path : str
        Folder to search
    category : str
        Category of interest
    blacklist : str
         (Default value = "$^")
         expression defining file paths to skip

    Returns
    -------
    hits : array
        Array of files predicted to be in the given category
    """
    re_blacklist = re.compile(blacklist)

    hits = []
    for folderName, subfolders, filenames in os.walk(path):
        for filename in filenames:
            filePath = folderName + '\\' + filename
            filePath = filePath.lower()

            if re_image.search(filePath) is None:
                continue
            if re_blacklist.search(filePath) is not None:
                continue
            print(filePath)
            predicted = predict_category(filePath)
            if (predicted == category):
                hits.append(filePath)
    return hits


def find_best_fit(hits, category):
    """Given a list of files predicted to be in a given category,
    find the file with the highest probability

    Parameters
    ----------
    hits : array of str
        List of files predicted to be in the category
    category : str
        Category of predicted files

    Returns
    -------
    bestfile : str
        Path of the highest probability
    """
    bestfit = 0
    bestfile = ""
    class_fit = class_from_category(category)
    for file in hits:
        last = predict(file)[0][class_fit]
        print(last)
        if last > bestfit:
            print("replacing best fit with...")
            bestfit = last
            print(file)
            bestfile = file
    return bestfile


def find_best_fit_by_folder(path, category, blacklist="$^"):
    """Search a folder for images. Compare each image and return best fit.

    Parameters
    ----------
    path : str

    category :


    blacklist : str
         (Default value = "$^")
         expression defining file paths to skip

    Returns
    -------
    """
    hits = find_category(path, category, blacklist)
    return find_best_fit(hits, category)


def show_image(image, title='Image', cmap_type='gray'):
    """Display the image

    Parameters
    ----------
    image : str
        path to the image
    title : str
        (Default value = 'Image')
    cmap_type :
        (Default value = 'gray')

    Returns
    -------
    """
    bits = io.imread(image)
    bits_grey = color.rgb2gray(bits)
    plt.imshow(bits_grey, cmap=cmap_type)
    plt.title(title)
    plt.axis('off')
    plt.show()
