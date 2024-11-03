"""
NeoPixel Animator code for ItsyBitsy nRF52840 NeoPixel Animation and Color Remote Control.
"""

import board
import neopixel
import neosprite
import time
import gc
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.group import AnimationGroup

import adafruit_led_animation.color as color
from neopixel_write import neopixel_write

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket

# The number of NeoPixels in the externally attached strip
# If using two strips connected to the same pin, count only one strip forthisnumber!
STRIP_PIXEL_NUMBER = 99

# Setup for comet animation
COMET_SPEED = 0.05  # Lower numbers increase the animation speed
STRIP_COMET_TAIL_LENGTH = 10  # The length of the comet on the NeoPixel strip
STRIP_COMET_BOUNCE = True  # Set to False to stop comet from "bouncing" on NeoPixel strip

# Create the NeoPixel strip
strip_pixels = neopixel.NeoPixel(board.D5, STRIP_PIXEL_NUMBER, brightness=0.7, auto_write=True)

# Setup BLE connection
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

solid_color = AnimationGroup(Solid(strip_pixels, color=(15, 100, 90)))
solid_white = AnimationGroup(Solid(strip_pixels, color=(120, 100, 90)))
animate_pulse = AnimationGroup(
    Pulse(strip_pixels, speed=.001, color=(150, 15, 30), period=5))
animate_chase = AnimationGroup(
    Chase(strip_pixels, speed=.03, color=(10, 100, 50), size=3, spacing=4, reverse=False))
animate_rainbow = AnimationGroup(
    RainbowChase(strip_pixels, speed=.03, size=3, spacing=4, reverse=False, step=8))
animation_color = (15, 100, 90)

