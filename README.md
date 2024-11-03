# Bluetooth-LED-control-program
Adafruit Bluetooth controller program to animate individually addressable LEDs
Bluetooth LED control program:

I designed all of the photo booths that our company currently sells.  Initially our products all ran on Windows software, and so the LED controller could plug directly into the USB port of the internal PC to control the animated patterns of the individually addressable LEDs.  As the industry shifted toward iPad controlled photobooths, we designed a booth enclosure specifically for the iPad, but we were no longer able to control the LEDs directly from the computer, so I found a small off-the-shelf bluetooth enabled circuit board that we could mount directly into the frame that would be able to control the individually addressable LED strips with simple Bluetooth commands from the iPad.  

I programmed the LED controls in circuitPY and have included the code.py file.  The program utilizes both prebuilt procedural animations as well as a custom image based option that allows images to be added as BMPs to the BMP folder which will then be played back as a sequence using each vertical line of pixels as individual frames that loop across the horizontal axis of the image file.

I am also including a link to the kickstarter page of this product.  In addition to designing the product, I shot most of the video materials, and created all of the animated product shots on the page (I am also in the pitch video along with the owner of the company and the product warehouse manager).

https://www.kickstarter.com/projects/laphotoparty/the-explorer-a-versatile-photo-booth-to-grow-with
