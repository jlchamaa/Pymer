from pymer.session import session
import Tkinter as tk


def main():
    root = tk.Tk()
    sesh = session(root)
    root.mainloop()
try:
    main()
except ValueError as ex:
    if str(ex) == 'toosmall':
        print("Window too narrow.  Try resizing!")
    else:
        raise
