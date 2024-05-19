from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO

app = Flask(__name__)

# Load your trained model
model = load_model('model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    img = request.files['image']
    if img:
        img = BytesIO(img.read())
        img = image.load_img(img, target_size=(224, 224))  # Adjust size if needed
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Model expects a batch

        prediction = model.predict(img_array)
        class_idx = np.argmax(prediction, axis=1)
        classes = ['Ice Cream', 'Pizza']
        result = classes[class_idx[0]]
        return jsonify({'prediction': result})
    
    return jsonify({'error': 'No image provided'}), 400

if __name__ == '__main__':
    app.run()