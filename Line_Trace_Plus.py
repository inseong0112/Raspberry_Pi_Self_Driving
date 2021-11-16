import cv2
import numpy as np
from gpiozero import Motor

motorA = Motor(forward=5, backward=6)
motorB = Motor(forward=13, backward=16)
motorC = Motor(forward=19, backward=26)
motorD = Motor(forward=20, backward=21)

spd = 0.7

def motor_go():
    motorA.forward(spd)
    motorB.forward(spd)
    motorC.forward(spd)
    motorD.forward(spd)

def motor_right():
    motorA.forward(1)
    motorB.backward(1)
    motorC.forward(1)
    motorD.backward(1)

def motor_left():
    motorA.backward(1)
    motorB.forward(1)
    motorC.backward(1)
    motorD.forward(1)
    
def motor_back():
    motorA.backward(spd)
    motorB.backward(spd)
    motorC.backward(spd)
    motorD.backward(spd)

def motor_stop():
    motorA.stop()
    motorB.stop()
    motorC.stop()
    motorD.stop()
    
def fself():
    while(1):
        keyValue = cv2.waitKey(10)
        
        if keyValue == ord('d'):
            break
        elif keyValue == ord('s'):
            motor_stop()
            print("stop")
        elif keyValue == 82:
            print("up")
            motor_go()
        elif keyValue == 84:
            print("down")
            motor_back()
        elif keyValue == 81:
            print("left")
            motor_left()
        elif keyValue == 83:
            print("right")
            motor_right()

    
def main():
    camera = cv2.VideoCapture(0)
    camera.set(3,160) 
    camera.set(4,120)

    while( camera.isOpened() ):
        ret, frame = camera.read()
        frame = cv2.flip(frame,-1)
        cv2.imshow('normal',frame)
        keyValue = cv2.waitKey(10)
        crop_img =frame[60:120, 0:160]
        
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    
        blur = cv2.GaussianBlur(gray,(5,5),0)
        
        ret,thresh1 = cv2.threshold(blur,160,255,cv2.THRESH_BINARY_INV)
        
        mask = cv2.erode(thresh1, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cv2.imshow('mask',mask)
    
        contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
        
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            
            if cx >= 100 and cx <= 130:              
                print("Turn Right!")
                motor_left()
            elif cx >= 43 and cx <= 65:
                print("Turn Left!")
                motor_right()
            else:
                print("go")
                motor_go()
        
        if keyValue == ord('d'):
            fself()
        
        if cv2.waitKey(1) == ord('q'):
            motorA.stop()
            motorB.stop()
            motorC.stop()
            motorD.stop()
            break
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    
