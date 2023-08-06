"""

Browse a circlify object with tkinter
=====================================
"""


import tkinter as tk
from tkinter import ttk

from nobvisual.utils import shade_color
from nobvisual.utils import PAULT_BRIGHT
from nobvisual.objects import CircularPackingCanvas
from nobvisual.objects import UnderFocusLabel
from nobvisual.objects import HighlightedText


SIZE = 800
BKGD = "#ffffff"


__all__ = ["tkcirclify"]


def tkcirclify(
    circles,
    holder=None,
    color="#777777",
    shade=-0.1,
    legend=None,
    colorscale=None,
    title=None,
    show_under_focus=True,
):
    """Generate a Circlify in a Tkinter canvas.

    :param circles: a ciclify object, list of Circles objects.
    :param color: hex coloer, for background of circles.
    :param shade: shading, making nested levels lighter (>0) or darker (<0)
        in range of floats [-0.5, 0.5]

    No returns
    ----------

    Interrupt the process with a tkinter canvas.
    """

    if holder is None:
        holder = tk.Tk()

    # create canvas
    canvas_holder = tk.Frame(holder, background=BKGD)
    inner_size = 0.9 * SIZE
    draw_can = CircularPackingCanvas(canvas_holder, inner_size, bg=BKGD, bd=5,
                                     base_color=color, shade_factor=shade)
    draw_can.pack()
    canvas_holder.pack(side='left')

    for circle in circles:
        draw_can.add_circle(circle)

    if show_under_focus:
        # under focus label
        frm = tk.LabelFrame(holder, text="UnderFocus", width=int(0.61 * SIZE),
                            height=SIZE, bg=BKGD)
        frm.pack(side="left", fill="both")

        lbl_width = 40  # characters
        focus_label = UnderFocusLabel(frm, width=lbl_width, wraplength=int(0.61 * SIZE),
                                      bg=shade_color(BKGD, -0.05), justify="left")
        focus_label.pack(side="top", fill="both")

        focus_label.configure_circles(circles)

    if title is not None:
        draw_title(draw_can, title)

    if legend is not None:
        draw_legend(draw_can, legend)

    if colorscale is not None:
        draw_colorscale(draw_can, colorscale[0], colorscale[1], colorscale[2])

    return draw_can


def draw_title(can, title):
    """Draw the title"""
    title_frame = ttk.Frame(can.master)
    title_label = tk.Label(title_frame, text=title, background=BKGD)
    title_label.pack()
    title_frame.pack()


def draw_legend(can, legend):
    """Draw a legend on the canvas"""

    size = float(can['width'])
    unit = int(0.03 * size)

    x_pix = 2 * unit
    y_pix = 2 * unit

    for labl in legend:
        can.create_oval(x_pix - 0.5 * unit, y_pix - 0.5 * unit,
                        x_pix + 0.5 * unit, y_pix + 0.5 * unit,
                        fill=labl[1], outline=shade_color(labl[1], -0.2),
                        state='disabled')
        HighlightedText(labl[0], x_pix + 0.81 * unit, y_pix,
                        anchor='w').create_widget(can)
        y_pix += 1.62 * unit


def draw_colorscale(can, titlestr, minstr, maxstr, colormap=PAULT_BRIGHT):
    """Draw a colorscale on the canvas"""

    size = float(can['width'])
    unit = int(0.03 * size)

    x_pix = 2 * unit
    y_pix = unit

    can.create_text(x_pix, y_pix, text=titlestr, anchor="w")
    y_pix += 0.81 * unit

    for i, cmap in enumerate(colormap):
        can.create_oval(
            x_pix - 0.5 * unit,
            y_pix - 0.5 * unit,
            x_pix + 0.5 * unit,
            y_pix + 0.5 * unit,
            fill=cmap,
            outline=shade_color(cmap, -0.2),
        )
        if i == 0:
            can.create_text(x_pix + 0.81 * unit, y_pix, text=minstr, anchor="w")
        if i == len(colormap) - 1:
            can.create_text(x_pix + 0.81 * unit, y_pix, text=maxstr, anchor="w")

        y_pix += 0.81 * unit
