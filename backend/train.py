import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from collections import defaultdict
import os
import sys

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
print("\n🧠 Detected Classes:", class_names)

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

train_counts = count_class_samples(train_ds)
val_counts = count_class_samples(val_ds)

print("\n📊 Training image count per class:")
all_good = True
for i, name in enumerate(class_names):
    count = train_counts[i]
    print(f"{i}: {name} — {count} images")
    if count == 0:
        print(f"❌ WARNING: No training images found for class '{name}'!")
        all_good = False

print("\n📊 Validation image count per class:")
for i, name in enumerate(class_names):
    count = val_counts[i]
    print(f"{i}: {name} — {count} images")
    if count == 0:
        print(f"❌ WARNING: No validation images found for class '{name}'!")
        all_good = False

if not all_good:
    print("\n⚠️ Some classes have 0 images. Fix this before training.")
    sys.exit(1)

print("✅ All classes loaded successfully with non-zero images.")

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

base_model = MobileNetV2(input_shape=IMG_SIZE + (3,), include_top=False, weights='imagenet')
base_model.trainable = True

fine_tune_at = len(base_model.layers) - 50
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

inputs = tf.keras.Input(shape=IMG_SIZE + (3,))
x = data_augmentation(inputs)
x = layers.Rescaling(1./255)(x)
x = base_model(x, training=True)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.3)(x)
outputs = layers.Dense(len(class_names), activation='softmax')(x)

model = tf.keras.Model(inputs, outputs)

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-4),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    verbose=1
)

model.save("skin_disease_classifier.keras") 
print("✅ Model trained and saved as skin_disease_classifier.h5")
