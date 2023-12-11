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
    """
    Plot coordinates from a drawing dictionary
    - drawing (dict): A dictionary containing the segments as keys and the Cartesian Coordinates as a list
    Returns:
    - str: Base64-encoded image of the plot
    """

    fig, ax = plt.subplots() #Creates the space where my plots will go
    
    for section, coordinates in drawing.items(): #Loops through the dictionary for each segment
        x_values, y_values = zip(*coordinates) #Loads all of the coordinates into a list of x and a list of y
        if color == None:
            ax.plot(x_values, y_values, marker='o', label=section) #draws all segments in their own color
        else:
            ax.plot(x_values, y_values, marker='o', label=section,color=color) #draws all segments in black

    #ax.legend()
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.grid(True, which='both', linestyle='--', linewidth=1, alpha=0.5)  # Customize grid lines# Set ticks at each 1 unit for both x and y axes
    ax.set_xticks(range(int(min(ax.get_xlim())), int(max(ax.get_xlim())) + 1, 1)) #Draws grid lines at every 1 unit
    ax.set_yticks(range(int(min(ax.get_ylim())), int(max(ax.get_ylim())) + 1, 1)) #Draws grid lines at every 1 unit
    fig.tight_layout() #Spaces the grid lines out so you can read them better
    canvas = FigureCanvas(fig) #Updates the figure with all of my segments
    img = BytesIO() #Creates a balnk image file
    fig.savefig(img, format='png') #Writes my plots to the blank image
    img.seek(0) #Sets the reading point of the file to the beginning
    
    img_base64 = base64.b64encode(img.getvalue()).decode() #No idea about this but it rewrites the image into a format that the computer will draw
    
    plt.close(fig) #Deletes the Coordinates because they are now saved in the image
    return img_base64

@app.route('/')
def index():
    #http://localhost:8080 will give you a multi coloured drawing
    with open('drawing.json', 'r') as file:
        drawing = json.load(file)

    img_base64 = plot_coordinates(drawing)
    
    return render_template('index.html', img_base64=img_base64)

@app.route('/black')
def index2():
    #http://localhost:8080/black will give you a black and white drawing
    with open('drawing.json', 'r') as file:
        drawing = json.load(file)

    img_base64 = plot_coordinates(drawing,"black")
    
    return render_template('index.html', img_base64=img_base64)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080 ,debug=True)
