import wx

from catalog import App

if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None)
    App(frame)
    frame.Show()
    app.MainLoop()
