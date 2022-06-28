import threading
import pynput
from pynput.mouse import Button, Controller
import time
import PySimpleGUI as sg
import sys
import keyboard
import random
mouse = Controller()
dis = 1
double_clicks = 1 #Multiplier 1 = 2, 2 = 3
down = False
autoclick = False
live = True
au_key = ""
toggled = False
ac_values = [0,0]
def on_click(x,y,button,pressed):
    global dis
    global down
    dis += 1
    if dis == 0 + (3*double_clicks):
        dis = 0
        time.sleep(0.0001)
        if down:
            mouse.click(button,1)
        
            print("Double Clicked")


def main():
    global down
    global listener
    global autoclick
    global live
    global toggled
    global ac_values
    sg.theme('LightBlue')
    sg.set_options(element_padding=(0, 0))

    layout = [[sg.Text('Ghast Ghost Client', pad=(50,0), size=(16, 1))],
    [sg.Button('Off', size=(3,1),
               button_color=('white', 'light green'),
               key='_B_'),
    sg.Text('Double Click', pad=(34,0))],
    [sg.Button('Off', size=(3,1),
               button_color=('white', 'light salmon'),
               key='_A_'),
    sg.Text('Autoclicker', pad=(27,0)),
    sg.InputText(' ',key="key",size=(3,1),use_readonly_for_disable=False,enable_events=True,disabled=False,focus=True)
    ],
    [sg.Button('Off', size=(3,1),
               button_color=('white', 'light salmon'),
               key='toggle'),
    sg.Text('Toggle', pad=(15,0))
    ],
    [sg.Button('Left', size=(5,1),
               button_color=('white', 'light salmon'),
               key='right'),
    sg.Text('Button')
    ],
    [sg.Slider(range=(1,20),
               orientation='horizontal',
               key='Max'),
    sg.Text('Max',
            pad=(0,5),
            size=(4, 0)),
    sg.Input(key="dataMax",size=(3,1),use_readonly_for_disable=False,enable_events=True,disabled=False)
    ],
    [sg.Slider(range=(1,20),
               orientation='horizontal',
               key='Min'),
    sg.Text('Min',
            pad=(0,30),
            size=(4, 0)),
    sg.Input(key="dataMin",size=(3,1))
    ],
    [sg.Button('Exit' ,pad=(50,0))]]

    window = sg.Window("Borderless Window",
                    layout,
                    default_element_size=(12, 1),
                    location=(0,0),
                    text_justification='r',
                    auto_size_text=False,
                    auto_size_buttons=False,
                    no_titlebar=True,
                    grab_anywhere=False,
                    default_button_element_size=(12, 1))
    event, values = window.read(timeout=1)
    window.Element('_B_').Update(('Off','On')[down], button_color=(('white', ('light salmon', 'light green')[down])))
    can = False
    button = Button.left
    tcb = False
    def autocli():
        while live:
            if autoclick == True:
                a1 = ac_values[0]
                a2 = ac_values[0]
                if a2 > a1:
                    a2 = a1
                val = (random.randint(a1*10,a2*10))
                time.sleep(1/(val/10))
                mouse.click(button,1)
    try:
        keyboard.read_key()
        can = True
    except:
        can = False
        print("Sudo Is Required For KeyBinds To Work On Linux!")
    threade = threading.Thread(target=autocli)
    threade.start()
    while live:


        event, values = window.read(timeout=0)
        window['dataMin'].update(int(values['Min']))
        window['dataMax'].update(int(values['Max']))
        window['Min'].update(range=(1,int(values['Max'])))
        ac_values[0] = int(values['Min'])
        ac_values[1] = int(values['Max'])
        if event in (sg.WIN_CLOSED, 'Exit'):
            window.close()
            down = False
            listener.stop()
            live=False
            sys.exit()
        if event in (None, 'Exit'):
            window.close()
            down = False
            listener.stop()
            live=False
            sys.exit()
        if len(values["key"]) > 1:
            if values["key"][1] == " ":

                try:
                    window.Element('key').Update(values["key"][2])
                except:
                    print("Dont Spam")
            else:
                try:
                    window.Element('key').Update(values["key"][1])
                except:
                    print("Dont Spam")
        if values["key"] == "":
            window.Element('key').Update(" ")
        au_key = values["key"]
        if event == '_B_':
            down = not down
        window.Element('_B_').Update(('Off','On')[down], button_color=(('white', ('light salmon', 'light green')[down])))
        if event == '_A_':
            autoclick = not autoclick
        if can:
            if toggled:
                if keyboard.read_key() == au_key:
                    autoclick = not autoclick
            else:
                if keyboard.read_key() == au_key:
                    autoclick = True
                else:
                    autoclick = False
        window.Element('_A_').Update(('Off','On')[autoclick], button_color=(('white', ('light salmon', 'light green')[autoclick])))
        if event == 'toggle':
            toggled = not toggled
        window.Element('toggle').Update(('Off','On')[toggled], button_color=(('white', ('light salmon', 'light green')[toggled])))

        if event == 'right':
            tcb = not tcb
        window.Element('right').Update(('Left','Right')[tcb], button_color=(('white', ('light blue', 'light blue')[tcb])))
thread = threading.Thread(target=main)
thread.start()
with pynput.mouse.Listener(
    on_click=on_click) as listener:
    listener.join()


