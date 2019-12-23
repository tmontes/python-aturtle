# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import tkinter


class Window:

    _root = None
    _toplevels = []

    def __init__(self, w=320, h=320, x=None, y=None, title='A-Turtle'):

        if not Window._root:
            Window._root = tkinter.Tk()
            window = Window._root
        else:
            window = tkinter.Toplevel()
            Window._toplevels.append(window)

        window.title(title)

        x = (window.winfo_screenwidth() - w) // 2 if x is None else x
        y = (window.winfo_screenheight() - h) // 2 if y is None else y

        window.geometry(f'{w}x{h}+{x}+{y}')
        canvas = tkinter.Canvas(window)
        canvas.pack(expand=True, fill='both')
        window.update()

        # 0, 0 should be at the center
        canvas.config(xscrollincrement=1, yscrollincrement=1)
        self._xscroll = -w // 2
        self._yscroll = -w // 2
        canvas.xview_scroll(self._xscroll, 'units')
        canvas.yview_scroll(self._yscroll, 'units')

        # Handle window resizing
        window.bind('<Configure>', self._resize_handler)

        self._window = window
        self.canvas = canvas

        self._w = w
        self._h = h


    def _resize_handler(self, event):

        event_w = event.width
        event_h = event.height

        if event_w != self._w:
            new_xscroll = -event_w // 2
            self.canvas.xview_scroll(new_xscroll-self._xscroll, 'units')
            self._xscroll = new_xscroll
            self._w = event_w

        if event_h != self._h:
            new_yscroll = -event_h // 2
            self.canvas.yview_scroll(new_yscroll-self._yscroll, 'units')
            self._yscroll = new_yscroll
            self._h = event_h



    def close(self):

        if self._window is Window._root and Window._toplevels:
            raise RuntimeError('Must be last to close.')

        if self._window is not Window._root:
            Window._toplevels.remove(self._window)
        else:
            Window._root = None

        self._window.destroy()
        self.canvas = None
        self._window = None

