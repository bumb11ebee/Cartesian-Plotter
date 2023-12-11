import json
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg'
from flask import Flask, render_template
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
import base64

app = Flask(__name__)

def plot_coordinates(drawing,color=None):
    fig, ax = plt.subplots()
    
    for section, coordinates in drawing.items():
        x_values, y_values = zip(*coordinates)
        if color == None:
            ax.plot(x_values, y_values, marker='o', label=section)
        else:
            ax.plot(x_values, y_values, marker='o', label=section,color=color)

    #ax.legend()
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.grid(True, which='both', linestyle='--', linewidth=1, alpha=0.5)  # Customize grid lines# Set ticks at each 1 unit for both x and y axes
    ax.set_xticks(range(int(min(ax.get_xlim())), int(max(ax.get_xlim())) + 1, 1))
    ax.set_yticks(range(int(min(ax.get_ylim())), int(max(ax.get_ylim())) + 1, 1))
    fig.tight_layout()
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    
    img_base64 = base64.b64encode(img.getvalue()).decode()
    
    plt.close(fig)
    return img_base64

@app.route('/')
def index():
    with open('drawing.json', 'r') as file:
        drawing = json.load(file)

    img_base64 = plot_coordinates(drawing)
    
    return render_template('index.html', img_base64=img_base64)

@app.route('/black')
def index2():
    with open('drawing.json', 'r') as file:
        drawing = json.load(file)

    img_base64 = plot_coordinates(drawing,"black")
    
    return render_template('index.html', img_base64=img_base64)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080 ,debug=True)
