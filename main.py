#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import serial


class Setup3DApp:
    def __init__(self, master=None):
        # build ui with pygubu designer
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=200, width=600)
        toplevel1.title("Longer LK4 pro BLTouch Setup")
        frame1 = ttk.Frame(toplevel1)
        frame1.configure(height=200, width=200)
        self.entry_com = ttk.Entry(frame1)
        self.entry_com.configure(state="normal")
        self.entry_com.grid(column=0, row=0)
        self.button_init = ttk.Button(frame1)
        self.button_init.configure(text='Init')
        self.button_init.grid(column=0, row=1)
        self.button_init.configure(command=self.on_click_init)
        self.button_get_z = ttk.Button(frame1)
        self.button_get_z.configure(text='Get Z')
        self.button_get_z.grid(column=0, row=2)
        self.button_get_z.configure(command=self.on_click_get_z)
        self.entry_z = ttk.Entry(frame1)
        self.entry_z.configure(state="normal", takefocus=True)
        self.entry_z.grid(column=0, row=3)
        self.button_save_z = ttk.Button(frame1)
        self.button_save_z.configure(text='Save Z')
        self.button_save_z.grid(column=1, row=3)
        self.button_save_z.configure(command=self.on_click_save_z)
        self.button_goto_z0 = ttk.Button(frame1)
        self.button_goto_z0.configure(text='Goto Z0')
        self.button_goto_z0.grid(column=0, row=4)
        self.button_goto_z0.configure(command=self.on_click_goto_z0)
        self.button_open_com = ttk.Button(frame1)
        self.button_open_com.configure(
            default="normal", state="normal", text='Open COM')
        self.button_open_com.grid(column=1, row=0)
        self.button_open_com.configure(command=self.on_click_open_com)
        self.button_goto_z10 = ttk.Button(frame1)
        self.button_goto_z10.configure(text='Goto Z10')
        self.button_goto_z10.grid(column=0, row=5)
        self.button_goto_z10.configure(command=self.on_click_goto_z10)
        frame1.grid(column=0, row=0)
        frame1.columnconfigure(0, minsize=100)
        frame2 = ttk.Frame(toplevel1)
        frame2.configure(height=200, width=200)
        self.console = tk.Text(frame2)
        self.console.configure(
            background="#000000",
            exportselection="false",
            foreground="#5fe262",
            height=10,
            insertunfocussed="none",
            state="disabled",
            width=50,
            wrap="none")
        self.console.grid(column=0, row=0)
        frame2.grid(column=1, row=0)
        toplevel1.bind("<Destroy>", self.close_app, add="")

        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()

    def on_click_open_com(self):
        self.serial_port = serial.Serial(
            port=self.entry_com.get(), baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
        )
        self.mainwindow.after(50, self.read_serial)

    def on_click_init(self):
        self.serial_port.write(b'M851 Z0\nG28\nG1 F60 Z0\nM211 S0\n')

    def on_click_get_z(self):
        self.serial_port.write(b'M114\n')

    def on_click_save_z(self):
        self.serial_port.write(b'M851 Z'+bytes(self.entry_z.get(), 'ascii')+b'\nM500\nM211 S1\nG28 Z0\n')

    def on_click_goto_z0(self):
        self.serial_port.write(b'G1 F60 Z10\n')
        self.serial_port.write(b'G1 F60 Z0\n')

    def on_click_goto_z0(self):
            self.serial_port.write(b'G1 F60 Z10\n')

    def close_app(self, event=None):
        self.serial_port.close()
        print("com Closed")
        # self.mainwindow.destroy()

    def read_serial(self):
        if self.serial_port.inWaiting() > 0:
            # read the bytes and convert from binary array to ASCII
            data_str = self.serial_port.read(self.serial_port.inWaiting()).decode('ascii')
            # print the incoming string without putting a new-line
            # ('\n') automatically after every print()
            num_lines = int(self.console.index('end - 1 line').split('.')[0])
            self.console['state'] = 'normal'
            print(num_lines)
            if num_lines == 10:
                self.console.delete(1.0, 2.0)
            self.console.insert('end-1c', data_str)
            self.console['state'] = 'disabled'

        self.mainwindow.after(50, self.read_serial)



if __name__ == "__main__":
    app = Setup3DApp()
    app.run()

