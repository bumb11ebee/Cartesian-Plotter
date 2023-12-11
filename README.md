# Cartesian-Plotter
The Cartesian Coordinates are written in a special file format called JSON.

Example:

`{
    "Name of the segment":[List of coordinates for that segment]
}`

My code will connect all of the coordinates for each segment in the order they are written in the list.

If you have more than one segment or shape just repeat the pattern.

Save the coordinates in a file called drawing.json

## Running the Code
I'm running this on a macbook.

Download my code to a folder on your macbook.

I'm running this on python 3.11

### Steps

* Open Terminal and go to the fodler where you downloaded this code then type:
```
python3.11 -m venv venv

source venv/bin/activate
```

* Next install all the python libraries by typing:

```
pip install -r requirements.txt
```
* Then run my code by typing:
```
python app.py
```
* To see your drawing open up a browser and go to http://localhost:8080 which will show you each segment in its own color OR got to http://localhost:8080/black to see your drawing in black and white