import qrcode
from PIL import Image

# 1. The Link to Your Live Jewelry Store
website_url = "https://naveen-jewellers1234.streamlit.app/"

# 2. Setup the QR Code with Maximum Error Correction (Crucial!)
qr = qrcode.QRCode(
    version=5, 
    error_correction=qrcode.constants.ERROR_CORRECT_H, # 'H' means High Correction
    box_size=15, 
    border=3,
)
qr.add_data(website_url)
qr.make(fit=True)

# 3. Create the black-and-white QR code image
qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

# 4. Load your logo and place it in the center
logo_path = "logo.png"

try:
    logo = Image.open(logo_path).convert("RGBA")
    
    # Calculate how big the logo should be (25% of the total QR code size)
    basewidth = int(float(qr_img.size[0]) * 0.25)
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
    
    # Calculate the exact center coordinates
    pos = ((qr_img.size[0] - logo.size[0]) // 2,
           (qr_img.size[1] - logo.size[1]) // 2)
    
    # Paste the logo onto the QR code (using the logo's transparency mask)
    qr_img.paste(logo, pos, mask=logo)
    print("✨ Success! Logo perfectly centered.")

except FileNotFoundError:
    print(f"⚠️ Could not find '{logo_path}'. Generated a standard QR code instead.")

# 5. Save the final masterpiece
output_name = "Invoice_Custom_QR.png"
qr_img.save(output_name)
print(f"Done! Check your folder for '{output_name}'")