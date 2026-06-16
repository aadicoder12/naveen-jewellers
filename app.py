import streamlit as st
import os
import base64
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Naveen Jewellers", layout="wide", page_icon="✨", initial_sidebar_state="collapsed")

IMAGE_FOLDER = "images"
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# --- 2. EDITORIAL HIGH-FASHION CSS INJECTION (PREMIUM BLACK & GOLD) ---
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&family=Playfair+Display:ital,wght@0,400;0,500;1,400&display=swap');
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* The Vault Background: Very deep charcoal/black */
    .stApp { 
        background-color: #080808; 
        font-family: 'Jost', sans-serif; 
        color: #E0E0E0; 
    }
    
    /* Luxury Gold Gradient Title */
    h1 { 
        font-family: 'Playfair Display', serif !important; 
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 500 !important;
        text-shadow: 0px 4px 20px rgba(212, 175, 55, 0.1); /* Faint gold glow */
    }
    
    /* Secondary Gold Headers */
    h2, h3 { 
        font-family: 'Playfair Display', serif !important; 
        color: #D4AF37 !important; 
        font-weight: 500 !important;
    }
    
    .block-container { 
        padding-top: 2rem !important; 
        padding-bottom: 4rem !important; 
        max-width: 1300px; 
    }
    
    /* Minimalist Tabs with Gold Underlines */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 40px; 
        justify-content: center; 
        border-bottom: 1px solid #2A2415; /* Tinted gold-brown border */
        padding-bottom: 15px;
        margin-bottom: 30px;
    }
    .stTabs [data-baseweb="tab"] { 
        font-family: 'Jost', sans-serif !important; 
        text-transform: uppercase !important; 
        letter-spacing: 2px !important; 
        font-size: 12px !important; 
        color: #888888 !important; 
        background-color: transparent !important; 
        border: none !important; 
        padding: 0 10px 10px 10px !important;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover { 
        color: #D4AF37 !important; /* Text turns gold on hover */
    }
    .stTabs [aria-selected="true"] { 
        color: #D4AF37 !important; 
        border-bottom: 2px solid #D4AF37 !important; /* Thicker gold line for active category */
    }

    /* Editorial Product Card Classes */
    .editorial-card {
        text-align: center;
        margin-bottom: 40px;
    }
    .img-wrapper {
        position: relative;
        overflow: hidden;
        margin-bottom: 15px;
        background: #111111; 
        aspect-ratio: 4/5; 
        border: 1px solid #332810; /* Very subtle gold/brown frame around the photo */
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5); /* Deep shadow to lift it off the background */
    }
    .img-wrapper img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        cursor: zoom-in;
    }
    .img-wrapper:hover img {
        transform: scale(1.08); 
    }
    .product-title {
        font-family: 'Jost', sans-serif;
        font-size: 13px;
        font-weight: 400;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #F3E5AB; /* Very soft champagne white/gold for text */
        margin: 0 0 12px 0;
    }
    
    /* The Premium Gold Inquire Button */
    .btn-inquire {
        display: inline-block;
        padding: 10px 30px;
        border: 1px solid #D4AF37; 
        color: #D4AF37; 
        text-decoration: none;
        font-family: 'Jost', sans-serif;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 2px;
        background: rgba(212, 175, 55, 0.03); /* Barely visible gold tint inside */
        transition: all 0.4s ease;
    }
    .btn-inquire:hover {
        background: #D4AF37; /* Fills with solid gold */
        color: #080808; /* Text turns pitch black */
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.3); /* Button glows gold when hovered */
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- IMAGE CACHING ENGINE ---
@st.cache_data(show_spinner=False)
def get_image_base64(img_path):
    with open(img_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# --- 3. EDITORIAL PRODUCT CARD RENDERER ---
def render_editorial_card(img_path, title):
    encoded_string = get_image_base64(img_path)
    
    ext = os.path.splitext(img_path)[1].lower()
    mime_type = "image/jpeg"
    if ext == ".png": mime_type = "image/png"
    elif ext == ".webp": mime_type = "image/webp"
    
    # WhatsApp Integration
    whatsapp_number = "919412977788" 
    raw_message = f"Hi Naveen Jewellers, I am interested in the {title}."
    encoded_message = urllib.parse.quote(raw_message)
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"
    
    safe_url_path = img_path.replace('\\', '/').replace(' ', '%20')
    github_high_res_url = f"https://raw.githubusercontent.com/aadicoder12/naveen-jewellers/main/{safe_url_path}"
    
    # Clean, borderless HTML matching the CSS
    html_code = f"""
<div class="editorial-card">
    <div class="img-wrapper">
        <a href="{github_high_res_url}" target="_blank" title="View High-Res Image">
            <img src="data:{mime_type};base64,{encoded_string}" loading="lazy">
        </a>
    </div>
    <div class="product-title">{title}</div>
    <a href="{whatsapp_url}" target="_blank" class="btn-inquire">Inquire</a>
</div>
"""
    return html_code

def get_categories():
    categories = [f.name for f in os.scandir(IMAGE_FOLDER) if f.is_dir()]
    return sorted(categories) if categories else ["Uncategorized"]

# --- 4. EDITORIAL HEADER ---
st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-top: 1rem; margin-bottom: 0; letter-spacing: 1px;'>Naveen Jewellers</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family: Jost; text-transform: uppercase; letter-spacing: 5px; font-size: 11px; color: #888888; margin-top: 8px; margin-bottom: 2rem;'>Fine Gold Collection</p>", unsafe_allow_html=True)

# Minimal contact info
st.markdown("<p style='text-align: center; font-family: Jost; color: #555555; font-size: 0.9rem; font-weight: 300; letter-spacing: 0.5px; margin-bottom: 0.2rem;'>Near Hanuman Mandir, Nanda Devi, Almora (Uttarakhand) - 263601</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family: Jost; color: #999999; font-size: 0.8rem; font-weight: 300; letter-spacing: 1px; margin-bottom: 3rem;'>+91 9412977788 &nbsp;|&nbsp; +91 9758838488</p>", unsafe_allow_html=True)

# --- 5. PUBLIC DISPLAY SYSTEM ---
current_categories = get_categories()
active_categories = []
for cat in current_categories:
    cat_path = os.path.join(IMAGE_FOLDER, cat)
    # Added .jpeg support here to match the studio updates
    if os.path.exists(cat_path) and any(f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")) for f in os.listdir(cat_path)):
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
                cols = st.columns(3, gap="large") # Wider gap for that airy, expensive feel
                for index, img_name in enumerate(sorted(images_in_cat)):
                    current_col = cols[index % 3]
                    with current_col:
                        img_path = os.path.join(cat_path, img_name)
                        display_title = os.path.splitext(img_name)[0].replace("_", " ").title()
                        st.markdown(render_editorial_card(img_path, display_title), unsafe_allow_html=True)

# --- 6. MINIMALIST FOOTER ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family: Jost; font-size: 0.75rem; color: #999999; letter-spacing: 2px; text-transform: uppercase;'>© 2026 Naveen Jewellers</p>", unsafe_allow_html=True)