import streamlit as st
import os
import base64

# 1. Page Configuration
st.set_page_config(page_title="Naveen Jewellers", layout="wide", page_icon="✨")

IMAGE_FOLDER = "images"
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# --- 2. LUXURY CUSTOM CSS INJECTION ---
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Lato:wght@300;400;700&display=swap');
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #FAFAFA; font-family: 'Lato', sans-serif; color: #333333; }
    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #1A1A1A !important; font-weight: 600 !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; justify-content: center; border-bottom: 1px solid #EAEAEA; }
    .stTabs [data-baseweb="tab"] { font-family: 'Lato', sans-serif !important; text-transform: uppercase !important; letter-spacing: 1.5px !important; font-size: 13px !important; padding-bottom: 15px !important; color: #888888 !important; background-color: transparent !important; border: none !important; }
    .stTabs [data-baseweb="tab"]:hover { color: #1A1A1A !important; }
    .stTabs [aria-selected="true"] { color: #1A1A1A !important; font-weight: 700 !important; border-bottom: 2px solid #1A1A1A !important; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- 3. PREMIUM PRODUCT CARD RENDERER ---
# --- 3. PREMIUM PRODUCT CARD RENDERER ---
def render_premium_card(img_path, title):
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    # --- ADD THIS MISSING LOGIC ---
    ext = os.path.splitext(img_path)[1].lower()
    mime_type = "image/jpeg"
    if ext == ".png": mime_type = "image/png"
    elif ext == ".webp": mime_type = "image/webp"
    # ------------------------------
    
    html_code = f"""
        <div style="background-color: #FFFFFF; padding: 20px; border-radius: 4px; box-shadow: 0 8px 24px rgba(0,0,0,0.04); border: 1px solid #F0F0F0; margin-bottom: 15px;">
            <div style="width: 100%; aspect-ratio: 1/1; overflow: hidden; display: flex; align-items: center; justify-content: center; background: #000000; margin-bottom: 20px;">
                <img src="data:{mime_type};base64,{encoded_string}" loading="lazy" style="width: 100%; height: 100%; object-fit: contain;">
            </div>
            <h3 style="text-align: center; font-size: 1.2rem; margin: 0; padding-bottom: 10px;">{title}</h3>
        </div>
    """
    return html_code

def get_categories():
    categories = [f.name for f in os.scandir(IMAGE_FOLDER) if f.is_dir()]
    return sorted(categories) if categories else ["Uncategorized"]

# 4. Brand Header
st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-top: 2rem;'>Naveen Jewellers</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family: Lato; color: #444; letter-spacing: 1px; margin-bottom: 0.5rem;'>Near Hanuman Mandir, Nanda Devi, Almora (Uttarakhand) - 263601</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family: Lato; color: #888; font-size: 0.9rem; margin-bottom: 3rem;'>📞 9412977788 &nbsp;|&nbsp; 9758838488 &nbsp;&nbsp;&bull;&nbsp;&nbsp; GST No: 05ABQPV7823F1Z7</p>", unsafe_allow_html=True)

# 5. Public Display System 
current_categories = get_categories()
active_categories = []
for cat in current_categories:
    cat_path = os.path.join(IMAGE_FOLDER, cat)
    if os.path.exists(cat_path) and any(f.endswith((".png", ".jpg", ".jpeg", ".webp")) for f in os.listdir(cat_path)):
        active_categories.append(cat)

if not active_categories:
    st.info("The collection is currently being curated. Please check back soon.")
else:
    tabs = st.tabs(active_categories)
    for i, tab in enumerate(tabs):
        category_name = active_categories[i]
        cat_path = os.path.join(IMAGE_FOLDER, category_name)
        with tab:
            st.write("<br>", unsafe_allow_html=True)
            supported_formats = (".png", ".jpg", ".jpeg", ".webp")
            images_in_cat = [f for f in os.listdir(cat_path) if f.lower().endswith(supported_formats)]
            
            if images_in_cat:
                cols = st.columns(3)
                for index, img_name in enumerate(sorted(images_in_cat)):
                    current_col = cols[index % 3]
                    with current_col:
                        img_path = os.path.join(cat_path, img_name)
                        display_title = os.path.splitext(img_name)[0].replace("_", " ").title()
                        with st.container():
                            st.markdown(render_premium_card(img_path, display_title), unsafe_allow_html=True)