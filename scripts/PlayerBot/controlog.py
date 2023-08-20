import pygame
import time
import socket
import sys
import math


''' MAPPING FUNCTION STARTS'''

def mapping(v, in_min, in_max, out_min, out_max):
    # Check that the value is at least in_min
    if v < in_min:
        v = in_min
    # Check that the value is at most in_max
    if v > in_max:
        v = in_max
    return int((v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def motorvals(axis_val):
    pwmb = [0, 0, 0]
    if 0 in axis_val.keys() and 1 in axis_val.keys():
        x = round(axis_val[0], 2)
        y = round(axis_val[1], 2)
        if (-0.05 <= x <= 0.05) and (-0.05 <= y <= 0.05):
            pwmb = [0, 0, 0]
            return pwmb
    else:
        pwmb = [0, 0, 0]
        return pwmb
    

    z = math.sqrt(x * x + y * y) #hypoteneuse
    rad = math.acos(math.fabs(x) / z) #angle in radians, performs cos inverse
    angle = rad * 180 / math.pi #angle in degrees

    tcoeff = -1 + (angle / 90) * 2
    # turn = tcoeff * math.fabs(math.fabs(y) - math.fabs(x))
    # turn = round(turn * 100, 0) / 100

    mov = max(math.fabs(y), math.fabs(x)) # And max of y or x is the movement
    turn = tcoeff * mov

    if (x >= 0 and y >= 0) or (x < 0 and y < 0): # First and third quadrant
        rawRight = mov
        rawLeft = turn
    else:
        rawLeft = mov
        rawRight = turn

    # Reverse polarity
    if y < 0:
        rawLeft = 0 - rawLeft
        rawRight = 0 - rawRight
    pwmb[0] = -mapping(rawLeft, -1, 1, -255, 255)
    pwmb[1] = -mapping(rawRight, -1, 1, -255, 255)
    return pwmb


''' PYGAME CONTROL STARTS'''

pygame.init() #initializing pygame

axis_data = None
button_data = None
hat_data = None

j = pygame.joystick #initializing joystick
j.init()
control = j.Joystick(0)
control.init()


''' SOCKET CONNECTION STARTS'''

#"84:CC:A8:7A:38:C2""7C:9E:BD:F4:C2:7E"
#addres="9C:9C:1F:C5:0E:DE"
#channel = 1
#s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, 
#socket.BTPROTO_RFCOMM)
#s.connect((addres,channel))
#btdiscovery -s"%sc% -%sn%"



''' UNNECESSARY FOR PLAY (WE ALSO DO NOT NEED HATS) '''
# if(j.get_count()==0):
#     print("No Controller")
# else:
#     print("Controller present")
# print(control.get_name())
# print(control.get_numaxes())
# print(control.get_numbuttons())




if not axis_data:
    axis_data = {}

if not button_data:
    button_data = {}
    for i in range(control.get_numbuttons()):
        button_data[i] = False



# if not hat_data:
#     hat_data = {}
#     for i in range(control.get_numhats()):
#         hat_data[i] = (0, 0)


flag=0
pwmb=[0,0,0]
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                axis_data[event.axis] = round(event.value, 2)
            if event.type == pygame.JOYBUTTONDOWN: #button pressed
                button_data[event.button] = True
            if event.type == pygame.JOYBUTTONUP: #button released
                button_data[event.button] = False
            # if event.type == pygame.JOYHATMOTION:
            
            #     hat_data[event.hat] = event.value

        pwmb=[0,0,0]   
        if 0 in axis_data.keys() and 1 in axis_data.keys():
            if not((-0.04 <= axis_data[0] <= 0.04) and (-0.04 <= axis_data[1] <= 0.04)):
                pwmb=motorvals(axis_data)
            else:
                pwmb=[0,0,0]


        if button_data[10]==True: #right bumper
            pwmb=[255,-255,0]
        if button_data[9]==True: #left bumper
            pwmb=[-255,255,0]
        if button_data[11]==True: #up dpad
            pwmb=[255,255,0]
        if button_data[12]==True: #down dpad
            pwmb=[-255,-255,0] 

        if button_data[0] == 1:
            sys.exit(0) #exits if you press x
 
        if button_data[2]==True and flag==0:
            flag=1
            pwmb[2]=1   #square
        
        if button_data[2]==False:
            flag=0 

        #if button_data[2]==False:
         #   flag=0    

        if button_data[1]==True and flag==0:
            flag=1
            pwmb[2]=-1     #circle

        if button_data[1]==False:
            flag=0   


        print(pwmb)
       # s.send(bytes(f"{','.join(map(str, pwmb))}\n", "UTF-8"))
        time.sleep(0.01)#increase


except KeyboardInterrupt:
    print("Interrupted")
    # s.close()