# Run with pysimplegui-4.28.0

import PySimpleGUI as sg
import time

wait_indicator_text = sg.Text("Calculating the crop,\nthis may take a while...",
                              visible=True)

layout = [
            [sg.Button("Crop")],
            [wait_indicator_text],
         ]
window = sg.Window(title="Crop Button", layout=layout, return_keyboard_events=True,) # finalize kwarg only after 4.0.0 sometime
window.Finalize()
wait_indicator_text.Update(visible=False)

while True: # Main event loop.
    btn, values_dict = window.Read()

    if btn.startswith("Crop"):
        print("Crop button")
        wait_indicator_text.Update(visible=True)
        window.refresh()
        time.sleep(1)
        wait_indicator_text.Update(visible=False)

