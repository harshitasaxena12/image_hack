import pandas as pd
from PIL import Image, ImageOps, ImageDraw, ImageFilter
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import os
import openai
import io
from io import BytesIO
import urllib.request
from streamlit_cropper import st_cropper
import numpy as np
from openai import OpenAI
from css import *
import base64
def download_image(image, filename):
    # Save image to a BytesIO object
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
IMAGE_PATH =r'C:\Users\Harshita.Saxena\Downloads\IMG_HACK\image1.jpg'
base64_image = encode_image(IMAGE_PATH)
    # Display download link
    # st.download_button(
    #     label="Download Image",
    #     data=img_bytes,
    #     file_name=filename,
    #     mime="image/jpeg"
    # )

client = OpenAI(api_key="---") #Add Openai key

set_custom_css()
st.title("Aspire Drive AI : Image Content Generator")
st.markdown("### Welcome to the Image Hack Solution")
img_gen , img_edit , img_variants = st.tabs(['**Generate Image **','**Interactive Edit - In & Out Paint**',\
                                                             '**Explore Creative Variants**'])
with img_gen:
    st.subheader('Generate your personalised Image Solution')
    col1,col2 = st.columns([0.20,0.80])
    with col1:
        car_model = st.selectbox(
        "Car Model :", ("TOYOTA COROLLA CROSS","TOYOYA LAND CRUISER","INFINITI Q70" ,"NISSAN KICKS","MG 5")
    )
    with col2: 
        if car_model :
            car = f"The generated image should be of the car {car_model} "
            prompt_user=st.text_input('The prompt for Dall-e', '')
            prompt = car + prompt_user
            prompt = prompt + ". The car should retain its original features like symbols make design .An ultra-realistic photograph captured with a Sony α7 III camera, equipped with an 85mm lens at F 1.2 aperture setting of the car.Car should be inforegoound "
            if st.button('Submit'):
                response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="hd",
                n=1,
                )
                image_url = response.data[0].url
                urllib.request.urlretrieve(image_url, "image1.jpg")
                img_dalle1 = Image.open("image1.jpg")
                download_image(img_dalle1, 'image1.jpg')
                with st.spinner('Wait for it...'):   
                    st.image(img_dalle1)
                    base64_image = encode_image(IMAGE_PATH)
                    caption = client.chat.completions.create(
                    model='gpt-4o',
                    messages=[
                        {"role": "system", "content": f"You are a helpful marketing agent assistant that responds in Markdown. Help me in generating a caption to boost sales of the given {car} "},
                        {"role": "user", "content": [
                            {"type": "text", "text": f"Generate a caption for the image that describes the specs of the {car} and helps boost sales"},
                            {"type": "image_url", "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"}
                            }
                        ]}
                    ],
                    temperature=0.0,
                )
                res = caption.choices[0].message.content
                st.write(res)
                st.success('Image Successfully Generated !')
        else :
            st.write("Please select car model")


        # Function to download the image
        # if img_dalle1:
        #     download_image(img_dalle1, 'image1.jpg')
        #     st.success("Image downloaded successfully!")

