import RPi.GPIO as gp  
from time import sleep 
import time 
import argparse

class Bed:
    def __init__(self,user, type, dir, c_time):
        self.user = user
        self.type = type
        self.dir = dir
        self.c_time = c_time 
    
    def __str__(self):
        return "{}_bed / type: {}, direction: {}, time: {}".format(self.user, self.type, self.dir, self.c_time)

    def __repr__(self):
        return "{}_bed / type: {}, direction: {}, time: {}".format(self.user, self.type, self.dir, self.c_time)
    
    #setting-led
    
    #setting-actuater
    def gpio_setup(self,led):
        gp.setmode(gp.BOARD)
        gp.setup(12,gp.OUT)
        gp.setup(32,gp.OUT)
        gp.setup(11,gp.OUT)
        gp.setup(31,gp.OUT)

        pwm_up1 = gp.PWM(32,50)
        pwm_up2 = gp.PWM(31,50)
        pwm_down1 = gp.PWM(12,50)  
        pwm_down2 = gp.PWM(11,50) 

        gp.setmode(gp.BOARD)


        if self.type == "head":
            pwm_down = pwm_down1
            pwm_up = pwm_up1

        elif self.type == "body":
            pwm_down = pwm_down2
            pwm_up = pwm_up2

        elif self.type == "both":
            pwm_down1.start(0)  
            pwm_up1.start(0)
            pwm_down2.start(0)  
            pwm_up2.start(0)
            return (pwm_up1, pwm_down1, pwm_up2, pwm_down2)
            
        else: 
            print("error")
            led("red")

        pwm_down.start(0)  
        pwm_up.start(0)

        return(pwm_up, pwm_down, 0, 0)

    #control according to direction,time
    def control(self,led):

        try:
            pwm_up, pwm_down, _ , _ = self.gpio_setup(led)
            #up
            led("off")
            if self.dir == "up":
                print("up")
                pwm = pwm_up

            elif self.dir == "down":
                print("down")
                pwm = pwm_down

            j = 0
            led("green")
            while True:
                pwm.ChangeDutyCycle(j)
                sleep(1)
                if j >= self.c_time:
                    break
                j += 1
            led("blue")
            pwm.ChangeDutyCycle(0) 
            pwm.stop()
        except:
            print("error1")
            led("red")
            

    def control_both(self,led):
        try:
            pwm_up, pwm_down, pwm_up2, pwm_down2 = self.gpio_setup(led)
            if self.dir == "up":
                print("up")
                pwm = pwm_up
                pwm1 = pwm_up2

            elif self.dir == "down":
                print("down")
                pwm = pwm_down
                pwm1 = pwm_down2

            j = 0
            led("green")
            while True:
                pwm.ChangeDutyCycle(j)
                pwm1.ChangeDutyCycle(j)
                sleep(1)
                if j >= self.c_time:
                    break
                j += 1
            led("blue")
            pwm.ChangeDutyCycle(0) 
            pwm1.ChangeDutyCycle(0) 
            pwm.stop()
            pwm1.stop()
        except:
            print("error2")
            led("red")    

    #LED 제어함수
    def led_on(self,color):
        gp.setmode(gp.BOARD)

        RED_PIN   = 13
        GREEN_PIN = 15
        BLUE_PIN  = 18

        gp.setwarnings(False)

        gp.setup(RED_PIN, gp.OUT)
        gp.setup(GREEN_PIN, gp.OUT)
        gp.setup(BLUE_PIN, gp.OUT)

        
        if color == "red":
            gp.output(RED_PIN, gp.HIGH)

        elif color == "green":
            gp.output(GREEN_PIN, gp.HIGH)

        elif color == "blue":
            gp.output(BLUE_PIN, gp.HIGH)

        elif color == "yellow":
            gp.output(RED_PIN, gp.HIGH)
            gp.output(GREEN_PIN, gp.HIGH)

        elif color == "white":
            gp.output(RED_PIN, gp.HIGH)
            gp.output(GREEN_PIN, gp.HIGH)
            gp.output(BLUE_PIN, gp.HIGH)

        elif color == "off":
            gp.output(RED_PIN, gp.LOW)
            gp.output(GREEN_PIN, gp.LOW)
            gp.output(BLUE_PIN, gp.LOW)
        else:
            print("----------------error")

    #LED반짝이 여부
    def twinkle(self,color):
        # if twinkle_input =="o":
        self.led_on(color)
        time.sleep(0.5)
        self.led_on("off")
        time.sleep(0.5)
        # else:
        #     self.led_on(color)
    
    #실행함수
    def run(self):
        led = self.led_on
        # led = self.twinkle 반짝이 하고싶으면 이걸로 바꾸면 됨
        if self.type == "both":
            self.control_both(led)
        else: self.control(led)

        gp.cleanup()


if __name__=='__main__':
    
    try:
        parser = argparse.ArgumentParser(description="Options")

        parser.add_argument('-t','--type', required = True, help = 'Choose the type (head/body/both)')
        parser.add_argument('-d','--direction', required = True, help = 'Choose the direction(up/down)')
        parser.add_argument('-c','--c_time', required = True, type = int, help = 'How much?')
        
        args = parser.parse_args()
        
        type = args.type
        dir = args.direction
        c_time = args.c_time

        # type = input("Choose the type (head/body/both): ")
        # dir = input("Choose the direction(up/down): ")
        # c_time = int(input("How much?: "))

        user1 = Bed('sujin',type,dir,c_time)
        user1.run()
    except:
        print("error error")
