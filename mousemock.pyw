import wx
import win32api
import win32con #for the VK keycodes
from threading import *
import time
EVT_RESULT_ID = wx.NewId()


def presskey(vitural_key, modifier):
    if modifier & 1:
        win32api.keybd_event(win32con.MOD_CONTROL, 0)
    if modifier & 2:
        win32api.keybd_event(win32con.MOD_SHIFT, 0)
    if modifier & 4:
        win32api.keybd_event(win32con.MOD_ALT, 0)
    win32api.keybd_event(vitural_key, 0)
    win32api.keybd_event(vitural_key, 0, win32con.KEYEVENTF_KEYUP)
    if modifier & 4:
        win32api.keybd_event(win32con.MOD_ALT, 0, win32con.KEYEVENTF_KEYUP)
    if modifier & 2:
        win32api.keybd_event(win32con.MOD_SHIFT, 0, win32con.KEYEVENTF_KEYUP)
    if modifier & 1:
        win32api.keybd_event(win32con.MOD_CONTROL, 0, win32con.KEYEVENTF_KEYUP)
    
def mouseClick():
    #print("Click!")
    x,y = win32api.GetCursorPos()
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0) 
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def mouseRightClick():
    x,y = win32api.GetCursorPos()
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)

def mouseEvent(opt):
    x,y = win32api.GetCursorPos()
    win32api.mouse_event(opt,x,y,0,0)

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)
    
class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data
        
class WorkerThread(Thread):
    '''Worker Thread Class.'''
    def __init__(self, notify_window, timer):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = False
        self.timer = timer
        self.vkey = notify_window.vkey
        self.mod = int(notify_window.ctrl.GetValue()) | 2*int(notify_window.shift.GetValue()) | 4*int(notify_window.alt.GetValue())
        self.rightclick = notify_window.rightclick.Value
        self.lasting = notify_window.lasting.Value
        self.start()
        
    def run(self):
        if self.lasting:
            '''if self.vkey:
                presskey(self.vkey, self.mod)
            el'''
            if self.rightclick:
                mouseEvent(win32con.MOUSEEVENTF_RIGHTDOWN)
            else:
                mouseEvent(win32con.MOUSEEVENTF_LEFTDOWN)
            while True:
                if self._want_abort:
                    '''if self.vkey:
                        presskey(self.vkey, self.mod)
                    el'''
                    if self.rightclick:
                        mouseEvent(win32con.MOUSEEVENTF_RIGHTUP)
                    else:
                        mouseEvent(win32con.MOUSEEVENTF_LEFTUP)
                    wx.PostEvent(self._notify_window, ResultEvent(None))
                    return
                time.sleep(self.timer)
        else:
            while True:
                if self._want_abort:
                    wx.PostEvent(self._notify_window, ResultEvent(None))
                    return
                if self.vkey:
                    presskey(self.vkey, self.mod)
                elif self.rightclick:
                    mouseRightClick()
                else:
                    mouseClick()
                time.sleep(self.timer)
                #print (self.timer)
        
    def abort(self):
        self._want_abort = True


class Frame1(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        
        self.vkey = 0
        self.mod = 0
        self.autoClick = False
        self.worker = None
        self.__set_properties()
        self.regHotKey()
        self.Bind(wx.EVT_HOTKEY, self.handleHotKey, id=self.hotKeyId)
        self.slider1 = wx.Slider(self, -1, 0, -3000, 3000, (0,0), (300, 20))
        self.label1 = wx.StaticText(self, 0, "每秒点击一次", (0, 20), (300, 30), wx.TE_CENTER)
        self.ctrl = wx.CheckBox(self, 1, "ctrl", (0, 100), (100, 20))
        self.shift = wx.CheckBox(self, 2, "shift", (120, 100), (100, 20))
        self.alt = wx.CheckBox(self, 3, "alt", (240, 100), (100, 20))
        self.key = wx.TextCtrl(self, 4, "输入Virtual-Key Code", (0, 80), (200,20))
        self.key.Bind(event = wx.EVT_TEXT_ENTER, handler = self.setvkey)
        self.slider1.Bind(event = wx.EVT_SLIDER, handler = self.settime)
        self.rightclick = wx.CheckBox(self, 5, "右键", (0, 40), (80, 30))
        self.lasting = wx.CheckBox(self, 6, "按住", (100, 40), (80, 30))

    def __set_properties(self):
        self.SetTitle("AutoClicker")
        self.SetSize((317, 200))
        self.SetBackgroundColour("white")
        
    def regHotKey(self):
        """
        This function registers the hotkey Alt+F1 with id=100
        """
        self.hotKeyId = 100
        self.RegisterHotKey(
            self.hotKeyId, #a unique ID for this hotkey
            win32con.MOD_ALT | win32con.MOD_CONTROL, #the modifier key
            0x5A) #the key to watch for
    def handleHotKey(self, evt):
        self.autoClick = not self.autoClick
        if self.autoClick:
            self.worker = WorkerThread(self, 10**(-0.001*self.slider1.GetValue()))
        else:
            self.worker.abort()
            self.worker = None
        #print (self.autoClick)
    
    def setvkey(self, e):
        try:
            if self.key.GetValue == "":
                self.vkey = 0
                return
            self.vkey = int(self.key.GetValue())
        finally:
            self.key.SetValue(str(self.vkey))
    def settime(self, e):
        if self.slider1.GetValue() < 0:
            self.label1.SetLabel("每" + str("%.3f"%10**(-0.001*self.slider1.GetValue())) + "秒点击一次")
        else:
            self.label1.SetLabel("每秒点击" + str("%.3f"%10**(0.001*self.slider1.GetValue())) + "次")

class AutoClicker(wx.App):
    def OnInit(self):
        frame1 = Frame1(None, wx.ID_ANY, "")
        self.SetTopWindow(frame1)
        frame1.Show()
        return 1

autoClicker = AutoClicker(0)
autoClicker.MainLoop()
