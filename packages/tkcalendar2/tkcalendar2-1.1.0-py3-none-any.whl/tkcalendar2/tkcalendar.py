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
        self.ca.DateSelected+=self.__date_selected
        self.date_selected_func=None
        self.ca.DateChanged+=self.__date_changed
        self.__date_changed_func=None

    def __resize(self,event):
        self.ca.Width=self.winfo_width()
        self.ca.Height=self.winfo_height()

    def __date_selected(self,this,e):
        if self.date_selected_func==None:
            pass
        else:
            self.date_selected_func(this,e.Start.ToString(),e.End.ToString())
    def date_selected(self,func):
        self.date_selected_func=func

    def __date_changed(self,this,e):
        if self.__date_changed_func==None:
            pass
        else:
            self.__date_changed_func(this,e.Start.ToShortDateString())
    def date_changed(self,func):
        self.date_changed_func=func

    def max_selection_count(self,days:int):
        self.ca.MaxSelectionCount=days


def test():
    a=Tk()
    a.geometry('600x600+5+5')

    ca=TkCalendar(a,500,500)
    ca.pack(fill='both',expand='True')
    ca.date_selected(print)
    ca.date_changed(print)
    ca.max_selection_count(20)

    a.mainloop()

if __name__=='__main__':
    test()
