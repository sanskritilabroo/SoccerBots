import pygame
import time
import socket
import sys
import math


def mapping(v, in_min, in_max, out_min, out_max):
    # Check that the value is at least in_min
    if v < in_min:
        v = in_min
    # Check that the value is at most in_max
    if v > in_max:
        v = in_max
    return int((v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def omni(axis_val):
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

    z = math.sqrt(x * x + y * y)
    theta = math.atan2(y,x) * 180 / math.pi #angle in radians to degrees

    if theta > 90:
         theta = 450 - theta
    else:
         theta = 90 - theta

    theta = (theta*math.pi)/180.0 #degrees to radians
    wheel_angles=[(90 * math.pi) / 180.0, (225 * math.pi) /180.0, (315 * math.pi) /180.0]

    for i in range(3):
         wv = z*math.sin(theta)*math.sin(wheel_angles[i])+z*math.cos(theta)*math.cos(wheel_angles[i])
         pwmb[i] = mapping(wv, -1, 1, -255, 255)
    pwmb[1]=-pwmb[1]

    return pwmb






pygame.init()
axis_data = None
button_data = None
hat_data = None
j = pygame.joystick
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

#CHECK ADDRESS THERE


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
flag = 0
pwmb = [0, 0, 0]
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                axis_data[event.axis] = round(event.value, 2)
            if event.type == pygame.JOYBUTTONDOWN:
                button_data[event.button] = True
            if event.type == pygame.JOYBUTTONUP:
                button_data[event.button] = False
            # if event.type == pygame.JOYHATMOTION:
            #     hat_data[event.hat] = event.value

        pwmb = [0, 0, 0]
        if 0 in axis_data.keys() and 1 in axis_data.keys():
            if not ((-0.04 <= axis_data[0] <= 0.04) and (-0.04 <= axis_data[1] <= 0.04)):
                pwmb = omni(axis_data)
            else:
                pwmb = [0, 0, 0]
        if button_data[10]==True: #right
            pwmb=[255,-255,-255]
        if button_data[9]==True: #left
            pwmb=[-255,255,255]
        if button_data[0] == 1:
            sys.exit(0)

        # if button_data[2]==True and flag==0:
        #     flag=1
        #     pwmb[0]=1   #square

        # if button_data[2]==False:
        #     flag=0    

        # if button_data[1]==True and flag==0:
        #     flag=1
        #     pwmb[0]=-1     #circle

        # if button_data[1]==False:
        #     flag=0   

        print(pwmb)
        #s.send(bytes(f"{','.join(map(str, pwmb))}\n", "UTF-8"))
        time.sleep(0.05)  # increase


except KeyboardInterrupt:
    print("Interrupted")
    # s.close()