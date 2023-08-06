from tkinter import Tk,Frame
from webbrowser import open as webopen
import ctypes
user32=ctypes.windll.user32

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
clr.AddReference('System')
from System.Windows.Forms import MonthCalendar
from System.Drawing import Font
from System import String,Single


class TkCalendar(Frame):
    '''日历框'''

    def __init__(self,master,width,height):
        Frame.__init__(self,master,width=width,height=height)
        self.ca=MonthCalendar()
        self.cahwnd=int(str(self.ca.Handle))
        user32.SetParent(self.cahwnd,self.winfo_id())
        user32.MoveWindow(self.cahwnd,0,0,width,height,True)
        self.bind('<Configure>',self.__resize)
        self.__bind_event()

    def __bind_event(self):
        pass

    def __resize(self,event):
        self.ca.Width=self.winfo_width()
        self.ca.Height=self.winfo_height()


def test():
    a=Tk()
    a.geometry('600x600+5+5')

    rt=TkCalendar(a,500,500)
    rt.pack(fill='both',expand='True')

    a.mainloop()

if __name__=='__main__':
    test()
