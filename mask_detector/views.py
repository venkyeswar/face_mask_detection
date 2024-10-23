from django.shortcuts import render
from .forms import UploadImageForm
from .models import MaskImage
from tensorflow.keras.preprocessing.image import img_to_array
from django.core.files.uploadedfile import InMemoryUploadedFile
import numpy as np
import cv2
from PIL import Image
import os
from keras.models import load_model
from django.conf import settings

# Load the model once when the module is imported
model_path = os.path.join(settings.BASE_DIR, 'model.h5')
model = load_model(model_path)

def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            # Perform model prediction
            label, confidence = predict_mask(image_file)

            # Save the image and prediction result in the database (if needed)
            mask_image = MaskImage(image=image_file, label=label, confidence=confidence)
            mask_image.save()

            # Prepare to display the uploaded image and prediction
            return render(request, 'mask_detector/index.html', {
                'form': form,
                'label': label,
                'confidence': confidence,
                'image_url': mask_image.image.url
            })

    else:
        form = UploadImageForm()
    
    # On GET request, just render the form without result
    return render(request, 'mask_detector/index.html', {'form': form})

def predict_mask(image):
    # Open image, resize and preprocess it for the model
    image = Image.open(image)
    image = image.resize((128, 128))  # Resize the image for the model
    image = img_to_array(image)       # Convert image to array
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    image = image / 255.0  # Normalize the image

    # Predict using the loaded model
    prediction = model.predict(image)[0][0]

    # Determine the label and confidence
    if prediction < 0.8:
        return "Without Mask", float(prediction)
    else:
        return "With Mask", float(prediction)
