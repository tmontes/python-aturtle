# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import tkinter



class Window:

    _windows = []

    def __init__(self, width=320, height=320, x=None, y=None,
                 fill_color='white', title='A-Turtle'):

        tk_window = tkinter.Tk() if not Window._windows else tkinter.Toplevel()
        Window._windows.append(self)

        tk_window.title(title)

        # Negative x/y values place tk_window from right/bottom of screen.
        if x is not None and x < 0:
            x = tk_window.winfo_screenwidth() - width + x
        if y is not None and y < 0:
            y = tk_window.winfo_screenheight() - height + y

        # Center tk_window on screen unless (x, y) is given.
        x = (tk_window.winfo_screenwidth() - width) // 2 if x is None else x
        y = (tk_window.winfo_screenheight() - height) // 2 if y is None else y

        tk_window.geometry(f'{width}x{height}+{x}+{y}')
        canvas = tkinter.Canvas(
            tk_window,
            highlightthickness=0,
            background=fill_color,
        )
        canvas.pack(expand=True, fill='both')
        tk_window.update()

        # Make (0, 0) the visual canvas center.
        canvas.config(xscrollincrement=1, yscrollincrement=1)
        self._x_scroll = -width // 2
        self._y_scroll = -height // 2
        canvas.xview_scroll(self._x_scroll, 'units')
        canvas.yview_scroll(self._y_scroll, 'units')

        # Handle tk_window resizing.
        tk_window.bind('<Configure>', self._resize_handler)

        self._tk_window = tk_window
        self.canvas = canvas

        # Event bindings.
        self._binds = {}

        # Direct key support.
        self._direct_key_callbacks = {}
        self._direct_key_after_ids = {}


    @property
    def x(self):

        return self._tk_window.winfo_x()


    @x.setter
    def x(self, value):

        if value < 0:
            value = self._tk_window.winfo_screenwidth() - self.width + value

        self._tk_window.geometry(f'+{value}+{self.y}')


    @property
    def y(self):

        return self._tk_window.winfo_y()


    @y.setter
    def y(self, value):

        if value < 0:
            value = self._tk_window.winfo_screenheight() - self.height + value

        self._tk_window.geometry(f'+{self.x}+{value}')


    @property
    def width(self):

        return self._tk_window.winfo_width()


    @width.setter
    def width(self, value):

        self._tk_window.geometry(f'{value}x{self.height}')


    @property
    def height(self):

        return self._tk_window.winfo_height()


    @height.setter
    def height(self, value):

        self._tk_window.geometry(f'{self.width}x{value}')


    def _resize_handler(self, event):

        # Adjust canvas scroll to keep (0, 0) centered.

        new_x_scroll = -event.width // 2
        self.canvas.xview_scroll(new_x_scroll-self._x_scroll, 'units')
        self._x_scroll = new_x_scroll

        new_y_scroll = -event.height // 2
        self.canvas.yview_scroll(new_y_scroll-self._y_scroll, 'units')
        self._y_scroll = new_y_scroll


    def bind(self, sequence, cb):

        self._binds[sequence] = self._tk_window.bind(sequence, cb)


    def unbind(self, sequence=None):

        if sequence is None:
            sequences = list(self._binds)
            for sequence in sequences:
                self.unbind(sequence)
        elif sequence in self._binds:
            self._tk_window.unbind(sequence, self._binds[sequence])
            del self._binds[sequence]
        else:
            raise ValueError(f'Unknown bound sequence: {sequence!r}.')


    def bind_direct_key(self, keysym, press_cb=None, release_cb=None):

        if not press_cb and not release_cb:
            raise ValueError(f'Missing event handler argument.')

        self.bind(f'<KeyPress-{keysym}>', self._direct_key_press)
        self.bind(f'<KeyRelease-{keysym}>', self._direct_key_release)

        self._direct_key_callbacks[keysym] = (press_cb, release_cb)


    def _direct_key_press(self, event):

        keysym = event.keysym
        if keysym in self._direct_key_after_ids:
            self._tk_window.after_cancel(self._direct_key_after_ids[keysym])
            del self._direct_key_after_ids[keysym]
        else:
            press_cb, _release_cb = self._direct_key_callbacks[keysym]
            if press_cb:
                press_cb(event)


    def _direct_key_release(self, event):

        keysym = event.keysym
        after_id = self._tk_window.after_idle(self._direct_handle_release, event)
        self._direct_key_after_ids[keysym] = after_id


    def _direct_handle_release(self, event):

        keysym = event.keysym
        del self._direct_key_after_ids[keysym]
        _press_cb, release_cb = self._direct_key_callbacks[keysym]
        if release_cb:
            release_cb(event)


    def unbind_direct_key(self, keysym=None):

        if keysym is None:
            keysyms = list(self._direct_key_callbacks)
            for keysym in keysyms:
                self.unbind_direct_key(keysym)
        elif keysym in self._direct_key_callbacks:
            self.unbind(f'<KeyPress-{keysym}>')
            self.unbind(f'<KeyRelease-{keysym}>')
            del self._direct_key_callbacks[keysym]
        else:
            raise ValueError(f'Unknown bound direct key: {keysym!r}.')


    def close(self):

        is_root = self._tk_window is Window._windows[0]._tk_window
        if is_root and len(Window._windows) > 1:
            raise RuntimeError('Must be last to close.')

        self._tk_window.destroy()

        Window._windows.remove(self)
        self.canvas = None
        self._tk_window = None


    @classmethod
    def close_all(cls, strict=True):

        if not cls._windows:
            if strict:
                raise RuntimeError('No windows.')
            return

        root = cls._windows[0]._tk_window
        root.destroy()

        for window in cls._windows:
            window._tk_window = None
            window.canvas = None

        cls._windows.clear()
