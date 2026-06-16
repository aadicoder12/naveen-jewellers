import qrcode

# 1. Set up the QR code instructions
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H, # High error correction (looks more dense and professional)
    box_size=20, # Makes the image massive and high-res
    border=4,    # Adds a clean white border
)

# 2. Add your live website link
qr.add_data('https://naveen-jewellers1234.streamlit.app/')
qr.make(fit=True)

# 3. Create and save the image
img = qr.make_image(fill_color="black", back_color="white")
img.save("Naveen_Jewellers_QR.png")

print("QR Code generated successfully! Check your folder.")