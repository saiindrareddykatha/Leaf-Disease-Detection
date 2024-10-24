from flask import Flask, jsonify
from flask import render_template
from flask import request
from PIL import Image
from tensorflow.keras.models import load_model
import numpy as np
import os

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

def delete_files_in_directory(directory_path):
   try:
     files = os.listdir(directory_path)
     for file in files:
       file_path = os.path.join(directory_path, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
         return 1
   except OSError:
     return 0

@app.route("/detect-plant-disease", methods=["GET", "POST"])
def upload_file():
    if request.method=="POST":
      try:
              directory_path = 'uploads/'
              delete_files_in_directory(directory_path)
              uploaded_image =  request.files['uploaded_image']
              uploaded_image.save("uploads/"+uploaded_image.filename)
              image_name = "uploads/"+uploaded_image.filename
              image = Image.open(image_name)
              image = image.resize((224, 224))
              image_array = np.array(image)
              image_array = image_array / 255.0
              image_array = image_array.reshape(1, 224, 224, 3)
              model_path = 'models/model.h5'
              model = load_model(model_path)
              prediction = model.predict(image_array)
              class_labels = ["Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy","Blueberry___healthy", "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy","Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Corn_(maize)__Common_rust", "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy", "Grape___Black_rot", "Grape___Esca_(Black_Measles)","Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy", "Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot", "Peach___healthy", "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy", "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy", "Raspberry___healthy", "Soybean___healthy", "Squash___Powdery_mildew", "Strawberry___Leaf_scorch", "Strawberry___healthy", "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite", "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus","Tomato___healthy"]

              class_description = {
          "Apple___Apple_scab": "A fungal disease that causes dark, scabby lesions on leaves, fruit, and bark of apple trees. It can lead to fruit deformities and premature fruit drop. A common issue in regions with cool, wet springs.",
          "Apple___Black_rot": "A fungal disease affecting apples, causing dark lesions on leaves and fruit rot. Infected fruits shrivel and turn black. The disease also causes cankers on branches and twigs.",
          "Apple___Cedar_apple_rust": "A fungal disease where bright orange spots appear on leaves, commonly caused by nearby cedar trees. It affects both apple and cedar trees in its lifecycle. The disease reduces fruit quality and weakens the tree.",
          "Apple___healthy": "The apple tree is in good health with no visible diseases. Healthy trees produce high-quality fruit and resist diseases better. Regular maintenance and monitoring help maintain tree health.",
          "Blueberry___healthy": "The blueberry plant is in good health with no visible diseases. Healthy plants produce optimal fruit yield. Ensuring proper soil conditions and watering promotes continued health.",
          "Cherry_(including_sour)___Powdery_mildew": "A fungal disease causing white powdery spots on the leaves of cherry trees. The disease can lead to stunted growth and premature leaf drop. It thrives in warm, dry conditions.",
          "Cherry_(including_sour)___healthy": "The cherry tree is in good health with no visible diseases. Healthy trees produce abundant fruit. Regular pruning and proper care help sustain tree vigor.",
          "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "A fungal disease causing grayish, elongated lesions on corn leaves. It reduces photosynthesis and can lead to lower yields. The disease is most severe in warm, humid environments.",
          "Corn_(maize)__Common_rust": "A fungal disease characterized by reddish-brown pustules on corn leaves. Infected plants may experience reduced growth and yield. Rust spreads through windborne spores.",
          "Corn_(maize)___Northern_Leaf_Blight": "A fungal disease that causes long, gray-green or tan lesions on corn leaves. Severe infections can reduce kernel fill and lead to lower yields. It typically thrives in wet conditions.",
          "Corn_(maize)___healthy": "The corn plant is in good health with no visible diseases. Healthy plants produce maximum yields. Proper soil, water, and pest management contribute to plant vigor.",
          "Grape___Black_rot": "A fungal disease causing black spots on grape leaves and fruit rot. Infected fruit shrivels and falls off, affecting crop yield. Regular pruning and fungicide application can control the spread.",
          "Grape___Esca_(Black_Measles)": "A fungal disease causing dark, streaky lesions on grapevine leaves and fruit. It can lead to leaf wilting and poor fruit development. The disease is more prevalent in older vineyards.",
          "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "A fungal disease causing small, dark spots or blights on grape leaves. It weakens the plant and reduces photosynthesis. The disease is more severe in damp, shaded areas.",
          "Grape___healthy": "The grapevine is in good health with no visible diseases. Healthy vines produce high-quality fruit and are more resilient. Proper vineyard management helps ensure vine longevity.",
          "Orange___Haunglongbing_(Citrus_greening)": "A bacterial disease that causes yellowing of leaves, misshapen fruit, and tree death. The disease is spread by the Asian citrus psyllid insect. There is no cure, making prevention critical.",
          "Peach___Bacterial_spot": "A bacterial disease causing dark, sunken spots on peach fruit and leaves. It leads to premature fruit drop and reduced quality. Wet, windy weather favors the spread of the disease.",
          "Peach___healthy": "The peach tree is in good health with no visible diseases. Healthy trees produce high-quality fruit. Proper pruning and pest management support tree vitality.",
          "Pepper,_bell___Bacterial_spot": "A bacterial disease causing dark spots on leaves and fruit of bell peppers. It can lead to leaf defoliation and poor fruit quality. The bacteria spread easily in wet, humid conditions.",
          "Pepper,_bell___healthy": "The bell pepper plant is in good health with no visible diseases. Healthy plants produce abundant, high-quality fruit. Regular watering and monitoring help maintain plant health.",
          "Potato___Early_blight": "A fungal disease causing dark, circular spots on potato leaves, leading to leaf blight. Severe infections can result in reduced yields and poor tuber quality. The disease spreads rapidly in warm, humid conditions.",
          "Potato___Late_blight": "A fungal disease causing brown lesions on leaves and tubers of potatoes. It spreads quickly in wet conditions and can cause devastating crop loss. Late blight was responsible for the Irish potato famine.",
          "Potato___healthy": "The potato plant is in good health with no visible diseases. Healthy plants yield well-formed tubers. Consistent watering and disease monitoring are important for optimal growth.",
          "Raspberry___healthy": "The raspberry plant is in good health with no visible diseases. Healthy plants produce flavorful, abundant fruit. Proper pruning and pest control are essential for maintaining plant health.",
          "Soybean___healthy": "The soybean plant is in good health with no visible diseases. Healthy plants yield protein-rich beans. Adequate soil nutrients and pest management support growth.",
          "Squash___Powdery_mildew": "A fungal disease causing white, powdery spots on the leaves of squash plants. It weakens the plant and reduces fruit yield. The disease is more severe in dry, warm conditions.",
          "Strawberry___Leaf_scorch": "A fungal disease that causes dark brown spots and scorched appearance on strawberry leaves. Infected leaves eventually dry up and fall off, reducing plant vigor. The disease is favored by wet, humid conditions.",
          "Strawberry___healthy": "The strawberry plant is in good health with no visible diseases. Healthy plants yield sweet, high-quality fruit. Proper watering and spacing promote vigorous growth.",
          "Tomato___Bacterial_spot": "A bacterial disease causing dark, water-soaked spots on tomato leaves and fruit. It can lead to premature leaf drop and poor fruit quality. The bacteria spread through wind, rain, and contaminated tools.",
          "Tomato___Early_blight": "A fungal disease causing dark spots and concentric rings on tomato leaves. It spreads quickly in warm, wet conditions, reducing yield. Proper sanitation and fungicide use help control the disease.",
          "Tomato___Late_blight": "A fungal disease causing large, irregular brown lesions on tomato leaves and fruit. It spreads rapidly in cool, wet weather and can cause severe crop loss. Late blight affects both tomatoes and potatoes.",
          "Tomato___Leaf_Mold": "A fungal disease causing yellow patches on tomato leaves and mold growth underneath. It can reduce yield and fruit quality if untreated. Humid greenhouse conditions favor its development.",
          "Tomato___Septoria_leaf_spot": "A fungal disease causing small, circular spots on tomato leaves, leading to defoliation. It weakens the plant and reduces fruit yield. The disease is more prevalent in wet, warm weather.",
          "Tomato___Spider_mites Two-spotted_spider_mite": "Damage caused by spider mites, resulting in yellowing and speckling of tomato leaves. Heavy infestations can reduce yield and weaken the plant. Spider mites thrive in hot, dry conditions.",
          "Tomato___Target_Spot": "A fungal disease causing dark, target-like spots on tomato leaves and fruit. It can lead to premature fruit drop and reduced yield. The disease spreads in warm, humid conditions.",
          "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "A viral disease causing yellowing and curling of tomato leaves, reducing yield. The virus is spread by whiteflies and can severely impact crop production. There is no cure, so prevention is key.",
          "Tomato___Tomato_mosaic_virus": "A viral disease causing mottling and mosaic-like patterns on tomato leaves. It stunts plant growth and reduces fruit yield. The virus spreads through contaminated tools, hands, and insects.",
          "Tomato___healthy": "The tomato plant is in good health with no visible diseases. Healthy plants produce abundant, high-quality fruit. Regular care and monitoring are essential for continued growth." }

              predicted_class = np.argmax(prediction)
              return({"status": 1, "detected_disease": class_labels[predicted_class], "disease_description": class_description[class_labels[predicted_class]]})
      except ValueError:
         return({"status": 0})


if __name__ == "__main__": 
    app.run(debug=True)