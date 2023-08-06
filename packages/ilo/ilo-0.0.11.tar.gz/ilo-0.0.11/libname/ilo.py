# This python scrip is the libery for python
# SIMON LE BERRE
# 12/12/2021
# pip install ilo
version = '0.0.10'
#-----------------------------------------------------------------------------

print("ilo robot library version ", version)
print("For any help or support contact us on our website, ilorobot.com ")
print(" ")

#-----------------------------------------------------------------------------
import socket,time,keyboard #,sys

#-----------------------------------------------------------------------------
'''
if 'ilo' in sys.modules:
    print ('ilo library is already imported')
else:    
    print('ilo library is importing ...')
'''    
global IP,Port,s,preview_stop,connect
IP = '192.168.4.1'
preview_stop = True

#-------------------------------------------------------------------------
def info():
    print("Ilo robot is an education robot controlable by direct python command")
    print("To know every fonction available with ilo,  use ilo.list_function() command")
    print("You are using the version ", version)

def list_function():
    print("info()                                        -> print info about ilorobot")
    print(" ")
    print("connection()                                  -> connection your machine to ilorobot")
    print(" ")
    print("step(direction)                               -> move by step ilorobot with selected direction during 2 seconds")
    print("                                                 direction is a string and should be (front, back, left, right, rot_trigo or rot_clock)")
    print(" ")
    print("move(direction, speed, time)                  -> move ilorobot with selected direction speed and time control")
    print("                                                 direction is a string and should be (front, back, left or right)")
    print("                                                 speed is an integer from 0 to 100 as a pourcentage ")
    print(" ")
    print("direct_contol(axial, radial, rotation, stop)) -> control ilorobot with full control ")
    print("                                                 axial, radial and roation are 3 integer from 0 to 255")
    print("                                                 value from 0 to 127 are negative, value from 127 to 255 are positve")
    print("                                                 stop is a boolean value, to don't stop after the command the robot use stop==False")                                
    print(" ")
    print("calculatrice(ilo_calcul)                      -> ilo will execute your calculus, ilo_calcul is a string")
    print("                                                 example of calcul: '3+2-1.5' ")
    print(" ")
    print("list_order(ilo_list)                          -> ilo will execute a list of displacment define my your ilo_list")
    print("                                                 example of list ['front', 'left', 'front', 'rot_trigo', 'back'] ")
    print("                                                 value of ilo_list are a string")
    print(" ")
    print("game()                                        -> control ilo using arrow or numb pad of your keyboard")
    print("                                                 avaible keyboard touch: 8,2,4,6,1,3   space = stop    esc = quit")
    print(" ")
    
    print("detection()                                   -> no yet available, coming soon on ilo...    ")

def socket_send(val,size):

    global s, IP, Port
    
    s = socket.socket()
    s.connect((IP, Port))
    
    if size == False:   
        msg = str(val[0])
        s.send(msg.encode())
        time.sleep(0.03)
    else:
        msg = str(len(val))
        s.send(msg.encode())
        time.sleep(0.03)
        for i in range (len(val)):
            s = socket.socket()
            s.connect((IP, Port))
            msg = str(val[i])
            s.send(msg.encode())
            time.sleep(0.03)

#-------------------------------------------------------------------------
try:
    socket_send([88],False)
    connect = True
except:
    connect = False
#------------------------------------------- ------------------------------
def connection():
    
    global IP,Port,connect, preview_stop
    preview_stop = True
    
    if connect == True:
        print('You are already connected to ilo, you can comment this command line')
        return None
    
    else:
        print('Connecting...')
        try:
            Port = 6000
            ping = socket.socket()
            ping.connect((IP, Port))         
            deviceIP = ping.getsockname()[0]     # IP of the machine
            #print('deviceIP', deviceIP)
            msg="0"
            ping.send(msg.encode())
            ping.close()
    
            inform = socket.socket()
            inform.bind((deviceIP, Port)) 
    
            while(1):
                inform.listen(5)
                client,addr = inform.accept()
                Port = int(client.recv(1024))
                #print('New Port of communication: ', Port)
                if Port != 0:
                    inform.close()
                    break
    
            time.sleep(1)
    
            s = socket.socket() 
            msg="0"
            s.connect((IP, Port))
            s.send(msg.encode())
            print('Connected to ilo')
            time.sleep(1)
        except:
            print("Error connection: you have to be connect to the ilo wifi network")
            print(" --> If the disfonction continu, switch off and switch on ilo")

