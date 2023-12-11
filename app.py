import json
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg'
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
import base64, os
from PIL import Image

app = Flask(__name__)

def plot_coordinates(drawing,color:bool,thumbnail_size=(200, 200)):
    """
    Plot coordinates from a drawing dictionary
    - drawing (dict): A dictionary containing the segments as keys and the Cartesian Coordinates as a list
    Returns:
    - str: Base64-encoded image of the plot
    """
    #xl,yl=find_plot_size(drawing)
    fig, ax = plt.subplots(figsize=(16,16)) #Creates the space where my plots will go
    
    for section, coordinates in drawing.items(): #Loops through the dictionary for each segment
        x_values, y_values = zip(*coordinates) #Loads all of the coordinates into a list of x and a list of y
        if color:
            ax.plot(x_values, y_values, marker='o', label=section) #draws all segments in their own color
        else:
            ax.plot(x_values, y_values, marker='o', label=section,color="black") #draws all segments in black

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
    # Creating a thumbnail from the full-size image
    full_image = Image.open(img)
    full_image.thumbnail(thumbnail_size)
    thumbnail_io = BytesIO()
    full_image.save(thumbnail_io, format='PNG')
    thumbnail_io.seek(0)
    thumbnail_base64 = base64.b64encode(thumbnail_io.getvalue()).decode()

    plt.close(fig)
    return img_base64, thumbnail_base64 #Deletes the Coordinates because they are now saved in the image
    

@app.route('/',methods=["GET","POST"])
def index():
    json_files = [file for file in os.listdir() if file.endswith('.json')]  # Get all JSON files in root
    #http://localhost:8080 will give you a multi coloured drawing
    if request.method == "GET":
        source = json_files[0]
        colour_segments = False
    else:
        source = request.form["file"]
        colour_segments = True if 'color' in request.form else False  # Check if checkbox is selected
    
    with open(source, 'r') as file:
        drawing = json.load(file)

    img_base64, thumbnail_base64 = plot_coordinates(drawing,colour_segments)
    
    return render_template('index.html', json_files=json_files,full_img=img_base64,thumbnail_img=thumbnail_base64)

@app.route('/black')
def index2():
    #http://localhost:8080/black will give you a black and white drawing
    with open('drawing.json', 'r') as file:
        drawing = json.load(file)

    img_base64, thumbnail_base64 = plot_coordinates(drawing,"black")
    
    return render_template('index.html', full_img=img_base64,thumbnail_img=thumbnail_base64)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080 ,debug=True)
