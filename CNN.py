# import os
# import tensorflow as tf
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# import matplotlib
# matplotlib.use('Agg')

# # Paths
# train_dir = r'C:\Jaris\College\Projects\AI Heart Attack Detection\Train'
# valid_dir = r'C:\Jaris\College\Projects\AI Heart Attack Detection\Valid'
# model_save_path = r'C:\Jaris\College\Projects\AI Heart Attack Detection\path_to_your_model\heart_ecg_model.keras'
# os.makedirs(os.path.dirname(model_save_path), exist_ok=True)

# # Data Generators
# train_datagen = ImageDataGenerator(rescale=1./255)
# valid_datagen = ImageDataGenerator(rescale=1./255)

# train_dataset = train_datagen.flow_from_directory(
#     directory=train_dir,
#     target_size=(200, 200),
#     batch_size=32,
#     class_mode='categorical'
# )

# validation_dataset = valid_datagen.flow_from_directory(
#     directory=valid_dir,
#     target_size=(200, 200),
#     batch_size=32,
#     class_mode='categorical'
# )

# # CNN Model
# model = tf.keras.models.Sequential([
#     tf.keras.layers.Input(shape=(200, 200, 3)),
#     tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
#     tf.keras.layers.MaxPooling2D(2, 2),
#     tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
#     tf.keras.layers.MaxPooling2D(2, 2),
#     tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
#     tf.keras.layers.MaxPooling2D(2, 2),
#     tf.keras.layers.Flatten(),
#     tf.keras.layers.Dense(256, activation='relu'),
#     tf.keras.layers.Dense(4, activation='softmax')  # 4 classes
# ])

# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
# model.fit(train_dataset, epochs=32, validation_data=validation_dataset)

# # Save model
# model.save(model_save_path)
# print(f"✅ CNN ECG model saved at {model_save_path}")
# print("Class indices:", validation_dataset.class_indices)
