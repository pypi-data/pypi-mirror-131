import sys
from typing import Optional, Tuple, Union

from sty import RgbFg, Style, bg, ef, fg, rs

"""To know more about sty module
https://github.com/feluxe/sty
"""
# Eg to create a new color
fg.orange = Style(RgbFg(255, 150, 50))


def aprint(
    *args,
    sup_err: Optional[bool] = True,
    sep: Optional[str] = " ",
    end: Optional[str] = "\n",
    same_line: Optional[bool] = False,
    flush: Optional[bool] = False,
    **kwargs
):
    """Alternative Print\n
    Eg:\n
        ("a--", (10, 15, 20), "b--", "red", "g--", "green", sep="\\n")\n
        ("Prints in green","green")

    Args:
        sup_err (bool, optional): Suppress errors/exceptions showing on terminal. Defaults to False.
        sep (str, optional): seperator used if the elements are more than 1 to print. Defaults to " ".
    """
    for i in range(0, len(args), 2):
        try:
            clr = args[i + 1]
            ender = fg.rs
            if type(clr) == int:
                para = fg(clr)
            elif type(clr) == str:
                try:
                    para = fg.__getattribute__(clr)
                except Exception as e:
                    if not sup_err:
                        print("-" * 20)
                        print(e)
                        print(
                            "\tTry to create custom color using sty module as shown below"
                        )
                        print("\tfg.orange = Style(RgbFg(255, 150, 50))")
                        print("-" * 20)
                    para, ender = "", ""
            elif len(clr) == 3:
                para = fg(*clr)
            else:
                continue
        except:
            para = ""
            ender = ""
        if i >= len(args) - 2:
            sep = ""
        print(para + str(args[i]) + ender, end=sep, flush=flush)
    if same_line:
        print(end="\r", flush=flush)
        sys.stdout.write("\033[K")
    else:
        print(end=end, flush=flush)


def printInfo(
    i_sym: str,
    i_clr: Union[int, str, Tuple[int, int, int]],
    b_clr: Union[int, str, Tuple[int, int, int]],
    *args,
    sup_err: Optional[bool] = True,
    sep: Optional[str] = " ",
    end: Optional[str] = "\n",
    same_line: Optional[bool] = False,
    flush: Optional[bool] = False,
    **kwargs
):
    aprint("[", b_clr, i_sym, i_clr, "] ", b_clr, sep="", end="")
    aprint(*args, sup_err=sup_err, sep=sep, end=end, same_line=same_line)


def deleteLines(n=1):
    """Delete 'n' last lines

    Args:
        n (int, optional): number of lines. Defaults to 1.
    """
    for _ in range(n):
        sys.stdout.write("\x1b[1A")  # cursor up
        sys.stdout.write("\x1b[2K")  # erase line
