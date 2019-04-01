
    
def active():
    global power
    vel = 10
    while(pressedKeys != []):
        mns = ""
        for i in pressedKeys:
            if i == 'Up':
                if(power < 1000):
                   power+=vel
                   mns += "pwm:"+str(power)+";"
    
            elif i == 'Down':
                if(power > -1000):
                    power-=vel
                    mns += "pwm:"+str(power)+";"

            elif i == 'Right':
                dire = 1
                mns += "dir:"+str(dire)+";"

            elif i == 'Left':
                dire = -1
                mns += "dir:"+str(dire)+";"

            elif i == 'h':
                horn = 1
                mns += "horn:"+str(horn)+";"

            elif i == 'l' and toggle:
                toggle = False
                lights[0] = not lights[0]
                mns += "ll:"+str(lights[0])+";"
            
            elif i == 'r' and toggle:
                toggle = False
                lights[1] = not lights[1]
                mns += "lr:"+str(lights[1])+";"

            elif i == 'b' and toggle:
                toggle = False
                lights[2] = not lights[2]
                mns += "lb:"+str(lights[2])+";"

            elif i == 'f' and toggle:
                toggle = False
                lights[3] = not lights[3]
                mns += "lf:"+str(lights[3])+";"

            myCar.send(mns)
            pressedKeys.remove(i)

def default(keyName):
    mns = ""
    if keyName == 'Up' or keyName == 'Down' :
        power=0
        mns += "pwm:"+str(power)+";"
    elif keyName == 'Right' or keyName == 'Left':
        dire = 0
        mns += "dire:"+str(dire)+";"
    elif keyName == 'h':
        horn = 0
        mns += "horn:"+str(horn)+";"
    else:
        toggle = True
        
    
def keyPress(event, focus):
    if(focus):
        keyName = event.keysym
        if(keyName in ['Up','Down','Right','Left', 'l', 'r', 'b', 'f', 'h', 'Space']):
            if(not (keyName in pressedKeys)):
                pressedKeys.append(keyName)
            active()


def keyRelease(event, focus):
    if(focus):
        keyName = event.keysym
        if(keyName in ['Up','Down','Right','Left', 'h','l', 'r', 'b', 'f', 'Space'] and (keyName in pressedKeys)):            
            pressedKeys.remove(keyName)
            default(keyName)