def step(direction):
    global preview_stop
    preview_stop = True
    
    if isinstance(direction, str) == False:
        print ('direction should be an string as front, back, left, rot_trigo, rot_clock')
        return None
    
    socket_send([88],False)
    socket_send([88],False)
    
    socket_send([1],False)
    if direction == 'front':
        socket_send([8],False)
    elif direction == 'back':
        socket_send([2],False)
    elif direction == 'left':
        socket_send([4],False)
    elif direction == 'right':
        socket_send([6],False)
    elif direction == 'rot_trigo':
        socket_send([1],False)
    elif direction == 'rot_clock':
        socket_send([3],False)
    else:
        print('direction name is not correct')
    
    time.sleep(2)                  #time for ilo displacement
    socket_send([88],False)

def correction_command(list_course):
    
    if int(list_course[0]) >= 100:
        list_course[0] = str(list_course[0])   
    elif 100 > int(list_course[0]) >= 10:
        list_course[0] = str('0') + str(list_course[0])
    elif 10 > int(list_course[0]) >=1:
        list_course[0] = str('00') + str(list_course[0])
    else:
        list_course[0] = str('000')

    if int(list_course[1]) >= 100:
        list_course[1] = str(list_course[1])     
    elif 100 > int(list_course[1]) >= 10:
        list_course[1] = str('0') + str(list_course[1])
    elif 10 > int(list_course[1]) >=1:
        list_course[1] = str('00') + str(list_course[1])
    else:
        list_course[1] = str('000')
        
    if int(list_course[2]) >= 100:
        list_course[2] = str(list_course[2])     
    elif 100 > int(list_course[2]) >= 10:
        list_course[2] = str('0') + str(list_course[2])
    elif 10 > int(list_course[2]) >=1:
        list_course[2] = str('00') + str(list_course[2])
    else:
        list_course[2] = str('000')
        
    new_command = []
    str_command = str(list_course[0] + list_course[1] + list_course[2])
    new_command.append(str_command)
    return new_command
    
def move(direction, speed, wait_time):
    global preview_stop
    preview_stop = True
    
    if isinstance(direction, str) == False:
        print ('direction should be an string as front, back, left, rot_trigo, rot_clock')
        return None
    
    if isinstance(speed, int) == False:
        print ('speed should be an integer between 0 to 100')
        return None
    if speed > 100:
        print ('speed should be an integer between 0 to 100')
        return None
    if speed < 0:
        print ('speed should be an integer between 0 to 100')
        return None
    
    if isinstance(wait_time, int) == False:
        print ('time should be an integer')
        return None
    
    socket_send([88],False)
    socket_send([88],False)
    
    socket_send([6],False)
    socket_send([1],False)
    
    if direction == 'front':
        command = [int((speed*1.27)+127),127,127]
    elif direction == 'back':
        command = [int(-(speed*1.27))+127,127,127]
    elif direction == 'leftt':
        command = [127,int((speed*1.27)+127),127]
    elif direction == 'right':
        command = [127,int(-(speed*1.27)+127),127]
    elif direction == 'rot_trigo':
        command = [127,127,int((speed*1.27)+127)]
    elif direction == 'rot_clock':
        command = [127,127,int(-(speed*1.27)+127)]
    else:
        print('direction is not correct')
    
    corrected_command = correction_command(command)

    socket_send(corrected_command,False)
    
    time.sleep(wait_time)   
    
    socket_send([88],False)
    socket_send([88],False)

