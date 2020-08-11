import tkinter.filedialog as filedialog
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import re
from PyPDF2 import PdfFileReader
import os
import subprocess
import cups
import time


class PyPrinter(object):

    def __init__(self, **kw):
        self.root = tk.Tk()
        self.root.title('Duplex Printer')
        self.padding = (10, 10)
        self.font_size = 14
        self.font_family = "Helvetica"

        self.welcome_label = tk.Label(text = "Want to print you file in a manual duplex?",
                 font=tkFont.Font(family=self.font_family, size=self.font_size)).grid(row=0,column=0, pady = (10,2),
                                              sticky="wens", padx = self.padding)
        self.welcome_label2 = tk.Label(text = "Search for the file bellow",
                 font=tkFont.Font(family=self.font_family, size=self.font_size)).grid(row=1,column=0, pady = self.padding,
                                              sticky="wens", padx = self.padding)
        self.search_button = tk.Button(text='Find the File',command=self.printer).grid(row=2,
         column=0, pady =(2,2), padx = self.padding)

    def execute(self):
        self.root.mainloop()

    def printer(self):
        self.name = filedialog.askopenfilename()
        self.conn = cups.Connection ()
        pdf = PdfFileReader(open(self.name,'rb'))
        self.pages = pdf.getNumPages()
        print(self.root.winfo_width())

        self.name_label = tk.Message(text =self.name.split("/")[-1], font=tkFont.Font(family=self.font_family, size=self.font_size), width=self.root.winfo_width()-20).grid(row=3,
         column=0, pady = self.padding,sticky="wens", padx = self.padding)
        self.pages_label = tk.Label(text = "Pages: "+ str(self.pages), font=tkFont.Font(family=self.font_family, size=self.font_size)).grid(row=4,
          column=0, pady = self.padding,sticky="wens", padx = self.padding)
        printers_list = self.conn.getPrinters()
        printers = []
        for printer in printers_list:
            printers.append(printer)


        self.printer = tk.Label(text = "Select the Printer:",
                 font=tkFont.Font(family=self.font_family, size=self.font_size)).grid(row=5,column=0, pady = (10,2),
                                              sticky="wens", padx = self.padding)
        self.printers  = ttk.Combobox(self.root,
                            values=printers)
        self.printers.bind("<<>ComboboxSelected>")
        self.printers.grid(row=6, column=0, pady = self.padding, padx = self.padding)


        self.print_button = tk.Button(text='Print!',command=self.send_print_first).grid(row=7,
         column=0, pady = self.padding, padx = self.padding)

    def popupmsg(self):
        self.popup = tk.Toplevel(self.root)
        self.popup.wm_title("!")
        self.popup.tkraise(self.root) # This just tells the message to be on top of the root window.
        tk.Label(self.popup ,text = "Hey, i finished to print the first part",
                 font=tkFont.Font(family=self.font_family, size=self.font_size)).grid(row=0,column=0, pady = (10,2),
                                              sticky="wens", padx = self.padding)
        tk.Label(self.popup ,text = "Grab you paper on the long side, turn it and insert into the printer",
                 font=tkFont.Font(family=self.font_family, size=self.font_size)).grid(row=1,column=0, pady = (10,2),
                                              sticky="wens", padx = self.padding)

        tk.Button(self.popup, text="Okay! Continue", command = self.send_print_2).grid(row=2,column=0, pady = (10,2),
                                     sticky="wens", padx = self.padding)

    def send_print_2(self):
        self.popup.destroy
        second_side = ",".join([str(i) for i in range(int(35+1)) if i%2 ==0])

        printid = self.conn.printFile(self.printers.get(), self.name, "PyPrinter First Side", {"page-ranges":second_side, "print-quality":"4"})
        while self.conn.getJobs().get(printid, None) is not None:
            time.sleep(1)

    def send_print_first(self):
        first_side = ",".join([str(i) for i in range(int(35+1)) if i%2 !=0])

        printid = self.conn.printFile(self.printers.get(), self.name, "PyPrinter First Side", {"page-ranges":first_side, "print-quality":"4"})
        while self.conn.getJobs().get(printid, None) is not None:
            time.sleep(1)

        self.popupmsg()

PyPrinter().execute()
