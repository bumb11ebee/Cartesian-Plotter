import json
from flask import Flask, render_template
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

def plot_coordinates(drawing):
    for section, coordinates in drawing.items():
        x_values, y_values = zip(*coordinates)
        plt.plot(x_values, y_values, marker='o', label=section)
    
    plt.legend()
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    
    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Encode the image to base64 for embedding in HTML
    img_base64 = base64.b64encode(img.getvalue()).decode()
    
    plt.close()  # Close the plot to avoid displaying it in the terminal
    return img_base64

@app.route('/')
def index():
    with open('drawing.json', 'r') as file:
        drawing = json.load(file)

    img_base64 = plot_coordinates(drawing)
    
    return render_template('index.html', img_base64=img_base64)

if __name__ == '__main__':
    app.run(debug=True)
