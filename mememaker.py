from flask import Flask, request, send_file, jsonify
from rembg import new_session, remove
from io import BytesIO
from flask_cors import CORS  # Import CORS to handle cross-origin requests
from PIL import Image  # Import the Image module from PIL
import os

app = Flask(__name__)

# Apply CORS policy for the frontend
CORS(app, origins="https://omiemomify.netlify.app")  # Update with your React frontend URL if different

def remove_background(image):
    """Remove the background using rembg."""
    if image.mode != 'RGBA':
        image = image.convert('RGBA')  # Ensure image is in RGBA mode

    # Convert the image to a byte stream
    img_byte_arr = BytesIO()
    try:
        image.save(img_byte_arr, format='PNG')  # Save image to byte array
        img_byte_arr.seek(0)  # Go to the beginning of the byte stream

        model_name = "isnet-anime"
        rembg_session = new_session(model_name)
        
        print("Sending image to rembg for background removal.")
        output = remove(img_byte_arr.read(), post_process_mask=True)  # Use rembg to remove the background

        if not output:
            print("rembg returned an empty result.")
            return None

        # Convert the output byte data back into a PIL image
        output_image = Image.open(BytesIO(output))  # Convert bytes to image
        return output_image
    except Exception as e:
        print(f"Error in remove_background: {e}")
        return None

@app.route('/process_image', methods=['POST'])
def process_image():
    """Receive an image from the frontend, remove its background and send it back."""
    try:
        # Receive the image file from the frontend
        image_file = request.files['image']  # Expecting 'image' field in the request
        img = Image.open(image_file)  # Open the image

        # Process the image to remove its background
        foreground = remove_background(img)
        if foreground is None:
            return jsonify({"error": "Failed to remove the background from the image."})

        # Convert the final image (PIL Image) to a BytesIO object
        img_io = BytesIO()
        foreground.save(img_io, 'PNG')
        img_io.seek(0)  # Go to the beginning of the BytesIO stream

        # Return the image in the response as a file-like object (so it can be displayed in the browser)
        print("Image processed and ready to send.")
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        print(f"Error in processing image: {e}")
        return jsonify({"error": "An error occurred while processing the image."})

if __name__ == '__main__':
    
    port = int(os.getenv("PORT", 15100))

    app.run(debug=True, port=port, host='0.0.0.0')
