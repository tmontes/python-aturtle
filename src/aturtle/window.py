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

    def __init__(self, width=320, height=320, x=None, y=None,
                 fill_color='white', title='A-Turtle'):

        if not Window._root:
            Window._root = tkinter.Tk()
            window = Window._root
        else:
            window = tkinter.Toplevel()
            Window._toplevels.append(window)

        window.title(title)

        # Center window on screen unless (x, y) is given.
        x = (window.winfo_screenwidth() - width) // 2 if x is None else x
        y = (window.winfo_screenheight() - height) // 2 if y is None else y

        window.geometry(f'{width}x{height}+{x}+{y}')
        canvas = tkinter.Canvas(
            window,
            highlightthickness=0,
            background=fill_color,
        )
        canvas.pack(expand=True, fill='both')
        window.update()

        # Make (0, 0) the visual canvas center.
        canvas.config(xscrollincrement=1, yscrollincrement=1)
        self._x_scroll = -width // 2
        self._y_scroll = -width // 2
        canvas.xview_scroll(self._x_scroll, 'units')
        canvas.yview_scroll(self._y_scroll, 'units')

        # Handle window resizing.
        window.bind('<Configure>', self._resize_handler)

        self._window = window
        self.canvas = canvas

        self._width = width
        self._height = height


    def _resize_handler(self, event):

        # Adjust canvas scroll to keep (0, 0) at the visual center.

        event_width = event.width
        event_height = event.height

        if event_width != self._width:
            new_x_scroll = -event_width // 2
            self.canvas.xview_scroll(new_x_scroll-self._x_scroll, 'units')
            self._x_scroll = new_x_scroll
            self._width = event_width

        if event_height != self._height:
            new_y_scroll = -event_height // 2
            self.canvas.yview_scroll(new_y_scroll-self._y_scroll, 'units')
            self._y_scroll = new_y_scroll
            self._height = event_height


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
