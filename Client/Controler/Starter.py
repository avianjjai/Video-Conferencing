from tkinter import *
from View.Ide import IDE

def main():
    root = Tk()
    root.resizable(width=False, height=False)
    application = IDE(root, width=800, height=600, bg='#B49D98')
    root.mainloop()