import streamlit as st
import os
import base64
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Naveen Jewellers", layout="wide", page_icon="✨")

IMAGE_FOLDER = "images"
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# --- 2. ULTRA-PREMIUM LUXURY CSS INJECTION ---
custom_css = """
<style>
    /* Import Luxury Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Montserrat:wght@300;400;500;600&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Set soft ivory background and default font */
    .stApp { 
        background-color: #FCFBF8; 
        font-family: 'Montserrat', sans-serif; 
        color: #333333; 
    }
    
    /* Override all headers with Playfair Display */
    h1, h2, h3 { 
        font-family: 'Playfair Display', serif !important; 
        color: #1A1A1A !important; 
        font-weight: 600 !important; 
    }
    
    /* Tighten the main container spacing */
    .block-container { 
        padding-top: 3rem !important; 
        padding-bottom: 2rem !important; 
        max-width: 1200px; 
    }
    
    /* Ultra-Premium Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 40px; 
        justify-content: center; 
        border-bottom: 1px solid #EAE5DD; 
        padding-bottom: 10px;
    }
    .stTabs [data-baseweb="tab"] { 
        font-family: 'Montserrat', sans-serif !important; 
        text-transform: uppercase !important; 
        letter-spacing: 2px !important; 
        font-size: 13px !important; 
        color: #A09E9A !important; 
        background-color: transparent !important; 
        border: none !important; 
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover { color: #D4AF37 !important; }
    .stTabs [aria-selected="true"] { 
        color: #D4AF37 !important; 
        font-weight: 500 !important; 
        border-bottom: 2px solid #D4AF37 !important; 
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- 3. PREMIUM FLOATING PRODUCT CARD RENDERER ---
# --- 3. PREMIUM FLOATING PRODUCT CARD RENDERER ---
# --- 3. PREMIUM FLOATING PRODUCT CARD RENDERER ---
def render_premium_card(img_path, title):
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    ext = os.path.splitext(img_path)[1].lower()
    mime_type = "image/jpeg"
    if ext == ".png": mime_type = "image/png"
    elif ext == ".webp": mime_type = "image/webp"
    
    whatsapp_number = "8439699542" 
    raw_message = f"Hi Naveen Jewellers, I am interested in the {title}."
    encoded_message = urllib.parse.quote(raw_message)
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"
    
    # We removed the indentations here so Streamlit doesn't think it's a code block!
    html_code = f"""
<div style="background-color: #FFFFFF; padding: 25px; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid #F7F5F0; margin-bottom: 25px; transition: transform 0.3s ease;">
    <div style="width: 100%; aspect-ratio: 1/1; overflow: hidden; display: flex; align-items: center; justify-content: center; background: #FFFFFF; margin-bottom: 20px;">
        <a href="data:{mime_type};base64,{encoded_string}" target="_blank" style="width: 100%; height: 100%; display: block;" title="Click to view high-resolution details">
            <img src="data:{mime_type};base64,{encoded_string}" loading="lazy" style="width: 100%; height: 100%; object-fit: contain; cursor: zoom-in; opacity: 0.92; transition: opacity 0.3s ease;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.92">
        </a>
    </div>
    <h3 style="text-align: center; font-size: 1.1rem; letter-spacing: 0.5px; margin: 0; padding-bottom: 5px; color: #222222 !important;">{title}</h3>
    <div style="width: 30px; height: 2px; background-color: #D4AF37; margin: 0 auto 15px auto;"></div>
    <a href="{whatsapp_url}" target="_blank" style="display: block; width: 100%; text-align: center; background-color: #25D366; color: #FFFFFF; padding: 10px 0; border-radius: 4px; text-decoration: none; font-family: 'Montserrat', sans-serif; font-weight: 500; font-size: 0.85rem; letter-spacing: 0.5px; transition: all 0.3s ease; box-shadow: 0 4px 10px rgba(37, 211, 102, 0.2);" onmouseover="this.style.backgroundColor='#1EBE53'; this.style.boxShadow='0 6px 14px rgba(37, 211, 102, 0.3)';" onmouseout="this.style.backgroundColor='#25D366'; this.style.boxShadow='0 4px 10px rgba(37, 211, 102, 0.2)';">
        <span style="font-size: 1.1rem; vertical-align: text-bottom; margin-right: 4px;">💬</span> Inquire on WhatsApp
    </a>
</div>
"""
    return html_code

def get_categories():
    categories = [f.name for f in os.scandir(IMAGE_FOLDER) if f.is_dir()]
    return sorted(categories) if categories else ["Uncategorized"]

# --- 4. BRAND HEADER (LUXURY LAYOUT) ---
st.markdown("<h1 style='text-align: center; font-size: 4.5rem; margin-top: 1rem; margin-bottom: 0; color: #D4AF37 !important; text-shadow: 1px 1px 2px rgba(0,0,0,0.05);'>✨ Naveen Jewellers ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family: Montserrat; text-transform: uppercase; letter-spacing: 4px; font-size: 14px; color: #A09E9A; margin-top: 5px; margin-bottom: 2rem;'>Exclusive Luxury Collections</p>", unsafe_allow_html=True)

# Subtle elegant divider
st.markdown("<div style='width: 100px; height: 1px; background-color: #EAE5DD; margin: 0 auto 2rem auto;'></div>", unsafe_allow_html=True)

# Address & Contact
st.markdown("<p style='text-align: center; font-family: Montserrat; color: #555555; font-weight: 300; letter-spacing: 1px; margin-bottom: 0.2rem;'>Near Hanuman Mandir, Nanda Devi, Almora (Uttarakhand) - 263601</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family: Montserrat; color: #888888; font-size: 0.85rem; font-weight: 300; letter-spacing: 1px; margin-bottom: 3.5rem;'>📞 +91 9412977788 &nbsp;|&nbsp; +91 9758838488 &nbsp;&nbsp;&bull;&nbsp;&nbsp; GST No: 05ABQPV7823F1Z7</p>", unsafe_allow_html=True)

# --- 5. PUBLIC DISPLAY SYSTEM ---
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
            st.write("<br><br>", unsafe_allow_html=True)
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

# --- 6. LUXURY FOOTER ---
st.markdown("<br><br><br><div style='width: 100%; height: 1px; background-color: #EAE5DD; margin: 2rem 0;'></div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family: Montserrat; font-size: 0.8rem; color: #A09E9A; letter-spacing: 1px;'>© 2026 NAVEEN JEWELLERS. ALL RIGHTS RESERVED.</p>", unsafe_allow_html=True)