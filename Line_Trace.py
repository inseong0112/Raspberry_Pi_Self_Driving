import cv2
import numpy as np

motorA = Motor(forward=5, backward=6)
motorB = Motor(forward=13, backward=16)
motorC = Motor(forward=19, backward=26)
motorD = Motor(forward=20, backward=21)

turn_spd = 0.5
spd = 1

def motor_go():
    motorA.forward(spd)
    motorB.forward(spd)
    motorC.forward(spd)
    motorD.forward(spd)

def motor_right():
    motorA.forward(spd)
    motorB.forward(turn_spd)
    motorC.forward(spd)
    motorD.forward(turn_spd)

def motor_left():
    motorA.forward(turn_spd)
    motorB.forward(spd)
    motorC.forward(turn_spd)
    motorD.forward(spd)

def main():
    camera = cv2.VideoCapture(0)
    camera.set(3,160) 
    camera.set(4,120)

    while( camera.isOpened() ):
        ret, frame = camera.read()
        frame = cv2.flip(frame,-1)
        cv2.imshow('normal',frame)
        
        crop_img =frame[60:120, 0:160]
        
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    
        blur = cv2.GaussianBlur(gray,(5,5),0)
        
        ret,thresh1 = cv2.threshold(blur,130,255,cv2.THRESH_BINARY_INV)
        
        mask = cv2.erode(thresh1, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cv2.imshow('mask',mask)
    
        contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
        
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            
            if cx >= 95 and cx <= 125:              
                print("Turn Left!")
                motor_left()
            elif cx >= 39 and cx <= 65:
                print("Turn Right")
                motor_right()
            else:
                print("go")
                motor_go()
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    
