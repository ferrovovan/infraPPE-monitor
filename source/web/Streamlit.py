import streamlit as st
from PIL import Image
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
import tensorflow as tf

# Заголовок приложения
st.title("Классификация изображений с помощью ResNet50")

# Описание
st.write("Загрузите изображение, и модель ResNet50 предскажет, что на нем изображено.")

# Загрузка изображения
uploaded_file = st.file_uploader("Выберите изображение...", type=["jpg", "jpeg", "png"])

# Загрузка модели ResNet50
@st.cache_resource
def load_model():
    return ResNet50(weights='imagenet')

model = load_model()

# Функция для обработки изображения
def preprocess_image(image):
    # Изменение размера изображения до 224x224 (требование ResNet50)
    image = image.resize((224, 224))
    # Конвертация в массив numpy
    image_array = np.array(image)
    # Добавление размерности для батча
    image_array = np.expand_dims(image_array, axis=0)
    # Предобработка изображения для ResNet50
    image_array = preprocess_input(image_array)
    return image_array

# Обработка загруженного изображения
if uploaded_file is not None:
    # Отображение загруженного изображения
    image = Image.open(uploaded_file)
    st.image(image, caption="Загруженное изображение", use_column_width=True)
    
    # Предобработка изображения
    processed_image = preprocess_image(image)
    
    # Предсказание
    predictions = model.predict(processed_image)
    # Декодирование результатов
    decoded_predictions = decode_predictions(predictions, top=3)[0]
    
    # Вывод результатов
    st.subheader("Результаты классификации:")
    for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
        st.write(f"{i+1}. {label}: {score:.2%} уверенности")