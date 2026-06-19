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

# 🚨 THE VAULT GUARD
if not os.path.exists(".git"):
    st.error("🚨 CRITICAL ERROR: You are in the wrong folder!")
    st.stop() 

IMAGE_FOLDER = "images"
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# --- WATERMARK ENGINE CORE (CENTERED & TRANSPARENT) ---
def apply_watermark(base_image):
    watermark_path = "watermark.png"
    if not os.path.exists(watermark_path):
        return base_image # Returns normal image if no watermark file exists
        
    try:
        # Open watermark and ensure it has transparency
        watermark = Image.open(watermark_path).convert("RGBA")
        
        # 1. Size it beautifully: Make the logo take up 50% of the image width
        base_width, base_height = base_image.size
        wm_width = int(base_width * 0.50)
        wm_ratio = wm_width / float(watermark.size[0])
        wm_height = int(float(watermark.size[1]) * float(wm_ratio))
        
        # Resize watermark cleanly
        watermark = watermark.resize((wm_width, wm_height), Image.Resampling.LANCZOS)
        
        # 2. The "Frosted Glass" Transparency Trick (Drops opacity to 25%)
        # This prevents the watermark from hiding the jewelry details
        alpha = watermark.split()[3]
        alpha = alpha.point(lambda p: int(p * 0.25)) 
        watermark.putalpha(alpha)
        
        # 3. Calculate Position: Dead Center
        x_center = (base_width - wm_width) // 2
        y_center = (base_height - wm_height) // 2
        position = (x_center, y_center)
        
        # Merge them together safely
        transparent_layer = Image.new('RGBA', base_image.size, (0,0,0,0))
        transparent_layer.paste(base_image.convert("RGBA"), (0,0))
        transparent_layer.paste(watermark, position, mask=watermark)
        
        return transparent_layer.convert("RGB")
    except Exception as e:
        st.error(f"Watermark error: {e}")
        return base_image

def get_categories():
    categories = [f.name for f in os.scandir(IMAGE_FOLDER) if f.is_dir()]
    return sorted(categories) if categories else ["Uncategorized"]

st.title("🔐 Naveen Jewellers: Private Upload Studio")
st.write("Manage your inventory with total quality control & business protection.")
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
    
    st.write("")
    upload_mode = st.radio(
        "⚙️ **Choose Image Engine:**",
        ["⚡ Fast Mobile Grid (High-Res + 600px Thumbnail)", "💎 Pure High-Res Only (No Thumbnail)"]
    )
    
    # --- WATERMARK TOGGLE ---
    use_watermark = st.checkbox("🛡️ Apply 'Naveen Jewellers' Watermark", value=False, help="Requires a 'watermark.png' file in your main folder. Stamps your logo in the bottom right corner to prevent theft.")
    st.write("")
    
    uploaded_files = st.file_uploader(
        "Drop images", 
        type=["png", "jpg", "jpeg", "webp", "dng", "heic"], 
        accept_multiple_files=True, 
        key="uploader"
    )
    
    if uploaded_files and st.button("Publish All to Category"):
        if use_watermark and not os.path.exists("watermark.png"):
            st.warning("⚠️ You checked 'Apply Watermark', but 'watermark.png' is missing from your folder. Uploading without watermark.")
            
        cat_path = os.path.join(IMAGE_FOLDER, selected_category)
        os.makedirs(cat_path, exist_ok=True)
        
        for f in uploaded_files:
            file_name = f.name.lower().replace(" ", "_")
            ext = os.path.splitext(file_name)[1]
            
            high_res_path = ""
            img_for_thumbnail = None
            
            # --- OPEN IMAGE & APPLY WATERMARK ---
            with st.spinner(f"Processing {f.name}..."):
                if ext == '.dng':
                    with rawpy.imread(f) as raw:
                        rgb = raw.postprocess()
                    base_img = Image.fromarray(rgb)
                elif ext == '.heic':
                    base_img = Image.open(f)
                else:
                    base_img = Image.open(f)
                
                # Apply Watermark if checked and file exists
                if use_watermark:
                    base_img = apply_watermark(base_img)
                
                # --- PHASE 1: Save High-Res Original ---
                new_file_name = file_name.replace(ext, ".webp")
                high_res_path = os.path.join(cat_path, new_file_name)
                
                # Convert to RGB before saving as WEBP
                if base_img.mode in ("RGBA", "P"):
                    base_img = base_img.convert("RGB")
                    
                base_img.save(high_res_path, "WEBP", quality=95)
                img_for_thumbnail = base_img.copy()
            
            # --- PHASE 2: Generate Lightning-Fast Thumbnail ---
            if upload_mode == "⚡ Fast Mobile Grid (High-Res + 600px Thumbnail)" and img_for_thumbnail:
                with st.spinner(f"Generating optimized thumbnail for {f.name}..."):
                    img_for_thumbnail.thumbnail((600, 600))
                    base_name = os.path.splitext(os.path.basename(high_res_path))[0]
                    thumb_path = os.path.join(cat_path, f"{base_name}_thumb.webp")
                    img_for_thumbnail.save(thumb_path, "WEBP", quality=85)
        
        st.success(f"Successfully processed using: {upload_mode.split('(')[0]}")
        del st.session_state["uploader"]
        st.rerun()

st.write("---")
st.write("### 🗑️ Manage Current Inventory")

current_categories = get_categories()
selected_cat = st.selectbox("View inventory for category:", current_categories)

if selected_cat:
    cat_path = os.path.join(IMAGE_FOLDER, selected_cat)
    
    if not os.path.exists(cat_path):
        all_files = []
    else:
        all_files = sorted([f for f in os.listdir(cat_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and "_thumb" not in f])
    
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
                    base_name = os.path.splitext(img_name)[0]
                    thumb_path = os.path.join(cat_path, f"{base_name}_thumb.webp")
                    if os.path.exists(thumb_path):
                        os.remove(thumb_path)
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
                st.error("The connection timed out. Try again in smaller batches.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")