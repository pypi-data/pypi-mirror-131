# pylint: disable=R0914
import os
import re
import datetime
import threading
from tkinter import ttk, N, W, E, S, StringVar, Tk
from plyer import notification
from playsound import playsound

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
W_WIDTH = 200
W_HEIGHT = 220


def format_time(sec):
    return str(datetime.timedelta(seconds=sec))


def validate_number(newval):
    return re.match("^[0-9]*$", newval) is not None


class Clock:
    def __init__(self, timeout=10, on_update=None, on_ready=None):
        self.__timeout = timeout
        self.__interval = None
        self.on_update = on_update
        self.on_ready = on_ready

    def __set_interval(self, sec):
        def func_wrapper():
            self.__interval = self.__set_interval(sec)
            self.__timeout -= 1
            if self.on_update is not None:
                self.on_update(self.get_timeout())
            if self.__timeout <= 0:
                self.stop()
                if self.on_ready is not None:
                    self.on_ready()

        timer = threading.Timer(sec, func_wrapper)
        timer.start()
        return timer

    @property
    def running(self):
        return self.__interval is not None

    def start(self):
        self.__interval = self.__set_interval(1)

    def stop(self):
        if self.__interval is not None:
            self.__interval.cancel()
        self.__interval = None

    def set_timeout(self, timeout):
        self.__timeout = timeout

    def get_timeout(self):
        return self.__timeout


class Pomodoro(Tk):
    def __init__(self):
        super().__init__()
        self.title("Pomodoro")
        self.geometry(f"{W_WIDTH}x{W_HEIGHT}")

        # Store time limit in minutes
        self.max_limit = StringVar(value="5")

        timeout = StringVar(value=format_time(self.get_limit()))
        validate_num_wrapper = (self.register(validate_number), "%P")

        frame = ttk.Frame(self, padding="3 3 12 12")
        clock = ttk.Label(frame, textvariable=timeout, font=("TkHeadingFont", 24))
        clock.configure(anchor="center")
        restart = ttk.Button(frame, text="Start Clock", command=self.restart_clock)
        pause = ttk.Button(frame, text="Pause", command=self.toggle_clock)
        dec_max_limit = ttk.Button(
            frame, text="-", width=2, command=self.decrement_limit
        )
        inc_max_limit = ttk.Button(
            frame, text="+", width=2, command=self.increment_limit
        )
        fill_text = ttk.Label(frame, text="minutes")
        limit = ttk.Entry(
            frame,
            width=4,
            textvariable=self.max_limit,
            validate="key",
            validatecommand=validate_num_wrapper,
        )
        pre_5_min = ttk.Button(
            frame, text="5 min.", command=lambda: self.max_limit.set(5)
        )
        pre_10_min = ttk.Button(
            frame, text="10 min.", command=lambda: self.max_limit.set(10)
        )
        pre_25_min = ttk.Button(
            frame, text="25 min.", command=lambda: self.max_limit.set(25)
        )
        pre_30_min = ttk.Button(
            frame, text="30 min.", command=lambda: self.max_limit.set(30)
        )

        for child in frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        frame.grid(row=0, column=0, sticky=(N, W, E, S))
        clock.grid(row=0, column=0, columnspan=4, sticky=(W, E))
        dec_max_limit.grid(row=1, column=0, sticky=W)
        limit.grid(row=1, column=1)
        inc_max_limit.grid(row=1, column=2)
        fill_text.grid(row=1, column=3, sticky=E)
        restart.grid(row=2, column=0, columnspan=2, sticky=W)
        pause.grid(row=2, column=2, columnspan=2, sticky=E)
        pre_5_min.grid(row=3, column=0, columnspan=2, sticky=W)
        pre_10_min.grid(row=3, column=2, columnspan=2, sticky=E)
        pre_25_min.grid(row=4, column=0, columnspan=2, sticky=W)
        pre_30_min.grid(row=4, column=2, columnspan=2, sticky=E)

        def clock_update(seconds):
            timeout.set(format_time(seconds))

        def clock_ready():
            timeout.set(format_time(0))
            playsound(os.path.join(BASE_DIR, "assets", "alarm-default.mp3"))
            notification.notify(
                title="Time's Up!",
                message="Your timer has reached 0",
                app_icon=None,
                timeout=25,
            )

        self.__clock = Clock(on_update=clock_update, on_ready=clock_ready)

    def get_limit(self):
        """Return max tim limit in seconds"""
        return int(self.max_limit.get()) * 60

    def increment_limit(self):
        newval = int(self.max_limit.get()) + 1
        self.max_limit.set(newval)

    def decrement_limit(self):
        oldval = int(self.max_limit.get())
        if oldval <= 1:
            return
        self.max_limit.set(oldval - 1)

    def restart_clock(self, *args):  # pylint: disable=W0613
        self.__clock.stop()
        self.__clock.set_timeout(self.get_limit())
        self.__clock.start()

    def stop_clock(self):
        self.__clock.stop()

    def toggle_clock(self):
        if self.__clock.running:
            self.__clock.stop()
        else:
            self.__clock.start()


def main():
    app = Pomodoro()
    app.mainloop()
    app.stop_clock()
