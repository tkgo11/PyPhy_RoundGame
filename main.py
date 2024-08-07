from machine import Pin, SoftI2C
import ssd1306
import framebuf
from neopixel import NeoPixel
from time import sleep
import ble_library
import bluetooth
from random import randint

i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128,64,i2c)

pin = Pin(14, Pin.OUT)
np = NeoPixel(pin, 12)


ble = bluetooth.BLE()
p = ble_library.BLESimplePeripheral(ble, "Game")

#초기화
for i in range(0,12):
    np[i] = (0,0,0)
np.write()

#변수 지정
isClockWise = bool(randint(0,1))

isGameStarted = False
isPoint = False

speed = 0.25
rad = 3
pos_list = list()
score = 0

display.fill(0)
display.text('Ready', 48, 28, 1)
display.show()
      
print(np)
def on_rx(v):
    global isTriggered, isGameStarted, pos_list, isPoint, score, speed, isClockWise
    if v == "START_GAME" and not isGameStarted:
        speed = 0.5
        pos = randint(0,12)
        pos_list = list()
        pos_list.extend(range(int(pos-rad/2), int(pos+rad/2)))
        if len(pos_list)<=2:
            pos = randint(0,12)
            pos_list = list()
            pos_list.extend(range(int(pos-rad/2), int(pos+rad/2)))
        if len(pos_list)<=2:
            pos = randint(0,12)
            pos_list = list()
            pos_list.extend(range(int(pos-rad/2), int(pos+rad/2)))
        if len(pos_list)<=2:
            pos = randint(0,12)
            pos_list = list()
            pos_list.extend(range(int(pos-rad/2), int(pos+rad/2)))
        #print(pos_list)
        #if len([i for i in pos_list if i < 0]) > 0:
            #del pos_list[len([i for i in pos_list if i < 0]):]
            #pos_list.insert(0, i for i in pos_list if i < 0)
        #elif len([i for i in pos_list if i > 11]) > 0:
            #del pos_list[-len([i for i in pos_list if i < 0]):]
            #pos_list.append(i for i in pos_list if i < 0)
        #print(pos_list)
        isGameStarted = True

    if v == "TRI":
        if isPoint == True:
            display.fill(0)
            display.text("+1pt!", 48, 28, 1)
            display.text(str(score), 0, 0, 1)
            score += 1
            isPoint = False
            speed -= speed / 5
        elif isPoint == False:
            display.fill(0)
            display.text("GameOver", 38, 28, 1)
            display.text(str(score), 0, 0, 1)
            isGameStarted = False
            speed = 0
        isClockWise = not isClockWise
        display.show()
        
p.on_write(on_rx)

while True:
    if isGameStarted:
        display.fill(0)
        display.text('Start', 48, 28, 1)
        display.text(str(score), 0, 0, 1)
        display.show()
        if isClockWise:
            for i in range(0, 12, 1):
                isPoint = False
                for j in range(0, 12):
                    if j == i:
                        np[j] = (255,255,255)
                        if j in pos_list:
                            isPoint = True
                    elif j in pos_list:
                        np[j] = (255,0,0)
                    else:
                        np[j] = (0,0,0)
                np.write()
                sleep(speed)
        else:
            for i in range(11, -1, -1):
                isPoint = False
                for j in range(0, 12):
                    if j==i:
                        np[j] = (255,255,255)
                        if j in pos_list:
                            isPoint = True
                    elif j in pos_list:
                        np[j] = (255,0,0)
                    else:
                        np[j] = (0,0,0)
                np.write()
                sleep(speed)
    else:
        for i in range(0, 2):
            for j in range(0, 12):
                if j%2==0:
                    if i:
                        np[j] = (255,255,255)
                    else:
                        np[j] = (0,0,0)
                else:
                    if i:
                        np[j] = (0,0,0)
                    else:
                        np[j] = (255,255,255)
            np.write()
            sleep(0.25)
