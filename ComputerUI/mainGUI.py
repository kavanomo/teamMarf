# Main gui for the desktop control of the

from tkinter import *
from tkinter import messagebox


def colourSortUi():
    class Application(Frame):

        def __init__(self, master=None):
            Frame.__init__(self, master)
            self.pack()
            self.createWidgets()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            sys.exit("Window closed.")

    root = Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app = Application(master=root)
    root.title("Unit Testing GUI")
    root.geometry('+%d+%d' % (200, 200))
    app.mainloop()
    root.destroy()
    print('Colour!')


def valueSortUi():
    print('Value!')


def catalogueSortUi():
    print('Catalogue!')


def startScreen():
    class Application(Frame):

        def createWidgets(self):
            top = Frame(root)
            bottom = Frame(root)
            top.pack(side=TOP)
            bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

            Label(text='Welcome to Cardobot', font=('Helvetica', 19)).pack(in_=top)

            colourSort = Button(text="Colour Sort", command=colourSortUi, bd=2, height=2, width=25, bg="green",
                                font=("Helvetica", 15))

            valueSort = Button(text="Value Sort", command=valueSortUi, bd=2, height=2, width=25, bg="green",
                               font=("Helvetica", 15))

            catalogueSort = Button(text="Catalogue", command=catalogueSortUi, bd=2, height=2, width=25, bg="green",
                                   font=("Helvetica", 15))

            quitSystem = Button(text="Production Setup", command=on_closing, bd=2, height=2, width=25, bg="red",
                                font=("Helvetica", 15))

            colourSort.pack(in_=top)
            valueSort.pack(in_=top)
            catalogueSort.pack(in_=top)
            quitSystem.pack(in_=top)

        def __init__(self, master=None):
            Frame.__init__(self, master)
            self.pack()
            self.createWidgets()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            sys.exit("Window closed.")

    root = Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app = Application(master=root)
    root.title("Unit Testing GUI")
    root.geometry('+%d+%d' % (200, 200))
    app.mainloop()
    root.destroy()


def main():
    startScreen()

if __name__ == '__main__':
    main()