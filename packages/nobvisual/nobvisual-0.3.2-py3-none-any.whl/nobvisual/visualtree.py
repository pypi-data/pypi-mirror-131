"""
Draw the circular packing of a folder tree.
===========================================

"""

import os
from glob import glob
import math
from ctypes import c_int64  # a mutable int
import tkinter as tk

from nobvisual.tkinter_circlify import tkcirclify
from nobvisual.helpers import from_nested_struct_to_nobvisual
from nobvisual.objects import VisualTreeClickBehavior


COLOR_BINARY = "#00ccff"
COLOR_ASCII = "#ffcc00"

__all__ = ["visual_tree"]


def visual_tree(tgt=None, max_recursion=3, start_mainloop=True):
    """Show the circular nested packing of a directory tree.

    The circular packing is computed using the circlify package.
    The graphical output is done using tkinter.
    Area of circles is proportional to lthe log10 of file sizes.
    ASCII-UTF8 files are blue, others (usually Binary)  are in green.

    :params wdir: path to a working directory. If None, set to current working directory.

    No returns.
    -----------

    Open a tkinter window with the circular packing.
    """
    if tgt is None:
        tgt = os.getcwd()

    nstruct = scan_wdir(tgt, max_recursion=max_recursion)

    circles = from_nested_struct_to_nobvisual(nstruct)
    click_behavior = VisualTreeClickBehavior()
    for circle in circles:
        circle.click_behavior = click_behavior

    draw_canvas = tkcirclify(
        circles,
        color="#eeeeee",
        legend=[("binary", COLOR_BINARY), ("ascii", COLOR_ASCII), ],
        title=f"Showing {str(tgt)}",
        show_under_focus=False,
    )
    draw_canvas.show_leaf_short_names()

    # make full name for leaf children of enclosing circle
    enclosing_circle = draw_canvas.find_enclosing_circle()
    for circle in enclosing_circle.children:
        if circle.is_leaf():
            circle.show_name()

    if start_mainloop:
        tk.mainloop()


def scan_wdir(wdir, max_recursion=3):
    """ Build the structure of a folder tree.

    :params wdir: path to a directory
    """
    n_wdir = len(os.path.normpath(wdir).split(os.sep))

    def _rec_subitems(path, recursion_level, item_id):
        name = os.path.split(path)[-1]

        item_id.value += 1
        out = {
            "id": item_id.value,
            "datum": 1.0,
            "name": name,
            "text": f"./{'/'.join(os.path.normpath(path).split(os.sep)[n_wdir:])}"
        }
        if os.path.isfile(path):
            out["short_name"] = os.path.splitext(path)[-1]  # ext

            path_size = os.path.getsize(path)
            size = math.log10(path_size) if path_size > 0 else 1

            try:
                with open(path, "r", encoding="utf8") as fin:
                    fin.readline()
                out["color"] = COLOR_ASCII
            except UnicodeDecodeError:
                out["color"] = COLOR_BINARY

            out["datum"] = size

        elif recursion_level >= max_recursion:
            pass  # does not modify 'out' and breaks recursion

        else:
            size = 0
            out["children"] = list()
            for nexpath in glob(os.path.join(path, "**")):
                record = _rec_subitems(nexpath, recursion_level + 1, item_id)
                size += record["datum"]
                out["children"].append(record)
            out["datum"] = size
            out["color"] = "default"

        return out

    out = [_rec_subitems(wdir, 0, item_id=c_int64(-1))]

    return out