while True:
    ble.start_advertising(advertisement)  # Start advertising.
    was_connected = False
    solid_white.animate()
    print("things")
    while not was_connected or ble.connected:
        if ble.connected:  # If BLE is connected...
            was_connected = True
            solid_white.animate()
            if uart.in_waiting:  # Check to see if any data is available from the Remote Control.
                try:
                    packet = Packet.from_stream(uart)  # Create the packet object.
                except ValueError:
                    continue
                if isinstance(packet, ColorPacket):  # If the packet is color packet...
                    print("Color:", packet.color)
                    gc.collect()
                    print(gc.mem_free())
                    animation_color = packet.color
                    # Keep track of the current color...
                elif isinstance(packet, ButtonPacket):  # If the packet is a button packet...
                    buttons = True
                    while buttons:
                        print("buttons are running")
                        print(gc.mem_free())
                        if not ble.connected:
                            print("buttonsDisconnect")
                            buttons = False
                            break
                        elif packet.pressed:  # If the buttons on the Remote Control are pressed...
                            if packet.button == ButtonPacket.RIGHT:  # If button A is pressed...
                                message = False
                                timeout = 1
                                try:
                                    sprite = neosprite.BmpSprite.open('/bmps/Flash.bmp')
                                except MemoryError:
                                    gc.collect()
                                    print("memoryError")
                                    buttons = False
                                    break
                                sprite.size = [1, 99]
                                gc.collect()
                                while not message:
                                    for xPos in range(0, 1, 1):
                                        sprite.offset = [xPos, 0]
                                        sprite.fillBuffer(strip_pixels.buf)
                                        neopixel_write(strip_pixels.pin, strip_pixels.buf)
                                        time.sleep(.01)
                                        if not ble.connected:
                                            print("messageDisconnect")
                                            message = True
                                            buttons = False
                                            break
                                        elif timeout > 300:
                                            print("timer exceeded")
                                            message = True
                                            buttons = False
                                            break
                                        elif uart.in_waiting:
                                            try:
                                                packet = Packet.from_stream(uart)  # Create the packet object.
                                            except ValueError:
                                                continue
                                            if isinstance(packet, ButtonPacket):
                                                if packet.button == ButtonPacket.RIGHT:
                                                    continue
                                                else:
                                                    del sprite
                                                    gc.collect()
                                                    message = True
                                                    break
                                            else:
                                                del sprite
                                                gc.collect()
                                                message = True
                                                buttons = False
                                                break
                                        else:
                                            timeout += 1
                            elif packet.button == ButtonPacket.LEFT:  # If button B is pressed...
                                message = False
                                try:
                                    sprite = neosprite.BmpSprite.open('/bmps/third.bmp')
                                except MemoryError:
                                    gc.collect()
                                    print("memoryError")
                                    buttons = False
                                    break
                                sprite.size = [1, 99]
                                gc.collect()
                                while not message:
                                    for xPos in range(0, 39, 1):
                                        sprite.offset = [xPos, 0]
                                        sprite.fillBuffer(strip_pixels.buf)
                                        neopixel_write(strip_pixels.pin, strip_pixels.buf)
                                        time.sleep(.01)
                                        if not ble.connected:
                                            print("messageDisconnect")
                                            message = True
                                            buttons = False
                                            break
                                        elif uart.in_waiting:
                                            try:
                                                packet = Packet.from_stream(uart)  # Create the packet object.
                                            except ValueError:
                                                continue
                                            if isinstance(packet, ButtonPacket):
                                                if packet.button == ButtonPacket.LEFT:
                                                    continue
                                                else:
                                                    del sprite
                                                    gc.collect()
                                                    message = True
                                                    break
                                            else:
                                                del sprite
                                                gc.collect()
                                                message = True
                                                buttons = False
                                                break
                            elif packet.button == ButtonPacket.UP:
                                try:
                                    sprite = neosprite.BmpSprite.open('/bmps/first.bmp')
                                except MemoryError:
                                    gc.collect()
                                    print("memoryError")
                                    buttons = False
                                    break
                                sprite.size = [1, 99]
                                gc.collect()
                                message = False
                                while not message:
                                    for xPos in range(0, 39, 1):
                                        sprite.offset = [xPos, 0]
                                        sprite.fillBuffer(strip_pixels.buf)
                                        neopixel_write(strip_pixels.pin, strip_pixels.buf)
                                        time.sleep(.03)
                                        if not ble.connected:
                                            print("messageDisconnect")
                                            message = True
                                            buttons = False
                                            break
                                        elif uart.in_waiting:
                                            try:
                                                packet = Packet.from_stream(uart)  # Create the packet object.
                                            except ValueError:
                                                continue
                                            if isinstance(packet, ButtonPacket):
                                                if packet.button == ButtonPacket.UP:
                                                    continue
                                                else:
                                                    del sprite
                                                    gc.collect()
                                                    message = True
                                                    break
                                            else:
                                                del sprite
                                                gc.collect()
                                                message = True
                                                buttons = False
                                                break
                            elif packet.button == ButtonPacket.DOWN:
                                try:
                                    sprite = neosprite.BmpSprite.open('/bmps/second.bmp')
                                except MemoryError:
                                    gc.collect()
                                    print("memoryError")
                                    buttons = False
                                    break
                                sprite.size = [1, 99]
                                gc.collect()
                                message = False
                                while not message:
                                    for xPos in range(0, 42, 1):
                                        sprite.offset = [xPos, 0]
                                        sprite.fillBuffer(strip_pixels.buf)
                                        neopixel_write(strip_pixels.pin, strip_pixels.buf)
                                        time.sleep(.01)
                                        if not ble.connected:
                                            print("messageDisconnect")
                                            message = True
                                            buttons = False
                                            break
                                        elif uart.in_waiting:
                                            try:
                                                packet = Packet.from_stream(uart)  # Create the packet object.
                                            except ValueError:
                                                continue
                                            if isinstance(packet, ButtonPacket):
                                                if packet.button == ButtonPacket.DOWN:
                                                    continue
                                                else:
                                                    del sprite
                                                    gc.collect()
                                                    message = True
                                                    break
                                            else:
                                                del sprite
                                                gc.collect()
                                                message = True
                                                buttons = False
                                                break
                            elif packet.button == ButtonPacket.BUTTON_1:
                                gc.collect()
                                message = False
                                while not message:
                                    solid_color.animate()
                                    solid_color.color = animation_color
                                    if not ble.connected:
                                            print("messageDisconnect")
                                            message = True
                                            buttons = False
                                            break
                                    elif uart.in_waiting:
                                        try:
                                            packet = Packet.from_stream(uart)  # Create the packet object.
                                        except ValueError:
                                            continue
                                        if isinstance(packet, ButtonPacket):
                                            if packet.button == ButtonPacket.BUTTON_1:
                                                continue
                                            else:
                                                gc.collect()
                                                message = True
                                                break
                                        elif isinstance(packet, ColorPacket):  # If the packet is color packet...
                                                gc.collect()
                                                print(gc.mem_free())
                                                animation_color = packet.color
                                                print(animation_color, "solid")
                                                continue
                                        else:
                                            gc.collect()
                                            message = True
                                            buttons = False
                                            break
                            elif packet.button == ButtonPacket.BUTTON_2:
                                gc.collect()
                                message = False
                                while not message:
                                    animate_chase.animate()
                                    animate_chase.color = animation_color
                                    if not ble.connected:
                                            print("messageDisconnect")
                                            message = True
                                            buttons = False
                                            break
                                    elif uart.in_waiting:
                                        try:
                                            packet = Packet.from_stream(uart)  # Create the packet object.
                                        except ValueError:
                                            continue
                                        if isinstance(packet, ButtonPacket):
                                            if packet.button == ButtonPacket.BUTTON_2:
                                                continue
                                            else:
                                                gc.collect()
                                                message = True
                                                break
                                        elif isinstance(packet, ColorPacket):  # If the packet is color packet...
                                            gc.collect()
                                            print(gc.mem_free())
                                            animation_color = packet.color
                                            print(animation_color, "chase")
                                            continue
                                        else:
                                            gc.collect()
                                            message = True
                                            buttons = False
                                            break
                            elif packet.button == ButtonPacket.BUTTON_3:
                                gc.collect()
                                message = False
                                while not message:
                                    animate_pulse.animate()
                                    animate_pulse.color = animation_color
                                    if not ble.connected:
                                        print("messageDisconnect")
                                        message = True
                                        buttons = False
                                        break
                                    elif uart.in_waiting:
                                        try:
                                            packet = Packet.from_stream(uart)  # Create the packet object.
                                        except ValueError:
                                            continue
                                        if isinstance(packet, ButtonPacket):
                                            if packet.button == ButtonPacket.BUTTON_3:
                                                continue
                                            else:
                                                gc.collect()
                                                message = True
                                                break
                                        elif isinstance(packet, ColorPacket):  # If the packet is color packet...
                                                gc.collect()
                                                print(gc.mem_free())
                                                animation_color = packet.color
                                                print(animation_color, "pulse")
                                                continue
                                        else:
                                            gc.collect()
                                            message = True
                                            buttons = False
                                            break
                            elif packet.button == ButtonPacket.BUTTON_4:
                                gc.collect()
                                message = False
                                while not message:
                                    animate_rainbow.animate()
                                    if not ble.connected:
                                        print("messageDisconnect")
                                        message = True
                                        buttons = False
                                        break
                                    elif uart.in_waiting:
                                        try:
                                            packet = Packet.from_stream(uart)  # Create the packet object.
                                        except ValueError:
                                            continue
                                        if isinstance(packet, ButtonPacket):
                                            if packet.button == ButtonPacket.BUTTON_4:
                                                continue
                                            else:
                                                gc.collect()
                                                message = True
                                                break
                                        else:
                                            gc.collect()
                                            message = True
                                            buttons = False
                                            break
                            else:
                                gc.collect
                                message = True
                                buttons = False
                                break
                        else:
                            gc.collect()
                            print(gc.mem_free())
                            print("moronTest")
                            buttons = False
