import tensorflow as tf
from tensorflow.keras import layers
import keras.utils as kutils
import os

model_present = False
# Check if 'model.h5' file is present
if os.path.isfile('model.h5'):
    model_present = True

if not model_present:
    # Environment variables
    TRAIN_DIR = 'dataset/train'
    VAL_DIR = 'dataset/valid'
    BATCH_SIZE = 32
    EPOCHS = 100

    train_ds = kutils.image_dataset_from_directory(
        TRAIN_DIR,
        labels='inferred',
        label_mode='categorical',
        batch_size=BATCH_SIZE,
        image_size=(224, 224),
        color_mode='rgb',
        shuffle=True,
        seed = 42,
    )

    val_ds = kutils.image_dataset_from_directory(
        VAL_DIR,
        labels='inferred',
        label_mode='categorical',
        image_size=(224, 224),
        batch_size=BATCH_SIZE,
        color_mode='rgb',
        shuffle=True,
        seed = 42,
    )

    model = tf.keras.Sequential([
            layers.Rescaling(1./255, input_shape=(224, 224, 3)),
            layers.Conv2D(16, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            layers.MaxPool2D((2, 2)),
            layers.Conv2D(32, (3, 3), activation='relu'),
            layers.MaxPool2D((2, 2)),
            layers.GlobalAvgPool2D(),
            layers.Dense(128, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(2, activation='sigmoid')
            ])
    
    model.summary()
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    history = model.fit(
        train_ds,
        epochs=EPOCHS,
        validation_data=val_ds,
        callbacks=[ tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=6, restore_best_weights=True)]
    )
    model.save('model.h5')

else:
    
    TEST_DIR = 'dataset/test'
    BATCH_SIZE = 32
    EPOCHS = 10
    
    test_ds = kutils.image_dataset_from_directory(
        TEST_DIR,
        labels='inferred',
        label_mode='categorical',
        image_size=(224, 224),
        batch_size=BATCH_SIZE,
        color_mode='rgb',
        shuffle=False,
        seed = 42,
    )
    
    model = tf.keras.models.load_model('model.h5')
    results = model.evaluate(test_ds, verbose=0)
    print(f'Test loss: {round(results[0])}')
    print(f'Test accuracy: {round(results[1],4)*100}%')
    
    