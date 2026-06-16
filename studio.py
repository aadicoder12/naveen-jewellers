import streamlit as st
import os
import shutil
import subprocess
import rawpy
from PIL import Image
import pillow_heif

# Teach Python how to read Apple HEIC files seamlessly
pillow_heif.register_heif_opener()

st.set_page_config(page_title="Admin - Naveen Jewellers", layout="wide", page_icon="🔐")

# 🚨 THE VAULT GUARD: Prevents the "Folder-in-a-Folder" Trap
if not os.path.exists(".git"):
    st.error("🚨 CRITICAL ERROR: You are in the wrong folder!")
    st.warning("Your computer cannot push to the live website because you are not inside the main GitHub vault.")
    st.info("**How to fix this:**\n1. Close VS Code.\n2. Move `studio.py`, `app.py`, and your `images/` folder directly inside the `naveen-jewellers` folder.\n3. Open VS Code, click **File > Open Folder**, and select the `naveen-jewellers` folder.\n4. Run the app again.")
    st.stop() # Stops the rest of the app from running until they fix it

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
    
    new_category = st.text_input("New category name:")
    if st.button("Add Category"):
        if new_category:
            os.makedirs(os.path.join(IMAGE_FOLDER, new_category.title().strip()), exist_ok=True)
            st.rerun()
            
    st.write("---")
    categories = get_categories()
    cat_to_delete = st.selectbox("Select category to remove:", categories)
    if st.button(f"🗑️ Delete Category: {cat_to_delete}"):
        cat_path = os.path.join(IMAGE_FOLDER, cat_to_delete)
        if os.path.exists(cat_path):
            shutil.rmtree(cat_path)
            st.success(f"Category '{cat_to_delete}' removed!")
        st.rerun()

with col_upload:
    st.write("### 📤 2. Upload Jewelry")
    categories = get_categories()
    selected_category = st.selectbox("Select category:", categories)
    
    st.info("💡 **Pro-Tip:** To prevent 'Connection Failed' errors, upload a maximum of 20 to 30 images at a time.")
    
    uploaded_files = st.file_uploader(
        "Drop images", 
        type=["png", "jpg", "jpeg", "webp", "dng", "heic"], 
        accept_multiple_files=True, 
        key="uploader"
    )
    
    if uploaded_files and st.button("Publish All to Category"):
        cat_path = os.path.join(IMAGE_FOLDER, selected_category)
        os.makedirs(cat_path, exist_ok=True)
        
        for f in uploaded_files:
            file_name = f.name.lower().replace(" ", "_")
            ext = os.path.splitext(file_name)[1]
            
            if ext == '.dng':
                with st.spinner(f"Converting raw file {f.name} to WebP..."):
                    with rawpy.imread(f) as raw:
                        rgb = raw.postprocess()
                    img = Image.fromarray(rgb)
                    new_file_name = file_name.replace(".dng", ".webp")
                    img.save(os.path.join(cat_path, new_file_name), "WEBP", quality=95)
                    
            elif ext == '.heic':
                with st.spinner(f"Converting iPhone HEIC {f.name} to WebP..."):
                    img = Image.open(f)
                    new_file_name = file_name.replace(".heic", ".webp")
                    img.save(os.path.join(cat_path, new_file_name), "WEBP", quality=95)
                    
            else:
                with open(os.path.join(cat_path, file_name), "wb") as out:
                    out.write(f.getbuffer())
        
        st.success("Uploaded & Processed successfully!")
        del st.session_state["uploader"]
        st.rerun()

st.write("---")
st.write("### 🗑️ Manage Current Inventory")

# 2. Optimized Inventory Section
current_categories = get_categories()
selected_cat = st.selectbox("View inventory for category:", current_categories)

if selected_cat:
    cat_path = os.path.join(IMAGE_FOLDER, selected_cat)
    
    if not os.path.exists(cat_path):
        all_files = []
    else:
        all_files = sorted([f for f in os.listdir(cat_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))])
    
    if not all_files:
        st.info("No images here.")
    else:
        items_per_page = 8
        total_pages = (len(all_files) - 1) // items_per_page + 1
        page = st.number_input("Page number", min_value=1, max_value=total_pages, value=1)
        
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

# --- 3. Publish & Sync to Live Server ---
st.write("---")
st.write("### 🚀 Sync with Live Website")
col_pull, col_push = st.columns(2)

with col_pull:
    st.write("**Missing files? Download from website:**")
    if st.button("📥 Download Latest Updates (Git Pull)", use_container_width=True):
        with st.spinner("Downloading missing folders/images from GitHub..."):
            result = subprocess.run(["git", "pull"], capture_output=True, text=True)
            if result.returncode == 0:
                st.success("✅ Download complete! Refreshing...")
                st.rerun()
            else:
                st.error(f"Failed to download. Error detail:\n{result.stderr}")

with col_push:
    st.write("**Ready to go live? Push to website:**")
    if st.button("🌐 Push Changes to Live Server", type="primary", use_container_width=True):
        with st.spinner("Connecting to GitHub and uploading..."):
            try:
                add_result = subprocess.run(["git", "add", "--all", "images/"], capture_output=True, text=True)
                if add_result.returncode != 0:
                    st.error(f"Failed to add files: {add_result.stderr}")
                    st.stop()

                commit_result = subprocess.run(["git", "commit", "-m", "Auto-update inventory via Studio"], capture_output=True, text=True)
                if "nothing to commit" in commit_result.stdout or "nothing to commit" in commit_result.stderr:
                    st.info("Everything is already up to date! No new changes to push.")
                    st.stop()
                elif commit_result.returncode != 0 and "nothing to commit" not in commit_result.stdout:
                    st.error(f"Commit failed: {commit_result.stderr}")
                    st.stop()

                push_result = subprocess.run(["git", "push"], capture_output=True, text=True, timeout=60)
                if push_result.returncode == 0:
                    st.success("🎉 Success! Your new inventory is live. (Remember to 'Clear Cache' on your live site if it doesn't update immediately!)")
                    st.balloons()
                else:
                    st.error(f"Push to GitHub failed. Error detail:\n{push_result.stderr}")
                    
            except subprocess.TimeoutExpired:
                st.error("The connection timed out. Your internet might have dropped, or the files were too large. Try again in smaller batches.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")