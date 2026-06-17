import streamlit as st
import os
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Naveen Jewellers", layout="wide", page_icon="✨", initial_sidebar_state="collapsed")

IMAGE_FOLDER = "images"
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# --- 2. PREMIUM BLACK & GOLD CSS (WITH MOBILE RESPONSIVENESS) ---
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&family=Playfair+Display:ital,wght@0,400;0,500;1,400&display=swap');
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .stApp { 
        background-color: #080808; 
        font-family: 'Jost', sans-serif; 
        color: #E0E0E0; 
    }
    
    h1 { 
        font-family: 'Playfair Display', serif !important; 
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 500 !important;
        text-shadow: 0px 4px 20px rgba(212, 175, 55, 0.1); 
        text-align: center;
        font-size: 3.5rem;
        margin-top: 1rem;
        margin-bottom: 0;
        letter-spacing: 1px;
    }
    
    .block-container { 
        padding-top: 2rem !important; 
        padding-bottom: 4rem !important; 
        max-width: 1300px; 
    }
    
    /* Responsive Tabs */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 40px; 
        justify-content: center; 
        border-bottom: 1px solid #2A2415; 
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
    .stTabs [data-baseweb="tab"]:hover { color: #D4AF37 !important; }
    .stTabs [aria-selected="true"] { 
        color: #D4AF37 !important; 
        border-bottom: 2px solid #D4AF37 !important; 
    }

    /* --- THE NEW RESPONSIVE GRID SYSTEM --- */
    .jewelry-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr); /* 3 Columns on Laptops */
        gap: 40px;
        margin-top: 20px;
    }

    /* Product Card */
    .editorial-card {
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* THE CROPPING FIX: aspect-ratio 1/1 and object-fit contain */
    .img-wrapper {
        position: relative;
        overflow: hidden;
        margin-bottom: 15px;
        background: #111111; 
        aspect-ratio: 1 / 1; /* Perfect Square for Pairs of Tops/Earrings */
        border: 1px solid #332810; 
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5); 
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .img-wrapper img {
        width: 92%; /* Creates a slight dark border padding around the jewelry */
        height: 92%;
        object-fit: contain; /* THIS FIXES THE CROPPING. 100% of image is visible. */
        transition: transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        cursor: zoom-in;
    }
    .img-wrapper:hover img { transform: scale(1.08); }
    
    .product-title {
        font-family: 'Jost', sans-serif;
        font-size: 13px;
        font-weight: 400;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #F3E5AB; 
        margin: 0 0 12px 0;
    }
    
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
        background: rgba(212, 175, 55, 0.03); 
        transition: all 0.4s ease;
    }
    .btn-inquire:hover {
        background: #D4AF37; 
        color: #080808; 
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.3); 
    }

    /* --- MOBILE PHONE OPTIMIZATIONS (ANDROID & iPHONE) --- */
    @media (max-width: 768px) {
        h1 { 
            font-size: 2.2rem; /* Smaller title so it doesn't break into 3 lines */
            margin-top: 0.5rem;
        }
        .jewelry-grid {
            grid-template-columns: repeat(2, 1fr); /* 2 items side-by-side on phones */
            gap: 15px; /* Tighter spacing for small screens */
        }
        .stTabs [data-baseweb="tab-list"] { 
            gap: 15px; 
            flex-wrap: wrap; /* Allows tabs to stack nicely if there are many categories */
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 10px !important;
            padding: 0 5px 8px 5px !important;
        }
        .product-title {
            font-size: 11px; /* Smaller font for 2-column mobile layout */
            letter-spacing: 1px;
        }
        .btn-inquire {
            padding: 8px 18px; /* Slightly more compact button for thumbs */
            font-size: 10px;
        }
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- 3. CDN PRODUCT CARD RENDERER (Ultra-Fast) ---
# --- 3. CDN PRODUCT CARD RENDERER (Ultra-Fast) ---
def render_editorial_card(img_path, title):
    # Convert local file path directly into the raw GitHub URL
    safe_url_path = img_path.replace('\\', '/').replace(' ', '%20')
    github_cdn_url = f"https://raw.githubusercontent.com/aadicoder12/naveen-jewellers/main/{safe_url_path}"
    
    whatsapp_number = "8439699542" 
    raw_message = f"Hi Naveen Jewellers, I am interested in the {title}."
    encoded_message = urllib.parse.quote(raw_message)
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"
    
    # Added the WhatsApp SVG Icon inside the button, perfectly aligned with the text
    html_code = f"""
<div class="editorial-card">
    <div class="img-wrapper">
        <a href="{github_cdn_url}" target="_blank" title="View High-Res Image">
            <img src="{github_cdn_url}" loading="lazy">
        </a>
    </div>
    <div class="product-title">{title}</div>
    <a href="{whatsapp_url}" target="_blank" class="btn-inquire" style="display: inline-flex; align-items: center; justify-content: center; gap: 8px;">
        <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"/>
        </svg>
        Inquire
    </a>
</div>
"""
    return html_code

def get_categories():
    categories = [f.name for f in os.scandir(IMAGE_FOLDER) if f.is_dir()]
    return sorted(categories) if categories else ["Uncategorized"]

# --- 4. EDITORIAL HEADER ---
st.markdown("<h1>Naveen Jewellers</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family: Jost; text-transform: uppercase; letter-spacing: 5px; font-size: 11px; color: #D4AF37; margin-top: 8px; margin-bottom: 2rem;'>Fine Gold Collection</p>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; font-family: Jost; color: #A0A0A0; font-size: 0.9rem; font-weight: 300; letter-spacing: 0.5px; margin-bottom: 0.2rem;'>Near Hanuman Mandir, Nanda Devi, Almora (Uttarakhand) - 263601</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family: Jost; color: #888888; font-size: 0.8rem; font-weight: 300; letter-spacing: 1px; margin-bottom: 3rem;'>+91 9412977788 &nbsp;|&nbsp; +91 9758838488</p>", unsafe_allow_html=True)

# --- 5. PUBLIC DISPLAY SYSTEM (Now powered by CSS Grid) ---
current_categories = get_categories()
active_categories = []
for cat in current_categories:
    cat_path = os.path.join(IMAGE_FOLDER, cat)
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
                # We build a single block of HTML with our new Responsive Grid
                grid_html = '<div class="jewelry-grid">'
                for img_name in sorted(images_in_cat):
                    img_path = os.path.join(cat_path, img_name)
                    display_title = os.path.splitext(img_name)[0].replace("_", " ").title()
                    grid_html += render_editorial_card(img_path, display_title)
                grid_html += '</div>'
                
                # Render the whole grid at once
                st.markdown(grid_html, unsafe_allow_html=True)

# --- 6. MINIMALIST FOOTER ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family: Jost; font-size: 0.75rem; color: #666666; letter-spacing: 2px; text-transform: uppercase;'>© 2026 Naveen Jewellers</p>", unsafe_allow_html=True)