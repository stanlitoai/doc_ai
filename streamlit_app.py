import streamlit as st
import os
import base64
import google.generativeai as genai
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Google API key
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

# Configure generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to load OpenAI model and get responses
def get_gemini_response(input_text, image, prompt):
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        }
    ]

    model = genai.GenerativeModel("gemini-pro-vision")
    # model = model.start_chat(history=[])
    response = model.generate_content([input_text, image[0], prompt], safety_settings=safety_settings)
    return response.text


def input_image_setup(uploaded_image):
    if uploaded_image is not None:
        bytes_data = uploaded_image.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_image.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        st.error("Can't read uploaded image.")


# Initialize Streamlit app
st.set_page_config(page_title="Extractor App",
                   page_icon=":art:",
                   layout="centered",
                   initial_sidebar_state="auto")

# Custom CSS for gradient background and centering content
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #ff7e5f, #feb47b); /* Gradient from pink to orange */
        font-family: Arial, sans-serif;
    }
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    .title {
        color: #fff; /* White color */
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center; /* Center the text */
    }
    .subtitle {
        color: #fff; /* White color */
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center; /* Center the text */
    }
    </style>
    """, unsafe_allow_html=True)

# Main content
with st.container() as container:
    with st.container() as content:
        # Revised title
        st.markdown('<h1 class="title">Document Description AI</h1>', unsafe_allow_html=True)
        st.markdown(
            '<p class="subtitle">Extracting and Describing Information from Documents</p>',
            unsafe_allow_html=True
        )

# Sidebar
# Revised sidebar content
st.sidebar.header("About the Document Description AI")

with st.sidebar:
    st.image("pic.png", use_column_width=True)  # Add your logo here for branding
    st.markdown(
        """
        ## Welcome to Document Description AI
        Extracting insights from documents made effortless. Our AI solution empowers businesses with accurate and insightful descriptions, enhancing decision-making and productivity.
        """
    )
    st.markdown(
    """
    ## Contact Information
    Email: mosesstanley99@gmail.com
    """
    )

# Separator with improved styling
st.markdown(
    """
    <style>
    .separator {
        margin-top: 20px;
        margin-bottom: 20px;
        height: 3px;
        background-color: #ddd;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='separator'></div>", unsafe_allow_html=True)


# Input area
input_text = st.text_input(
    label="Enter key terms and details to generate a descriptive document summary:",
    placeholder="Provide details for document summarization...",
    key="document_input",
    help="Please enter relevant information and key terms to generate a detailed document summary."
)

# Image uploader
uploaded_image = st.file_uploader("Select an image...",
                                  type=["jpg", "jpeg", "png"],
                                  help=r"Click the `Browse files` to upload an image of your choice.")

# Display uploaded image
if uploaded_image is not None:
    image_data = base64.b64encode(uploaded_image.read()).decode()
    st.markdown(
        f'<div style="display: flex; justify-content: center;"><img src="data:image/png;base64,{image_data}" '
        f'alt="Uploaded Image" style="width: 50%; height: auto; max-width: 500px; border-radius: 15%; '
        f'border: 10px solid #ff7f0e;"></div>',
        unsafe_allow_html=True
    )

# Button to trigger description generation
submit_button = st.button("Describe the Product")

# Predefined prompt
input_prompt = """
    Welcome to the Expert Product Image Description task. 
    \n Your expertise is crucial in understanding product images and crafting compelling descriptions. 
    \n You will receive input product images, and your role is to 
    generate captivating product descriptions based on the visual information.

    \n Example: Analyze the provided image of a [Product Type] and generate a detailed description. 
    \n Highlight key features, materials used, and any unique design elements. 
    \n Consider potential customer inquiries and proactively address them in your description.

    \n Your goal is to create vivid, informative, and engaging product descriptions that resonate with our target audience. 
    Maintain a professional tone and ensure that your responses are tailored to the specific details present in the image.

    \n This prompt is tailored for extracting info not only from invoices but also from some other kind of usual documents 
    in a company's financial department. However, it is not English language, it is Romanian language.
    """

# Handle button click event
if submit_button:
    if uploaded_image and input_text:
        with st.spinner("Reading your product and generating description..."):
            start = time.time()
            image_data = input_image_setup(uploaded_image)
            response = get_gemini_response(input_text, image_data, input_prompt)
            st.subheader("Hey Buddy \n Here is your product description:")
            st.markdown(response)
            end = time.time()
    elif uploaded_image and not input_text:
        st.error("Please enter your prompt details before describing the product.")
    elif input_text and not uploaded_image:
        st.error("Please upload your product image before describing the product.")
    else:
        st.error("Please upload your product image and prompt details before describing the product.")
