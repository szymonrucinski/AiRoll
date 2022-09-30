# %%
from keras_preprocessing.image import ImageDataGenerator
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pylab as plt
import numpy as np
import tensorflow_datasets as tfds

beans_dataset, beans_info = tfds.load(
    name="beans",
    with_info=True,
    as_supervised=True,
    split=["train", "test", "validation"],
)

builder = tfds.ImageFolder("/Users/szymon/Desktop/AiRoll/data/")

# %%
ds = builder.as_dataset(split="train", shuffle_files=True)

def preprocessing(image, label):
    image /= 255.0

    return tf.image.resize(image, [224, 224]), tf.one_hot(label, 7)

datagen = ImageDataGenerator(
    rescale=1.0 / 255, horizontal_flip=True, validation_split=0.2
)
train_generator = datagen.flow_from_directory(
    directory=r"/Users/szymon/Desktop/AiRoll/data/train",
    target_size=(224, 224),
    color_mode="rgb",
    batch_size=32,
    class_mode="categorical",
    shuffle=True,
    seed=42,
    subset="training",
)

validation_generator = datagen.flow_from_directory(
    directory=r"../data/train/",
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

# %%
train_generator.class_indices.items()

for _ in range(5):
    img, label = train_generator.next()
    print(img.shape)  #  (1,256,256,3)
    plt.imshow(img[0])
    plt.show()

train_generator.class_indices


mobilenet_v2 = "https://tfhub.dev/google/imagenet/resnet_v2_50/classification/5"

mobile_net_layers = hub.KerasLayer(mobilenet_v2, input_shape=(224, 224, 3))

mobile_net_layers.trainable = False

# Build the neural network and add custom layers.
neural_net = tf.keras.Sequential(
    [
        mobile_net_layers,
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(7, activation="softmax"),
    ]
)

# %%
neural_net.summary()

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
model_fit = neural_net.fit(
    train_generator,
    epochs=epochs,
    validation_data=validation_generator,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(
            patience=10, monitor="val_prec", restore_best_weights=True
        )
    ],
)

# %%
for _ in range(len(validation_generator.labels) - 1):
    img, label = validation_generator.next()
    plt.imshow(img[0])
    pred = neural_net.predict(img)
    pred = np.argmax(pred)
    print(pred)
    pred = list(validation_generator.class_indices.keys())[pred]
    print(pred)
    plt.show()


# %%
neural_net.save("../models/")
