import time
from adafruit_crickit import crickit
from adafruit_seesaw.neopixel import NeoPixel

ss = crickit.seesaw
pot = crickit.SIGNAL2

ss.pin_mode(pot, ss.INPUT)
LDR = crickit.SIGNAL8
ss.pin_mode(LDR, ss.INPUT)

lowerThreshold = 300
higherThreshold = 500
    
num_pixels = 24
# The following line sets up a NeoPixel strip on Seesaw pin 20 for Feather
pixels = NeoPixel(crickit.seesaw, 20, num_pixels)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)
 
def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)

def fish():
    for i in range(num_pixels):
        if (i == pixelmOn):
            k = i-1
            if k<0:
                k=23
            pixels[i] = CYAN
            pixels[k] = BLUE
            print("pixel i = cyan")
            #k= BLANK
          #  k++
           # i++
        else:
            pixels[i] = BLANK
     #       time.sleep(wait)
            #print("pixel i = blank")
        pixels.show()
#        pixels[i] = color

def translate(value, leftMin, leftMax, rightMin, rightMax): #Adam Luchjenbroers, 12/8/2009
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
BLANK = (0, 0, 0)

while True:
    LDRValue = ss.analog_read(LDR) # read the LDR pin and set that reading to our LDRValue variable
    print(LDRValue) # print that value for our information
    potValue = ss.analog_read(pot)
    pixelmOn = round(translate(potValue, 0, 1023, 23, 0))
    print(pixelmOn)

    fish()
    
    if (LDRValue > higherThreshold):
      # this is where you specify what happens at a higher threshold
        print("Higher threshold exceeded")
        crickit.servo_1.angle = 180     # middle
      # this is where you specify what happens when you exceed a high threshold
    
    elif (LDRValue > lowerThreshold):
        print("Lower threshold exceeded")
        crickit.servo_1.angle = 0
      # this is where you specify what happens when you exceed a low threshold

    else:
        print("Below lower threshold")
        crickit.servo_1.angle = 180     # right
      # this is where you specify what happens when you're below both thresholds
      
    #time.sleep(0.25) # wait .25 seconds to slow down the interaction

#    print("chase")
 # Increase the number to slow down the color chase
#    color_chase(CYAN, 0.1)
#    color_chase(BLUE, 0.1)