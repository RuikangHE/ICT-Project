# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 00:48:13 2020

@author: 2369158615@qq.com
"""

import tkinter
from tkinter import *
import pandas as pd
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import numpy as np


class Demo1:
    def __init__(self, master):
        self.master = master
        self.frame = tkinter.Frame(self.master)
        self.button1 = tkinter.Button(self.master, text = 'View Wheels Hisotry', width = 33, command = self.new_window).place(x = 30,y = 80)
        #self.button1.pack()
        # name = tkinter.StringVar()
        # self.nameEntered = ttk.Entry(self.master, width = 15, textvariable = name)
        # self.nameEntered.pack()
        
        self.name = Label(self.master, text = "Name").place(x = 30,y = 50) 
        self.query = StringVar()
        self.entry = Entry(self.master, textvariable=self.query)#.place(x = 80, y = 50)
        self.entry.place(x = 80 , y = 50)
        # Entry(self.master, textvariable=self.query).pack()
        
        self.frame.pack()

    def new_window(self):
        self.newWindow = tkinter.Toplevel(self.master)
        entered = self.query.get()
        self.app = Demo2(self.newWindow, entered)

class Demo2:
    def __init__(self, master, entered):
        self.master = master
        self.frame = tkinter.Frame(self.master)
        rawData = pd.read_excel("C:\\Users\\23691\\Desktop\\Wheels History.xlsx")
        # locomotive = input("Please input a locomotive unit to continues: ")
        data = rawData[rawData["Locomotive"]==entered]
        measureDate = []
        for x in data[data.columns[1]]:
            measureDate.append(str(x)[0:10])
        df = pd.DataFrame(measureDate)
        data = data.sort_values(by=data.columns[1], ascending=True)
        df = df.sort_values(by=df.columns[0],ascending=True)
        
        fig = Figure(figsize=(16, 8), dpi=100)
        t = np.arange(0, 3, .01)
        ax = fig.add_subplot(521)
        ax.plot_date(df[df.columns[0]],data[data.columns[6]], linestyle = 'solid', label = data.columns[6])
        for a,b in zip(df[df.columns[0]], data[data.columns[6]]): 
            ax.text(a, b, str(b))
        ax.legend()
        ax = fig.add_subplot(522)
        ax.plot_date(df[df.columns[0]],data[data.columns[7]], linestyle = 'solid', color = 'tab:blue', label = data.columns[7])
        for a,b in zip(df[df.columns[0]], data[data.columns[7]]): 
            ax.text(a, b, str(b))
        ax.legend()
        
        ax = fig.add_subplot(523)
        ax.plot_date(df[df.columns[0]],data[data.columns[8]], linestyle = 'solid', color = 'tab:orange', label = data.columns[8])
        for a,b in zip(df[df.columns[0]], data[data.columns[8]]): 
            ax.text(a, b, str(b))
        ax.legend()
        
        ax = fig.add_subplot(524)
        ax.plot_date(df[df.columns[0]],data[data.columns[10]], linestyle = 'solid', color = 'tab:green', label = data.columns[10])
        for a,b in zip(df[df.columns[0]], data[data.columns[10]]): 
            ax.text(a, b, str(b))
        ax.legend()
        
        ax = fig.add_subplot(525)
        ax.plot_date(df[df.columns[0]],data[data.columns[11]], linestyle = 'solid', color = 'tab:purple', label = data.columns[11])
        for a,b in zip(df[df.columns[0]], data[data.columns[11]]): 
            ax.text(a, b, str(b))
        ax.legend()
        
        ax = fig.add_subplot(526)
        ax.plot_date(df[df.columns[0]],data[data.columns[12]], linestyle = 'solid', color = 'tab:brown', label = data.columns[12])
        for a,b in zip(df[df.columns[0]], data[data.columns[12]]): 
            ax.text(a, b, str(b))
        ax.legend()
        
        ax = fig.add_subplot(527)
        ax.plot_date(df[df.columns[0]],data[data.columns[13]], linestyle = 'solid', color = 'tab:pink', label = data.columns[13])
        for a,b in zip(df[df.columns[0]], data[data.columns[13]]): 
            ax.text(a, b, str(b))
        ax.legend()
        
        ax = fig.add_subplot(528)
        ax.plot_date(df[df.columns[0]],data[data.columns[14]], linestyle = 'solid', color = 'tab:gray', label = data.columns[14])
        for a,b in zip(df[df.columns[0]], data[data.columns[14]]): 
            ax.text(a, b, str(b))
        ax.legend()
        
        ax = fig.add_subplot(529)
        ax.plot_date(df[df.columns[0]],data[data.columns[15]], linestyle = 'solid', color = 'tab:olive', label = data.columns[15])
        for a,b in zip(df[df.columns[0]], data[data.columns[15]]): 
            ax.text(a, b, str(b))
        ax.legend()
        
        ax = fig.add_subplot(5, 2, 10)
        ax.plot_date(df[df.columns[0]],data[data.columns[16]], linestyle = 'solid', color = 'tab:cyan', label = data.columns[16])
        for a,b in zip(df[df.columns[0]], data[data.columns[16]]): 
            ax.text(a, b, str(b))
        ax.legend()
        self.frame.pack()
        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, master=self.master)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self.master)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        tkinter.mainloop()

        
    def close_windows(self):
        self.master.destroy()

def main(): 
    root = tkinter.Tk()
    root.withdraw()
    root.update_idletasks()
    
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.geometry("300x166+" + str(int(x)) + "+" + str(int(y)))
    
    root.deiconify() 
  
    app = Demo1(root)
    root.mainloop()

if __name__ == '__main__':
    main()
