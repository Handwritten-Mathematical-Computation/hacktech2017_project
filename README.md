# hacktech2017_project
Handwritten Mathematical Computation

Are you tired of entering an equation in your phone? Well now you can handwrite it as if you are doing homework.

# How we built it:
The application was built with Python and is made up of major three parts; the user input, the data processing, and the output. The data that comes into the computer was sorted and we were able to make a list of coordinates which was used to draw the shape as it was coming in. The shape is then saved as an image and is ran through Google's Machine Learning API in order to create a text version of the shape. That text is then inputted into Wolfram Alpha's Full Results API which solved the equation. We took the outputs from both API's and the Image that was saved in order to put them in a new window which displays the handwriting, the Google API output, and the Wolfram Alpha output.

More info on our Devpost:
https://devpost.com/software/handwritten-mathematical-computation

# How to run this program:

pip install -r requirements.txt

login to Google Cloud (link below)

run server.py

Press Start button on http://127.0.0.1:8080/

run main.py

Draw!

have fun!

# Ref Link:
Synaptics:
http://www.synaptics.com/products/touch-controllers

GOOGLE CLOUD API:
https://cloud.google.com/sdk/gcloud/reference/beta/auth/application-default/login
https://cloud.google.com/sdk/downloads#windows

Wolfram Alpha API:
https://products.wolframalpha.com/api/

Pygame:
https://www.pygame.org/
