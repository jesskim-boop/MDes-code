import picamera     #camera library
import pygame as pg #audio library
import os           #communicate with os/command line
from adafruit_seesaw.neopixel import NeoPixel

from google.cloud import vision  #gcp vision library
from time import sleep
from adafruit_crickit import crickit
import time


import signal
import sys
import re           #regular expression lib for string searches!
import subprocess

ss = crickit.seesaw
BUTTON_1 = crickit.SIGNAL1  # button #1 connected to signal port 1 & ground

ss.pin_mode(BUTTON_1, ss.INPUT_PULLUP)

num_pixels = 30

pixels = NeoPixel(crickit.seesaw, 20, num_pixels)
ss.pin_mode(BUTTON_1, ss.INPUT_PULLUP)

WHITE = (255,255,255)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
BLANK = (0, 0, 0)

#set up your GCP credentials - replace the " " in the following line with your .json file and path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="TDF-VoiceVision.json"

# this line connects to Google Cloud Vision! 
client = vision.ImageAnnotatorClient()

# global variable for our image file - to be captured soon!
image = 'image.jpg'

def espeak(text: str, pitch: int=50) -> int:
    """ Use espeak to convert text to speech. """
    return subprocess.run(['espeak', f'-p {pitch}', text]).returncode

def takephoto(camera):
    
    # this triggers an on-screen preview, so you know what you're photographing!
    camera.start_preview() 
    sleep(.5)                   #give it a pause so you can adjust if needed
    camera.capture('image.jpg') #save the image
    camera.stop_preview()       #stop the preview
        

def colorChange(color):
    if color < 0 or color > 255:
        return(BLANK)
    elif color > 0:
        return(RED)
    elif color < 50:
        return(YELLOW)
    elif color < 100:
        return(CYAN)
    elif color < 150:
        return(GREEN)
    elif color < 200:
        return(PURPLE)
    elif color < 230:
        return(BLUE)
    elif color < 255:
        return (WHITE)
        
def image_labeling(image):
    #this function sends your image to google cloud using the
    #label_detection method, collects a response, and parses that
    #response for all of the label descriptions collected - that is,
    #the AI's guesses at what is contained in the image.
    #each of these labels, identified as .description, are combined into
    #a single string label_text.
    #this time we'll be triggering different sounds - a bark or a meow! -
    #depending on what's in the image. 
    
    string1 = "fruit"
    string2 = "Spring onion"
    string3= "fish"
    
    sound1 = "voicemail.wav"
    sound2 = "dishes.wav"
    sound3 = "taiko.wav"
    
    response = client.label_detection(image=image)
    labels = response.label_annotations
       
    label_text = ""
    
    #this next block of code parses the various labels returned by google,
    #extracts the text descriptions, and combines them into a single string. 
    for label in labels:
        label_text += ''.join([label.description, " "])
    
    #if labels are identified, send the sound files, search strings, and label
    #text to speaker_out()
    if label_text:
        print('image_labeling(): {}'.format(label_text))
        speaker_out(sound1, sound2, sound3, label_text, string1, string2, string3)
        if ss.digital_read(BUTTON_1):
            color = color + 50
            print("Button 1 pressed")
            pixels.fill(colorChange(color))
            pixels.show()
        
        else:
            print("Button 1 NOT pressed")
            pixels.fill(BLANK)
            pixels.show()
        
    
def speaker_out(sound1, sound2, sound3, text, string1, string2, string3):
    
    #this function plays sound1 
    #if string1 is found in the text descriptions returned
    #using regular expressions as in motor_turn().
    #similarly, sound 2 is played if string 2 is detected.
    #the pygame library is used to playback audio.
    #please note, if you're changing out sound files, 16-bit
    #.wav files are needed, otherwise you risk getting some
    #underrun errors. 
    
#    print(text)
    
    if re.search(string1, text, re.IGNORECASE):
       # espeak("hand")
        print("fruit")
        pg.mixer.music.load("Papa_Grandma.wav")
        pg.mixer.play("Papa_Grandma.wav")
        color = 25

   #     pg.mixer.music.load(sound1) #pygame - load the sound file
 #       pg.mixer.music.play()       #pygame - play the sound file
    elif re.search(string2, text, re.IGNORECASE):
        #espeak("spring onion")
        print("said spring onion")
        pg.mixer.music.load(sound2)
        color = 101
        
        #pg.mixer.music.play()
    elif re.search(string3, text, re.IGNORECASE):
        #espeak("fruit")
        print("said fish")
        color = 201
        if ss.digital_read(BUTTON_1):
            color = color + 50
            print("Button 1 pressed")
            pixels.fill(colorChange(color))
            pixels.show()
        
        else:
            print("Button 1 NOT pressed")
            pixels.fill(BLANK)
            pixels.show()

    #
 
def main():
    
    #generate a camera object for the takephoto function to
    #work with
    camera = picamera.PiCamera()
    
    #setup our pygame mixer to play audio in subsequent stages
    pg.init()
    pg.mixer.init()
    
    #this while loop lets the script run until you ctrl+c (command line)
    #or press 'stop' (Thonny IDE)
    while True:
 
        takephoto(camera) # First take a picture
        """Run a label request on a single image"""

        with open('image.jpg', 'rb') as image_file:
            #read the image file
            content = image_file.read()
            #convert the image file to a GCP Vision-friendly type
            image = vision.Image(content=content)
            #ocr_handwriting(image)
            p =image_labeling(image)
            print(p)
            time.sleep(0.1)        
        
if __name__ == '__main__':
        main()    
