import streamlit as st

from PIL import Image
from ultralytics import YOLO



cataract_model = './Model/cataract-detection.pt'
eye_diseases_model = './Model/eye-disease-detection.pt'

image_ext = ["png", "jpg", "jpeg", "heic", "heif"]

# --- HEADER SECTION ---
with st.container():
    st.subheader("EYE DISEASE ONLINE DETECTION")
    st.write("The app is designed and developed to detect cataract, glaucoma and other eye diseases")

# --- MODELS SECTION ---
with st.container():
    st.subheader("Choose a model: Cataract Detection or Other Eye Diseases")
    selected_option = st.selectbox("Select a model", ["Eye Diseases Detector"])
    if selected_option == "Cataract Detector":
        model = YOLO(cataract_model)
    else:
        model = YOLO(eye_diseases_model)


# --- PREDICTION SECTION ---
detectedDisease = False;
with st.container():
    st.subheader("Upload your own image to diagnose")
    uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False, type=["png", "jpg", "jpeg", "heic", "heif"])
    if uploaded_file is not None:
        ext_position = len(uploaded_file.name.split('.')) - 1
        file_ext = uploaded_file.name.split('.')[ext_position]
        if file_ext in image_ext:
            image = Image.open(uploaded_file)
            # Resize the image while maintaining aspect ratio
            max_size = 640
            img_width, img_height = image.size
            if img_width > max_size or img_height > max_size:
                # Calculate the aspect ratio
                aspect_ratio = img_width / img_height
                if img_width > img_height:
                    new_width = max_size
                    new_height = int(max_size / aspect_ratio)
                else:
                    new_height = max_size
                    new_width = int(max_size * aspect_ratio)
                image = image.resize((new_width, new_height), Image.LANCZOS)

            else:
                # If both width and height are smaller than max_size, upscale to max_size
                aspect_ratio = img_width / img_height
                if img_width > img_height:
                    new_width = max_size
                    new_height = int(max_size / aspect_ratio)
                else:
                    new_height = max_size
                    new_width = int(max_size * aspect_ratio)
                image = image.resize((new_width, new_height), Image.LANCZOS)

            st.header("Uploaded Image")
            st.image(image, width=400)
            results = model.predict(image, conf = 0.5)
            result = results[0]
            st.header("Predictions Result")
            result_plotted = result.plot()
            st.image(result_plotted,
                        caption='Detected result',
                        channels="BGR",
                        use_column_width=False,
                        width=400)
            count = 0
            for box in result.boxes:
                class_id = result.names[box.cls[0].item()]
                cords = box.xyxy[0].tolist()
                cords = [round(x) for x in cords]
                conf = (round(box.conf[0].item(), 2))
                percentage_conf = f"{conf * 100:.0f}%"
                st.text(f"Disease: {class_id}")
                st.text(f"Confidence: {percentage_conf}")
                if class_id != "Normal" and class_id != "Normal_eyes" :
                    detectedDisease = True
                    count = count + 1
                st.divider()
            if detectedDisease:
                st.subheader(f'Result: {count} diseases detected')
            else:
                st.subheader(f'Result: no diseases detected')

