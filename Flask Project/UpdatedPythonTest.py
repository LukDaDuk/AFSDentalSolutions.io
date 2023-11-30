import matplotlib
matplotlib.use('Agg')
from PIL import Image
import os
import matplotlib.pyplot as plt
import io

def red_saturation(pixel):
    r, g, b = pixel
    avg = (r + g + b) / 3
    return r - avg

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif']

def check_teeth_condition(file_storage):
    if isinstance(file_storage, io.BytesIO):
        file_storage.seek(0)  # Reset file pointer to the beginning
        img = Image.open(file_storage)
    else:
        img = Image.open(file_storage.stream)
    img_rgb = img.convert("RGB")

    total_red_saturation = 0
    saturation_values = []

    for pixel in img_rgb.getdata():
        saturation = red_saturation(pixel)
        saturation_values.append(saturation)
        total_red_saturation += saturation

    avg_saturation = total_red_saturation / (img_rgb.width * img_rgb.height)

    result_key = ""
    if avg_saturation > 80:
        result_key = "condition2"
    elif avg_saturation < 30:
        result_key = "condition1"
    else:
        result_key = "condition3"

    processed_image_path = 'processed_image.jpg'
    img_rgb.save(os.path.join('static', processed_image_path))

    plt.figure()
    plt.plot(saturation_values)
    plt.title('Saturation Graph')
    plt.xlabel('Pixel Index')
    plt.ylabel('Red Saturation Value')
    saturation_graph_path = 'saturation_graph.jpg'
    plt.savefig(os.path.join('static', saturation_graph_path))
    plt.close()

    return result_key, processed_image_path, saturation_graph_path
