import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import createTrainingData
import json


def plot_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                         100 * np.max(predictions_array),
                                         class_names[true_label]),
               color=color)


def plot_value_array(i, predictions_array, true_label):
    predictions_array, true_label = predictions_array[i], true_label[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')


# fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels, class_names) = createTrainingData.returnTrainingData()
(test_images, test_labels) = createTrainingData.returnTestingData(class_names, 3000)
(train_images, train_labels) = createTrainingData.returnTestingData(class_names, 40000)
# train_images = np.concatenate((train_images, moreTraining))
# train_labels = np.concatenate((train_labels, moreTrainingLabels))

# (train_images2, train_labels2), (test_images2, test_labels2) = fashion_mnist.load_data()
# class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker',
# 'Bag', 'Ankle boot']

# old_model = keras.models.load_model('setIconModel.h5')

# loss, acc = old_model.evaluate(test_images, test_labels)

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(90, 90)),
    keras.layers.Dense(64, activation=tf.nn.relu),
    keras.layers.Dropout(.150),
    keras.layers.Dense(64, activation=tf.nn.relu),
    keras.layers.Dropout(.150),
    keras.layers.Dense(len(class_names), activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=65, batch_size=1024)

test_loss, test_acc = model.evaluate(test_images, test_labels)

print('Test accuracy:', test_acc)
predictions = model.predict(test_images)
model.save('setIconModel.h5')

num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions, test_labels, test_images)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions, test_labels)
plt.show()

