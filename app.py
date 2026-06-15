import streamlit as st
import os
import base64
import urllib.parse

# 1. Page Configuration (Optimized for speed)
st.set_page_config(page_title="Naveen Jewellers", layout="wide", page_icon="✨", initial_sidebar_state="collapsed")

IMAGE_FOLDER = "images"
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# --- 2. ULTRA-PREMIUM LUXURY CSS INJECTION ---
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Montserrat:wght@300;400;500;600&display=swap');
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .stApp { 
        background-color: #FCFBF8; 
        font-family: 'Montserrat', sans-serif; 
        color: #333333; 
    }
    
    h1, h2, h3 { 
        font-family: 'Playfair Display', serif !important; 
        color: #1A1A1A !important; 
    }
    
    .block-container { 
        padding-top: 2rem !important; 
        padding-bottom: 2rem !important; 
        max-width: 1200px; 
    }
    
    /* Sleek, Modern Tabs */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 30px; 
        justify-content: center; 
        border-bottom: 1px solid #EAE5DD; 
        padding-bottom: 5px;
    }
    .stTabs [data-baseweb="tab"] { 
        font-family: 'Montserrat', sans-serif !important; 
        text-transform: uppercase !important; 
        letter-spacing: 2px !important; 
        font-size: 13px !important; 
        color: #A09E9A !important; 
        background-color: transparent !important; 
        border: none !important; 
        padding: 10px 15px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stTabs [data-baseweb="tab"]:hover { 
        color: #D4AF37 !important; 
        transform: translateY(-2px);
    }
    .stTabs [aria-selected="true"] { 
        color: #D4AF37 !important; 
        font-weight: 600 !important; 
        border-bottom: 2px solid #D4AF37 !important; 
    }

    /* Floating Card Animation */
    .premium-card {
        background-color: #FFFFFF; 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.02); 
        border: 1px solid #F7F5F0; 
        margin-bottom: 20px; 
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
    }
    .premium-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.06);
        border-color: #EAE5DD;
    }
    
    /* Image Zoom Hover */
    .img-container img {
        transition: transform 0.5s cubic-bezier(0.165, 0.84, 0.44, 1);
    }
    .img-container:hover img {
        transform: scale(1.05);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- CACHING ENGINE (MASSIVE SPEED BOOST) ---
@st.cache_data(show_spinner=False)
def get_image_base64(img_path):
    """Memorizes the image data so it loads instantly next time."""
    with open(img_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# --- 3. PREMIUM FLOATING PRODUCT CARD RENDERER ---
def render_premium_card(img_path, title):
    encoded_string = get_image_base64(img_path)
    
    ext = os.path.splitext(img_path)[1].lower()
    mime_type = "image/jpeg"
    if ext == ".png": mime_type = "image/png"
    elif ext == ".webp": mime_type = "image/webp"
    
    whatsapp_number = "919412977788" 
    raw_message = f"Hi Naveen Jewellers, I am interested in the {title}."
    encoded_message = urllib.parse.quote(raw_message)
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"
    
    safe_url_path = img_path.replace('\\', '/').replace(' ', '%20')
    github_high_res_url = f"https://raw.githubusercontent.com/aadicoder12/naveen-jewellers/main/{safe_url_path}"
    
    html_code = f"""
<div class="premium-card">
    <div class="img-container" style="width: 100%; aspect-ratio: 1/1; overflow: hidden; border-radius: 8px; display: flex; align-items: center; justify-content: center; background: #FFFFFF; margin-bottom: 20px;">
        <a href="{github_high_res_url}" target="_blank" style="width: 100%; height: 100%; display: block;" title="Click to view high-resolution details">
            <img src="data:{mime_type};base64,{encoded_string}" loading="lazy" style="width: 100%; height: 100%; object-fit: contain; cursor: zoom-in; opacity: 0.95;">
        </a>
    </div>
    <h3 style="text-align: center; font-size: 1.05rem; letter-spacing: 0.5px; margin: 0; padding-bottom: 5px; color: #222222 !important;">{title}</h3>
    <div style="width: 25px; height: 2px; background-color: #D4AF37; margin: 0 auto 15px auto; border-radius: 2px;"></div>
    
    <a href="{whatsapp_url}" target="_blank" style="display: block; width: 100%; text-align: center; background-color: #25D366; color: #FFFFFF; padding: 12px 0; border-radius: 6px; text-decoration: none; font-family: 'Montserrat', sans-serif; font-weight: 600; font-size: 0.85rem; letter-spacing: 0.5px; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='#1EBE53';" onmouseout="this.style.backgroundColor='#25D366';">
        <span style="font-size: 1.1rem; vertical-align: text-bottom; margin-right: 4px;">💬</span> Inquire
    </a>
</div>
"""
    return html_code

@st.cache_data(show_spinner=False)
def get_categories():
    categories = [f.name for f in os.scandir(IMAGE_FOLDER) if f.is_dir()]
    return sorted(categories) if categories else ["Uncategorized"]

# --- 4. BRAND HEADER (LUXURY LAYOUT) ---
st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-top: 0.5rem; margin-bottom: 0; color: #D4AF37 !important;'>✨ Naveen Jewellers ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family: Montserrat; text-transform: uppercase; letter-spacing: 4px; font-size: 13px; color: #A09E9A; margin-top: 5px; margin-bottom: 1.5rem;'>Exclusive Luxury Collections</p>", unsafe_allow_html=True)

st.markdown("<div style='width: 80px; height: 1px; background-color: #EAE5DD; margin: 0 auto 1.5rem auto;'></div>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; font-family: Montserrat; color: #666666; font-size: 0.9rem; font-weight: 400; letter-spacing: 1px; margin-bottom: 0.2rem;'>Near Hanuman Mandir, Nanda Devi, Almora (Uttarakhand) - 263601</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family: Montserrat; color: #888888; font-size: 0.8rem; font-weight: 300; letter-spacing: 1px; margin-bottom: 3rem;'>📞 +91 9412977788 &nbsp;|&nbsp; +91 9758838488 &nbsp;&nbsp;&bull;&nbsp;&nbsp; GST: 05ABQPV7823F1Z7</p>", unsafe_allow_html=True)

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
            st.write("<br>", unsafe_allow_html=True)
            supported_formats = (".png", ".jpg", ".jpeg", ".webp")
            images_in_cat = [f for f in os.listdir(cat_path) if f.lower().endswith(supported_formats)]
            
            if images_in_cat:
                cols = st.columns(3, gap="medium") # Added medium gap for better spacing
                for index, img_name in enumerate(sorted(images_in_cat)):
                    current_col = cols[index % 3]
                    with current_col:
                        img_path = os.path.join(cat_path, img_name)
                        display_title = os.path.splitext(img_name)[0].replace("_", " ").title()
                        st.markdown(render_premium_card(img_path, display_title), unsafe_allow_html=True)

# --- 6. LUXURY FOOTER ---
st.markdown("<br><br><div style='width: 100%; height: 1px; background-color: #EAE5DD; margin: 2rem 0;'></div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family: Montserrat; font-size: 0.75rem; color: #B0AFA9; letter-spacing: 1.5px;'>© 2026 NAVEEN JEWELLERS. CRAFTED WITH ELEGANCE.</p>", unsafe_allow_html=True)