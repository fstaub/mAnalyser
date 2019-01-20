"""
===============
Embedding In Tk
===============

"""

import tkinter as tk
import tkinter.ttk as ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np




def add_canvas(frame):
    fig = Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

    canvas = FigureCanvasTkAgg(fig, master=frame)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # canvas.mpl_connect("key_press_event", on_key_press)


#toolbar = NavigationToolbar2Tk(canvas, root)
#toolbar.update()
#canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


# def on_key_press(event):
#     print("you pressed {}".format(event.key))
#     key_press_handler(event, canvas, toolbar)




# def _quit():
#     root.quit()     # stops mainloop
#     root.destroy()  # this is necessary on Windows to prevent
#                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate


# button = tk.Button(master=root, text="Quit", command=_quit)
# button.pack(side=tkinter.BOTTOM)

# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.

def init_main_frame():
    frame = tk.Frame(root)
    frame.pack()

    add_selection_frame(frame)
    add_plot_settings_frame(frame)
    add_canvas(frame)

def add_plot_settings_frame(frame): 
    new_frame = tk.Frame(frame)
    new_frame.pack(side = tk.TOP)

    group = tk.LabelFrame(new_frame, text="Settings", padx=5, pady=5)
    group.pack(padx=10, pady=10)

    # w = tk.Entry(group)
    # w.pack()


    # Buttons
    v = tk.IntVar()
    tk.Radiobutton(group, text="One", variable=v, value=1).pack(anchor=tk.W)
    tk.Radiobutton(group, text="Two", variable=v, value=2).pack(anchor=tk.W)   

def add_selection_frame(frame):
    new_frame = tk.Frame(frame)
    new_frame.pack(side = tk.TOP)

    new_frame.configure(background='black')

    add_selection_choices(new_frame)
    add_selection_buttons(new_frame)

def add_selection_buttons(frame):
    new_frame = tk.Frame(frame)
    new_frame.pack(side = tk.TOP)
    redbutton = tk.Button(new_frame, text="Red", fg="red")
    redbutton.pack( side = tk.LEFT)

    greenbutton = tk.Button(new_frame, text="Brown", fg="brown")
    greenbutton.pack( side = tk.RIGHT )

def add_selection_choices(frame):
    new_frame = tk.Frame(frame)
    new_frame.pack(side = tk.TOP)
    # Buttons
    v = tk.IntVar()
    tk.Radiobutton(new_frame, text="One", variable=v, value=1).pack(anchor=tk.W)
    tk.Radiobutton(new_frame, text="Two", variable=v, value=2).pack(anchor=tk.W)





root = tk.Tk()


# style = ttk.Style()
# style.configure("BW.TLabel", foreground="black", background="white")


root.wm_title("mAnalyser")



init_main_frame()
root.configure(background='black')

tk.mainloop()