with img_edit: 
    st.markdown("##### Step 1: Upload an image")
    st.markdown("In the sidebar you can upload your image from your local computer. Note: the file should be from the PNG or JPG/JPEG file format")
    st.markdown("##### Step 2: Crop the image")
    st.markdown("When you have uploaded the image you can use this tool to select the part of the image that you want to use.")


    img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'])
    realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
    box_color = '#0000FF'

    if img_file:
        image_crop = Image.open(img_file)
        if not realtime_update:
            st.write("Double click to save crop")
        # Get a cropped image from the frontend            
        cropped_img = st_cropper(image_crop, realtime_update=realtime_update, box_color=box_color,
                                    aspect_ratio=(1, 1))   

        st.markdown("##### Step 3: Inpaint or Outpaint the image")
        st.markdown("Select inpainting or out painting. In case you choose inpainting draw \
                    on the image below to select the area you want to change. \
                    In case you choose outpainting draw on the image to select the area you want to keep.")
        inpainting = st.radio("Choose inpainting or outpainting",('Inpainting', 'Outpainting'),label_visibility="hidden")
        # Specify canvas parameters in application
        drawing_mode = st.sidebar.selectbox(
            "Drawing tool:", ("freedraw", "line", "transform","rect", "circle", "polygon", "point")
        )
        stroke_width = st.sidebar.slider("Stroke width: ", 25, 50, 3)
        if drawing_mode == 'point':
            point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
        bg_color = "#eee"
        #bg_image = Image.fromarray(np.array(cropped_img))
        img = cropped_img
        width_img, height_img =img.size
        # Create a canvas component
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
            stroke_width=stroke_width,
            stroke_color="00FFFFFF",
            background_color=bg_color,
            background_image=cropped_img if cropped_img else None,
            update_streamlit=realtime_update,
            height=512,
            width=512,
            drawing_mode=drawing_mode,
            point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
            key="canvas",
        )
        st.markdown('##### Step 4: Come up with a prompt')
        #st.markdown('A prompt is a text description of an image. It is important to remember that the prompt should describe the entire image, not just a part of it. For example, if you want to turn yourself into an astronaut, you may use the outpainting tool to select your face. The prompt is what tells the model what to do with that image. A poorly-written prompt might be something like "Add an astronaut helmet and suit" this does not give the model much information to work with, and it only describes a small part of the image. A more effective prompt would be something like "A picture from the 1970s of an astronaut wearing a space suit and helmet, floating in space with planet Mars in the background." This prompt gives the model a lot more information to work with, and it allows the model to produce a more detailed and accurate image.')
        prompt_text=st.text_input('The prompt for personalised editing (Dall-e 2)', '')
        st.write('The current prompt is:  ', prompt_text)
        # Do something interesting with the image data and paths
        def get_image(prompt_text,mask,image):
            #openai.api_key= "sk-proj-6U2T199nFR7W5JiF98B7T3BlbkFJBFDco1Ihl4JLZ6SId0Hw" #st.secrets["APIKEY"]
            response = client.images.edit(
            model="dall-e-2",
            image=image,
            mask=mask,
            prompt=prompt_text,
            n=1,
            size="512x512"
            )
            image_url = response.data[0].url
            urllib.request.urlretrieve(image_url, "image.jpg")
            img_dalle = Image.open("image.jpg")
            return img_dalle
        test = Image.fromarray(canvas_result.image_data)
        #st.image(test)
        if inpainting == 'Inpainting':
            new_img = Image.new("RGBA", test.size, (0, 0, 0, 0))
            # Loop over all pixels in the image
            #st.image(new_img)
            for x in range(test.size[0]):
                for y in range(test.size[1]):
                    # Get the RGBA values for the current pixel
                    r, g, b, a = test.getpixel((x, y))
                    # Invert the alpha value (255 becomes 0, and 0 becomes 255)
                    a = 255 - a
                    # Set the RGBA values for the current pixel in the new image
                    new_img.putpixel((x, y), (r, g, b, a))
            mask = new_img
        else:
            mask = Image.fromarray(canvas_result.image_data)

        #st.image(mask)
        mask = mask.resize((512, 512), Image.ANTIALIAS)
        img = img.resize((512, 512), Image.ANTIALIAS)

        byte_stream = BytesIO()
        img.save(byte_stream, format='PNG')
        byte_array = byte_stream.getvalue()

        byte_stream2 = BytesIO()
        mask.save(byte_stream2, format='PNG')
        byte_array_mask = byte_stream2.getvalue()

        if canvas_result.image_data is not None and cropped_img is not None:
            if st.button('Generate Dall-e image'):
                with st.spinner('Wait for it...'):
                    st.image(byte_array_mask)
                    st.image(byte_array)
                    get_image=get_image(prompt_text,byte_array_mask,byte_array)
                    
                    st.image(get_image)
                    #st.image(soften)
                    def soften_img(image, radius):
                        RADIUS = radius
                        diam = 2*RADIUS
                        back = Image.new('RGB', (image.size[0]+diam, image.size[1]+diam), (232,232,232))
                        back.paste(image, (RADIUS, RADIUS))

                        # Create paste mask
                        mask = Image.new('L', back.size, 0)
                        draw = ImageDraw.Draw(mask)
                        x0, y0 = 0, 0
                        x1, y1 = back.size
                        for d in range(diam+RADIUS):
                            x1, y1 = x1-1, y1-1
                            alpha = 255 if d<RADIUS else int(255*(diam+RADIUS-d)/diam)
                            draw.rectangle([x0, y0, x1, y1], outline=alpha)
                            x0, y0 = x0+1, y0+1
                        # Blur image and paste blurred edge according to mask
                        blur = back.filter(ImageFilter.GaussianBlur(RADIUS/2))
                        back.paste(blur, mask=mask)
                        return back                
                st.success('Done!')
                st.balloons()
            else:
                pass
        else: 
            pass
    else:
        pass
with img_variants:
        # Define the options for the radio button
    options = ('Dailogue and Image','Image Variants')

    # Initialize the selected option
    selected_option = st.session_state.page_selection if 'page_selection' in st.session_state else options[0]

    # Create the radio button with a horizontal layout
    selected_option = st.radio("", options, index=options.index(selected_option),horizontal=True, 
                               key="navigation", format_func=lambda x: x, help="Page Navigation")
    # Store the selected option in session state
    st.session_state.page_selection = selected_option
    if selected_option == 'Dailogue and Image':
        if st.button("Generate Advertisement Plot"):
            initial = f"A Singular Two Line dailogue between salesperson and a couple in a light hearted tone.Ends with a sense of confirmation that the car will be bought for select {car}"
            def get_completion(client,prompt, model="gpt-4o",temperature=0): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
                messages = [{"role": "user", "content": prompt}]
                #client = openai.OpenAI()
                response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature, # this is the degree of randomness of the model's output
            )
                return response.choices[0].message.content
            comic_res = get_completion(client,initial)
            col1,col2 = st.columns([0.20,0.80])
            with col1:
                st.write(comic_res)
            comic_prompt = "A comic strip that captures the following " + comic_res
            comic_response = client.images.generate(
            model="dall-e-3",
            prompt=comic_prompt,
            size="1024x1024",
            quality="hd",
            n=1,
            )
            image_url_comic = comic_response.data[0].url
            urllib.request.urlretrieve(image_url_comic, "image_comic.jpg")
            img_dalle_comic= Image.open("image_comic.jpg")
            with col2:
                st.image(img_dalle_comic)
    else :
        img_upload = st.file_uploader(label='Upload a file for variation', type=['png', 'jpg'])
        if img_upload:
            img_upload = Image.open(img_upload)
            width, height = 256, 256
            image = img_upload.resize((width, height))
            st.write('Uploaded Image :')
            st.image(img_upload)
            # Convert the image to a BytesIO object
            byte_stream = BytesIO()
            image.save(byte_stream, format='PNG')
            byte_array = byte_stream.getvalue()
            if st.button('Generate Variants'):
                response = client.images.create_variation(
                image=byte_array,
                n=2,
                model="dall-e-2",
                size="1024x1024"
                )
                image_url_ = response.data[0].url
                urllib.request.urlretrieve(image_url_, "image2.jpg")
                img_dalle2 = Image.open("image2.jpg")
                st.image(img_dalle2)
        else:
            pass
        


