import streamlit as st
import os
import shutil
import subprocess
import rawpy
from PIL import Image

st.set_page_config(page_title="Admin - Naveen Jewellers", layout="wide", page_icon="🔐")

IMAGE_FOLDER = "images"
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

def get_categories():
    categories = [f.name for f in os.scandir(IMAGE_FOLDER) if f.is_dir()]
    return sorted(categories) if categories else ["Uncategorized"]

st.title("🔐 Naveen Jewellers: Private Upload Studio")
st.write("Manage your inventory. Optimized for speed.")
st.write("---")

# 1. Upload & Create Section
col_upload, col_manage = st.columns([2, 1])

with col_manage:
    st.write("### 📁 1. Create/Delete Categories")
    
    # Create
    new_category = st.text_input("New category name:")
    if st.button("Add Category"):
        if new_category:
            os.makedirs(os.path.join(IMAGE_FOLDER, new_category.title().strip()), exist_ok=True)
            st.rerun()
            
    # Delete
    st.write("---")
    categories = get_categories()
    cat_to_delete = st.selectbox("Select category to remove:", categories)
    if st.button(f"🗑️ Delete Category: {cat_to_delete}"):
        cat_path = os.path.join(IMAGE_FOLDER, cat_to_delete)
        shutil.rmtree(cat_path)
        st.success(f"Category '{cat_to_delete}' removed!")
        st.rerun()

with col_upload:
    st.write("### 📤 2. Upload Jewelry")
    categories = get_categories()
    selected_category = st.selectbox("Select category:", categories)
    
    # 🚨 ADDED .dng SUPPORT HERE 🚨
    uploaded_files = st.file_uploader("Drop images", type=["png", "jpg", "jpeg", "webp", "dng"], accept_multiple_files=True, key="uploader")
    
    if uploaded_files and st.button("Publish All to Category"):
        cat_path = os.path.join(IMAGE_FOLDER, selected_category)
        for f in uploaded_files:
            file_name = f.name.lower().replace(" ", "_")
            ext = os.path.splitext(file_name)[1]
            
            # 🚨 THE NEW DNG AUTO-CONVERTER 🚨
            if ext == '.dng':
                with st.spinner(f"Converting raw file {f.name} to WebP..."):
                    with rawpy.imread(f) as raw:
                        rgb = raw.postprocess()
                    img = Image.fromarray(rgb)
                    # Change extension to .webp for the live site
                    new_file_name = file_name.replace(".dng", ".webp")
                    img.save(os.path.join(cat_path, new_file_name), "WEBP", quality=95)
            else:
                # Normal save for png/jpg/webp
                with open(os.path.join(cat_path, file_name), "wb") as out:
                    out.write(f.getbuffer())
        
        st.success("Uploaded & Processed successfully!")
        del st.session_state["uploader"]
        st.rerun()

st.write("---")
st.write("### 🗑️ Manage Current Inventory")

# 2. Optimized Inventory Section with Pagination
current_categories = get_categories()
selected_cat = st.selectbox("View inventory for category:", current_categories)

if selected_cat:
    cat_path = os.path.join(IMAGE_FOLDER, selected_cat)
    all_files = sorted([f for f in os.listdir(cat_path) if f.lower().endswith(('.png', '.jpg', '.webp'))])
    
    if not all_files:
        st.info("No images here.")
    else:
        # Define how many images per page
        items_per_page = 8
        total_pages = (len(all_files) - 1) // items_per_page + 1
        
        page = st.number_input("Page number", min_value=1, max_value=total_pages, value=1)
        
        # Calculate start/end indices for current page
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        current_page_files = all_files[start_idx:end_idx]
        
        cols = st.columns(4)
        for i, img_name in enumerate(current_page_files):
            with cols[i % 4]:
                img_path = os.path.join(cat_path, img_name)
                st.image(img_path, use_container_width=True)
                if st.button("Delete", key=f"del_{img_name}"):
                    os.remove(img_path)
                    st.rerun()

# --- 3. Publish to Live Server ---
st.write("---")
st.write("### 🚀 Publish to Live Website")
st.write("Click below to automatically push your latest inventory to the internet.")

if st.button("🌐 Sync Changes to Live Server", type="primary"):
    with st.spinner("Connecting to GitHub and uploading..."):
        try:
            # Stage the changes in the images folder
            subprocess.run(["git", "add", "images/"], check=True)
            
            # Commit the changes
            subprocess.run(["git", "commit", "-m", "Auto-update inventory via Studio"], check=True)
            
            # Push to GitHub
            subprocess.run(["git", "push"], check=True)
            
            st.success("🎉 Success! Your new inventory is live. (It may take 60 seconds to appear on the site).")
            st.balloons()
            
        except subprocess.CalledProcessError as e:
            # Handles the case where you click the button but haven't added new images
            if "nothing to commit" in str(e) or e.returncode == 1:
                st.info("Everything is already up to date! No new changes to push.")
            else:
                st.error("Failed to sync. Make sure your GitHub connection is working.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")