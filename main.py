import streamlit as st
import tensorflow
from keras.models import load_model 
from PIL import Image
import numpy as np
from streamlit_extras.stylable_container import stylable_container

from util import classify, set_background


set_background('bg2.jpg')

# Define the styles for the container
with stylable_container(
    key="container_main",
    css_styles="""
        {
            border: 1px solid rgba(49, 51, 63, 0.2);
            border-radius: 0.5rem;
            padding: calc(1em);
            background-color: rgba(255, 255, 255, 0.1);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(5px);
        }
    """
):
    # Set title
    st.markdown(
        """
        <style>
            @keyframes gradientAnimation {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            .gradient-text {
                background: linear-gradient(270deg, #f32170, #ff6b08, #cf23cf, #eedd44);
                background-size: 400% 400%;
                animation: gradientAnimation 8s ease infinite;
                background-clip: text;
                -webkit-background-clip: text;
                color: transparent;
                text-align: center;
                display: inline-block;
            }
        </style>

        <h1 class="gradient-text">
            Cherry Plant Disease(Powdery Mildew) Detection App
        </h1>
        """,
        unsafe_allow_html=True
    )
    # set header
    st.write('#### Please Upload a Cherry Plant Leaf Image')
    # upload file
    file = st.file_uploader('', type=['jpeg', 'jpg', 'png'])

# load classifier
model = load_model('Model_DenseNet121.h5')
# load class names
with open('labels.txt', 'r') as f:
    class_names = [a[:-1].split(' ')[1] for a in f.readlines()]
    f.close()
# display image
if file is not None:
    image = Image.open(file).convert('RGB')
    st.image(image, use_column_width=True)

    # classify image
    class_name, conf_score = classify(image, model, class_names)

    # Define the styles for the container
    with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px);
                background-color: rgba(255, 255, 255, 0.1);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(5px);
            }
        """
    ):
        # Format the text
        st.write("## Detecting: :green[{}]".format(class_name))
        st.write("### The Model Predicts a :red[{}%] Chances That The Uploaded Cherry Plant Contains {}.".format(int(conf_score * 1000) / 10,class_name))


