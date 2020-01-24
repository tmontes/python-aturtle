Python A-Turtle: AsyncIO-ready Turtle Graphics
==============================================

Python A-Trutle is a library that implements Turtle Graphics with `asyncio` support.

A short capability summary:

* Supports both sync and asyncio compatible coroutine API.
* Multiple turtle support with either vector or bitmap shapes.
* Concurrent animation support via the coroutine API.
* Built on top of the Standard Library's ``tkinter`` module.
* Sprite support (essentially turtles that don't draw lines)
* More.


Installation
------------

Python A-Turtle is a pure Python package distributed via `PyPI <https://pypi.org/pypi/aturtle>`_. Install it with:

.. code-block:: console
                                                                                          
        $ pip install aturtle

For improved bitmap image rotation speed and quality, install the optional `Pillow <https://pypi.org/pypi/Pillow>`_ extra with:

.. code-block:: console
                                                                                          
        $ pip install aturtle[pillow]



Quick Start
-----------

.. code-block:: python                                                                    

    import aturtle

    w = aturtle.Window()
    sh = aturtle.shapes.vector.Triangle(radius=20, angle=0)
    s = aturtle.create_sprite(w, sh, update=True)
    t = aturtle.turtle.Turtle(s)
    t.sync_forward(100)


Thanks
------

.. marker-start-thanks-dont-remove

* To the creators and maintainers of `Tcl/Tk <https://www.tcl.tk/>`_, a programming language I used for a while in the late 1990's, in particular for the seriously under-appreciated `Canvas widget <https://www.tcl.tk/man/tcl8.6/TkCmd/canvas.htm>`_ which is amazingly powerful. Python embeds the Tcl/Tk interpreter in the form of the `tkinter <https://docs.python.org/3/library/tkinter.html>`_ Standard Library module. Long live Tcl/Tk and `tkinter`!

* To whoever `Quarks <https://www.daniweb.com/members/228139/quarks>`_ is, for sharing an effective technique for debouncing Tk `KeyPress` / `KeyRelease` events in towards the end of `this thread <https://www.daniweb.com/programming/software-development/threads/70746/keypress-event-with-holding-down-the-key>`_.

* To `Terry Pratchet <https://en.wikipedia.org/wiki/Terry_Pratchett>`_, for his `Discworld <https://en.wikipedia.org/wiki/Discworld>`_ novels and, in particular, for `Great A'Tuin <https://en.wikipedia.org/wiki/Discworld_%28world%29#Great_A%27Tuin>`_, the *"Giant Star Turtle (...) who travels through the Discworld universe's space, carrying four giant elephants (...) who in turn carry the Discworld."*, which has come to my mind often while creating this.

.. marker-end-thanks-dont-remove



About
-----

.. marker-start-about-dont-remove

Python A-Turtle is being created by Tiago Montes.

.. marker-end-about-dont-remove