def direct_control(axial, radial, rotation, stop):

    if isinstance(axial, int) == False:
        print ('axial should be an interger')
        return None
    if axial> 255 or axial<0:
        print ('axial should be include between 0 and 255')
        return None
    
    if isinstance(radial, int) == False:
        print ('Radial should be an interger')
        return None
    if radial> 255 or radial<0:
        print ('Radial should be include between 0 and 255')
        return None
    
    if isinstance(rotation, int) == False:
        print ('rotation should be an interger')
        return None
    if rotation> 255 or rotation<0:
        print ('rotation should be include between 0 and 255')
        return None
    
    if isinstance(stop, bool) == False:
        print("stop should be a boolean, True or False")
        return None
    
    global preview_stop
    
    if preview_stop == True:
        socket_send([88],False)
        socket_send([88],False)
        socket_send([6],False)
        socket_send([1],False)
    
    preview_stop = stop
    
    command = [axial, radial, rotation]
    corrected_command = correction_command(command)
    socket_send(corrected_command,False)
    
    if stop == True:
        socket_send([88],False)
        socket_send([88],False)

def calculatrice(ilo_calcul):
    global preview_stop
    preview_stop = True
    
    if isinstance(ilo_calcul, str) == False:
        print("ilo_calcul should be an integer as 3+2-1.5 // put comma")
        return None
   
    socket_send([88],False)
    socket_send([88],False)
    
    socket_send([2],False) 
    
    list_user = []
    c = 1
    decimal_number =  False
    d = 0.1
    number = 0
    signe = 1
    for val in range(len(ilo_calcul)):
        if ilo_calcul[val] == '+':
            signe = 1
        elif ilo_calcul[val] == '-':
            signe = -1   
        elif ilo_calcul[val] == '.':
            decimal_number = True

        else:
            if decimal_number == True:
                number = number + d*int(ilo_calcul[val])
                d = d/10 
            else: 
                number = number*c + int(ilo_calcul[val])
                c = 10
            if val+1 == len(ilo_calcul) or ilo_calcul[val+1] == '+' or ilo_calcul[val+1] == '-':
                value = round((number*signe),2)
                list_user.append(value)
                c = 1
                decimal_number =  False
                d = 0.1
                number = 0
                signe = 1

    print('list sendable :',list_user)
    socket_send(list_user, True)
    socket_send([88],False) 
        
def list_order(ilo_list):
    
    if isinstance(ilo_list, list) == False:
        print ('the variable should be a list, with inside string as front, back, left, rot_trigo, rot_clock')
        return None
    
    global preview_stop
    preview_stop = True
    
    for i in range(len(ilo_list)):
        step(ilo_list[i])
    
def game():
    axial_value = 127
    radial_value = 127
    rotation_value = 127
    direct_control(127, 127, 127, False)
    print('Game mode start, use keyboard arrow to control ilo')
    print("Press echap to leave the game mode")
    
    send_info = False
    
    while (True):
        if keyboard.is_pressed("8"):
            time.sleep(0.05)
            send_info = True
            axial_value = axial_value + 5
            if axial_value > 255:
                axial_value = 255     
        elif keyboard.is_pressed("2"):
            time.sleep(0.05)
            send_info = True
            axial_value = axial_value - 5
            if axial_value < 1:
                axial_value = 0
        elif keyboard.is_pressed("6"):
            time.sleep(0.05)
            send_info = True
            radial_value = radial_value + 5
            if radial_value > 255:
                radial_value = 255  
        elif keyboard.is_pressed("4"):
            time.sleep(0.05)
            send_info = True
            radial_value = radial_value - 5
            if radial_value < 1:
                radial_value = 0
        elif keyboard.is_pressed("3"):
            time.sleep(0.05)
            send_info = True
            rotation_value = rotation_value + 5
            if rotation_value > 255:
                rotation_value = 255  
        elif keyboard.is_pressed("1"):
            time.sleep(0.05)
            send_info = True
            rotation_value = rotation_value - 5
            if rotation_value < 1:
                rotation_value = 0  
        elif keyboard.is_pressed("space"):
            time.sleep(0.05)
            send_info = True
            axial_value = 127
            radial_value = 127
            rotation_value = 127  
        elif keyboard.is_pressed("esc"):
            direct_control(127, 127, 127, True)
            break
        
        if send_info == True:
            direct_control(axial_value, radial_value, rotation_value, False)
            send_info = False
                 
def detection():
    #capteur = reception_data from esp32 provide list of capteur value
    capteur_front = 0
    capteur_back  = 0
    capteur_left  = 0
    capteur_right = 0
    detection = [capteur_front, capteur_back, capteur_left, capteur_right]
    return detection
        