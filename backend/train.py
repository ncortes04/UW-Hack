import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from collections import defaultdict
import os

DATA_DIR = "dataset/train_set"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
SEED = 42

print("🔍 Checking for GPU support...")
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"✅ GPU detected: {gpus[0].name}")
else:
    print("⚠️ No GPU detected. Using CPU instead.")

train_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="validation",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

class_names = train_ds.class_names
print("🧠 Classes:", class_names)

with open("class_names.txt", "w") as f:
    for name in class_names:
        f.write(name + "\n")
print("✅ Saved class_names.txt")

def count_class_samples(dataset):
    counts = defaultdict(int)
    for _, labels in dataset:
        for label in labels.numpy():
            counts[label] += 1
    return counts

counts = count_class_samples(train_ds)
print("\n📊 Training image count per class:")
for i, name in enumerate(class_names):
    print(f"{i}: {name} — {counts[i]} images")

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

base_model = MobileNetV2(
    input_shape=IMG_SIZE + (3,),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False 

inputs = tf.keras.Input(shape=IMG_SIZE + (3,))
x = layers.Rescaling(1./255)(inputs)
x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.3)(x)
outputs = layers.Dense(len(class_names), activation='softmax')(x)

model = tf.keras.Model(inputs, outputs)

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)

model.save("skin_disease_classifier.h5")
print("✅ Model trained and saved as skin_disease_classifier.h5")
