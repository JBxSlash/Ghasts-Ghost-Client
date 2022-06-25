from threading import Thread
import pynput
from pynput.mouse import Controller
import time
import PySimpleGUI as sg
import sys
mouse = Controller()
dis = 1
double_clicks = 1 #Multiplier 1 = 2, 2 = 3
down = True
def on_click(x,y,button,pressed):
    global dis
    global down
    dis += 1
    if dis == 0 + (3*double_clicks):
        dis = 0
        time.sleep(0.0001)
        if down:
            mouse.click(button,1)
        
            ("Double Clicked")
listener = pynput.mouse.Listener(on_click=on_click)
def main():
    global down
    global listener
    sg.theme('light blue')
    sg.set_options(element_padding=(0, 0))

    layout = [[sg.Text('Ghast Ghost Client', pad=((0, 0), 0), size=(16, 1))],
    [sg.Button('On', size=(3,1), button_color=('white', 'light green'), key='_B_'), sg.Button('Exit')]]

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
    window.finalize()
   
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            window.close()
            down = False
            listener.stop()
            sys.exit()
        if event in (None, 'Exit'):
            window.close()
            down = False
            listener.stop()
            sys.exit()
        if event == '_B_':
            down = not down
            window.Element('_B_').Update(('Off','On')[down], button_color=(('white', ('light salmon', 'light green')[down])))

thread = Thread(target=main)
thread.start()

listener.start()
listener.join()
