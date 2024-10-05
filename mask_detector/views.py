from django.shortcuts import render, redirect
from .forms import UploadImageForm
from .models import MaskImage
from tensorflow.keras.preprocessing.image import img_to_array
from django.core.files.uploadedfile import InMemoryUploadedFile
import numpy as np
import cv2
import os
from keras.models import load_model
from django.conf import settings

# Load the model once when the module is imported
model_path = os.path.join(settings.BASE_DIR, 'predicting_model.h5')
model = load_model(model_path)

def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            # Perform your model prediction here
            label, confidence = predict_mask(image_file)  # Call the predict function

            # Save the image and prediction result in the database
            mask_image = MaskImage(image=image_file, label=label, confidence=confidence)
            mask_image.save()

            return redirect('result', pk=mask_image.pk)

    else:
        form = UploadImageForm()
    return render(request, 'mask_detector/upload.html', {'form': form})

def result(request, pk):
    mask_image = MaskImage.objects.get(pk=pk)
    return render(request, 'mask_detector/result.html', {'mask_image': mask_image})

def predict_mask(image):
    file_bytes = np.asarray(bytearray(image.read()),dtype=np.uint8)
    img = cv2.imdecode(file_bytes,cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Image not Loaded Correctly")
    
    img_resized = cv2.resize(img,(128,128))
    img_array = np.array(img_resized)/255.0
    img_array = np.expand_dims(img_array,axis=0)
      
    prediction = model.predict(img_array)[0][0]

    # Determine the label and confidence
    if prediction > 0.8:
        return "Without Mask", float(prediction)
    else:
        return "With Mask", float(prediction)

