from keras_preprocessing.image import ImageDataGenerator
import tensorflow as tf
import time
import tensorflow_hub as hub
import matplotlib.pylab as plt
import numpy as np
import tensorflow_datasets as tfds
from pathlib import Path
from tensorflow.keras.applications.vgg16 import preprocess_input
import os
import wandb

wandb.init(project="airoll")

data_folder = Path(__file__).resolve().parent.parent.parent
# train_folder = Path(data_folder, "data")
train_folder = "/Users/szymon/Documents/AiRoll/data/train"
print(train_folder)

print(data_folder)
builder = tfds.ImageFolder(train_folder)

# %%
# ds = builder.as_dataset(split="train", shuffle_files=True)


# def preprocessing(image, label):
#     image /= 255.0
#     return tf.image.resize(image, [224, 224]), tf.one_hot(label, 7)


datagen = ImageDataGenerator(
    rescale=1.0 / 255, horizontal_flip=True, validation_split=0.2
)
train_generator = datagen.flow_from_directory(
    directory=train_folder,
    target_size=(224, 224),
    color_mode="rgb",
    batch_size=32,
    class_mode="categorical",
    shuffle=True,
    seed=42,
    subset="training",
)

validation_generator = datagen.flow_from_directory(
    directory=train_folder,
    target_size=(224, 224),
    color_mode="rgb",
    batch_size=32,
    class_mode="categorical",
    shuffle=True,
    seed=42,
    subset="validation",
)

train_generator.classes

from itertools import count

a = train_generator.classes.flatten().tolist()
dist_dict = {}
for label, number in train_generator.class_indices.items():
    dist_dict[label] = a.count(number)
dist_dict

print(train_generator.classes)
# %%
train_generator.class_indices.items()

# for _ in range(5):
#     img, label = train_generator.next()
#     print(img.shape)  #  (1,256,256,3)
#     plt.imshow(img[0])
#     plt.show()

train_generator.class_indices


# pretrained_model = "https://tfhub.dev/google/imagenet/resnet_v2_50/classification/5"
base_model = tf.keras.applications.vgg16.VGG16(
    include_top=False, weights="imagenet", input_shape=(224, 224, 3)
)


base_model.trainable = False

inputs = tf.keras.Input(shape=(224, 224, 3))
preprocessed_inputs = preprocess_input(inputs)
x = base_model(preprocessed_inputs, training=False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
outputs = tf.keras.layers.Dense(7, activation="softmax")(x)

neural_net = tf.keras.Model(inputs, outputs)

neural_net.summary()


# Build the neural network and add custom layers.
# neural_net = tf.keras.Sequential(
#     [
#         base_model,
#         tf.keras.layers.Dropout(0.2),
#         tf.keras.layers.Dense(7, activation="softmax"),
#     ]
# )


# %%

# %%
# Compile the deep neural network using the following code
learning_rate = 0.1
epochs = 100
decay_rate = learning_rate / epochs
neural_net.compile(
    optimizer=tf.keras.optimizers.SGD(
        learning_rate=0.95, momentum=0.8, decay=learning_rate / epochs
    ),
    loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
    metrics=[
        tf.keras.metrics.Precision(),
        tf.keras.metrics.Recall(),
    ],
)

# %%
# ...
neural_net.fit(
    train_generator,
    epochs=epochs,
    validation_data=validation_generator,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(
            patience=10, monitor="val_precision", restore_best_weights=True
        ),
        wandb.keras.WandbCallback(),
    ],
)

# %%
for _ in range(len(validation_generator.labels) - 1):
    print("1")
    img, label = validation_generator.next()
    print("2")
    plt.imshow(img[0])
    print("3")
    pred = neural_net.predict(img)
    pred = np.argmax(pred)
    print("4")
    print(pred)
    pred = list(validation_generator.class_indices.keys())[pred]
    print(pred)
    plt.show()


# %%
neural_net.save("../models/")
