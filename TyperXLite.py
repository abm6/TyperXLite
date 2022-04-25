import time
from pynput.keyboard import Key, Controller
import tkinter as tk
import tkinter.ttk as ttk

keyboard = Controller()


class UI:

    def __init__(self, root):
        self.root = root
        self.root.geometry("400x200")
        self.root.minsize(400, 400)
        self.root.maxsize(800, 600)

    def createWidgets(self, inputWindow=None):
        keyStrokeDelayValues = ["0.01", "0.05", "0.07", "0.10"]
        startDelayValues = ["2", "5", "10", "15"]

        # Top Frame and subframes
        self.frame1 = tk.Frame(self.root, bg="#eaeaea")
        self.frame1.pack(fill='both')
        self.keyStrokeDelay = tk.StringVar()
        self.keyStrokeDelay.set(keyStrokeDelayValues[0])
        self.startDelay = tk.StringVar()
        self.startDelay.set(startDelayValues[1])

        #Text Box Frame
        self.text_box = InputWindow(self.root)
        self.text_box.txt.config(font=("consolas", 12), undo=True, wrap='word')
        self.text_box.txt.config(borderwidth=3, relief="sunken")

        #Footer Frame
        self.footer = tk.Label(self.root, text="")

        # plotting the frames
        self.keyStrokeIntervalMenuLabel = tk.Label(
            self.frame1, text="Key stroke Interval").pack(side=tk.LEFT)

        self.keyStrokeIntervalMenu = tk.OptionMenu(
            self.frame1, self.keyStrokeDelay,
            *keyStrokeDelayValues).pack(side=tk.LEFT)

        self.delay = tk.OptionMenu(self.frame1, self.startDelay,
                                   *startDelayValues).pack(side=tk.RIGHT)

        self.delayLabel = tk.Label(
            self.frame1, text="Start Typing after").pack(side=tk.RIGHT)

        self.text_box.pack(fill="both", expand=True)

        self.footer.pack(side=tk.BOTTOM)

        ttk.Style().theme_use('clam')

    def createStartButton(self, tm):

        self.startButton = tk.Button(self.root,
                                     text="Start Typing",
                                     command=tm.startTyping,
                                     fg="black",
                                     bg="skyblue")
        self.startButton.pack(side=tk.BOTTOM)
        return self.startButton


class TextManager:

    def __init__(self, ui, text_box, footer):

        self.text_box = text_box
        self.footer = footer
        self.ui = ui

    def startTyping(self):

        text = self.text_box.get()

        strokeDelay = float(self.ui.keyStrokeDelay.get())
        startDelay = float(self.ui.startDelay.get())

        while startDelay > 0:
            self.footer.configure(
                text=f"Processing in {str(int(startDelay))} seconds")
            self.footer.update()
            startDelay -= 1
            time.sleep(1)

        start = time.time()

        for char in text:
            if char == '\n':
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
            else:
                keyboard.press(char)
                keyboard.release(char)

            time.sleep(strokeDelay)

        end = time.time()
        self.footer.configure(
            text=f"Task completed in {round(end-start,2)} seconds")


class InputWindow(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ensure a consistent GUI size
        self.grid_propagate(False)

        # implement stretchability
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create a Text widget
        self.txt = tk.Text(self)
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # create a Scrollbar and associate it with txt
        scrollb = ttk.Scrollbar(self, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')

        self.txt['yscrollcommand'] = scrollb.set

    def get(self):
        return self.txt.get("1.0", "end-1c")


def main():
    root = tk.Tk()
    root.title("TyperX Lite")

    ui = UI(root)

    ui.createWidgets()

    footer = ui.footer
    text_box = ui.text_box

    #manipulate and do typing emulations
    tm = TextManager(ui, text_box, footer)

    # Creating the start button and passing the reference of the text manager object
    startButton = ui.createStartButton(tm)

    root.mainloop()


if __name__ == "__main__":
    main()
