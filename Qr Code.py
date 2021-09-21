from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pyqrcode
import os
import cv2
from tkinter.filedialog import askopenfile

def write_QR():
    window = Tk()
    window.title("Qr Code Generator")
    window.configure(bg="#ffffff")

    def clear_subject():
        subjectEntry.delete(0, END)

    def clear_Filename():
        nameEntry.delete(0, END)

    def generate():
        subject = subjectEntry.get()
        if len(subject) != 0:
            global myQr
            myQr = pyqrcode.create(subject)
            qrImage = myQr.xbm(scale=6)
            global photo
            photo = BitmapImage(data = qrImage)
        else:
            messagebox.showerror("Error!", "Please Enter the Subject")

    def save():
        generate()
        #folder to save all the codes
        dir = path1 = os.getcwd() + "\\QR Codes"

        #Create a folder if it does not exist
        if not os.path.exists(dir):
            os.makedirs(dir)
        try:
            if len(nameEntry.get()) != 0:
                if os.path.exists(os.path.join(dir, nameEntry.get() + ".png")):
                    choice = messagebox.askquestion('Overwrite?', "QR Code with this filename already exists, Overwrite?")
                    if choice == 'yes':
                        qrImage = myQr.png(os.path.join(dir, nameEntry.get() + ".png"), scale = 6)
                        messagebox.showinfo("Saved", "Qr Code Saved to QR Codes folder")
                else:
                    qrImage = myQr.png(os.path.join(dir, nameEntry.get() + ".png"), scale = 6)
                    messagebox.showinfo("Saved", "Qr Code Saved to " + (os.path.join(dir, nameEntry.get() + ".png")))
            else:
                messagebox.showerror("Error!", "Filename can not be empty!")
        except NameError:
            messagebox.showerror("Error!", "Please Generate the QR Code first")
            
    ttk.Label(window, text="Enter Subject", font=("Helvetica", 12)).grid(row = 0, column = 0,pady = 10, padx = 10, sticky = N+S+E+W)

    ttk.Label(window, text="Enter File Name", font=("Helvetica", 12)).grid(row = 1, column = 0,pady = 10, padx = 10,  sticky = N+S+E+W)

    subjectEntry = ttk.Entry(window, font=("Helvetica", 12))
    subjectEntry.grid(row = 0, column = 1,pady = 10, padx = 10,  sticky = N+S+E+W)

    nameEntry = ttk.Entry(window, font=("Helvetica", 12))
    nameEntry.grid(row = 1, column = 1, pady = 10, padx = 10, sticky=N+S+E+W)

    ttk.Button(window, text="Clear Subject", width = 15, command = clear_subject).grid(row = 0, column = 2, pady = 10, padx = 10)

    ttk.Button(window, text="Clear Filename", width = 15, command = clear_Filename).grid(row = 1, column = 2, pady = 10, padx = 10)

    ttk.Button(window, text = "Generate QR & save as PNG", width = 15, command = save).grid(row = 2, column = 0,pady = 10, padx = 10, columnspan = 3,  sticky = N+S+E+W)

    #Making a responsive layout:
    totalRows = 2
    totalCols = 1

    for row in range(totalRows+1):
        window.grid_rowconfigure(row, weight=1)
    for col in range(totalCols+1):
        window.grid_columnconfigure(col, weight=1)
        
    window.mainloop()
    
def read_QR():
    read = Tk()
    read.title("Read QR")
    read.configure(bg="#ffffff")
    s = ttk.Style()
    s.configure('TLabel', bg="#ffffff")
    ttk.Label(read, text = "Select the Image", style="TLabel", font=("Helvetica", 12)).grid(row = 0, column = 0, pady = 10, padx = 10)
    file = ttk.Entry(read, width = 50)
    ttk.Label(read, text = "Enter File name", style="TLabel", font=("Helvetica", 12)).grid(row = 1, column = 0, pady = 10, padx = 10)
    name_entry = ttk.Entry(read, width = 50)

    def clear():
        global result
        name_entry.delete(0, END)
        file.delete(0, END)
        try:
            result.grid_forget()
        except NameError:
            pass
    def open_image():
        file.delete(0, END)
        file_name = askopenfile(filetypes = [('png files', '*.png'), ('jpg files', '*.jpg')])
        if file_name is not None:
            file.insert(0, file_name.name)
    def read_now():
        try:
            global data, result
            try:
                if result:
                    result.grid_forget()
            except NameError:
                pass
            filename = file.get()
            img  = cv2.imread(filename)
            detector = cv2.QRCodeDetector()
            data, bbox, straight_qrcode = detector.detectAndDecode(img)
            if data == '':
                messagebox.showerror("Overflow!!", "Data Stored in Image was too large")

            if bbox is not None:
                result = Label(read, text = "Data = " + data, borderwidth = 3, relief = "sunken", fg="white", bg="red")
                result.grid(row = 3, column = 0, columnspan = 2)
        except:
            messagebox.showerror("Invalid Image", "Please select a valid image to read data From")
    def save():
        global data
        #folder to save all the codes
        dir = path1 = os.getcwd() + "\\QR Codes"
        try:
            #Create a folder if it does not exist
            if not os.path.exists(dir):
                os.makedirs(dir)
            if len(name_entry.get()) != 0:
                if os.path.exists(os.path.join(dir, name_entry.get() + ".txt")):
                    choice = messagebox.askquestion('Overwrite?', "Data with this filename already exists, Overwrite?")
                    if choice == 'yes':
                        file = open((os.path.join(dir, name_entry.get() + ".txt")), "a")
                        file.write(data)
                        file.write("\n")
                        file.close()
                        messagebox.showinfo("Saved!!", "Data saved in " + (os.path.join(dir, name_entry.get() + ".txt")))
                else:
                    file = open((os.path.join(dir, name_entry.get() + ".txt")), "a")
                    file.write(data)
                    file.write("\n")
                    file.close()
                    messagebox.showinfo("Saved!!", "Data saved in " + (os.path.join(dir, name_entry.get() + ".txt")))
            else:
                messagebox.showerror("Error!", "Filename can not be empty!")
        except NameError:
            messagebox.showerror("Data not found", "Please Extract data From QR Code first")

    ttk.Button(read, text='Browse Image', width = 15, command = open_image).grid(row = 0, column = 2, pady = 10, padx = 10)
    ttk.Button(read, text = "Read", width = 15, command = read_now).grid(row = 2, column = 1, pady = 10, padx = 10)
    ttk.Button(read, text = "Save", width = 15, command = save).grid(row = 1, column = 2, pady = 10, padx = 10)
    ttk.Button(read, text = "Clear", width = 15, command = clear).grid(row = 2, column = 0, pady = 10, padx = 10)
    file.grid(row = 0, column = 1, pady = 10, padx = 10)
    name_entry.grid(row = 1, column = 1, pady = 10, padx = 10)

    totalRows = 2
    totalCols = 1
    for row in range(totalRows + 1):
             read.grid_rowconfigure(row, weight=1)
    for col in range(totalCols + 1):
             read.grid_columnconfigure(col, weight=1)
    read.mainloop()
    
if __name__ == "__main__":
    gui = Tk()
    gui.configure(bg="Black")
    gui.title("QR Code")
    gui.configure(bg="#ffffff")
    s = ttk.Style()
    s.configure('TLabel', background='#ffffff')
    ttk.Label(gui, text = "QR Code", font=("Times", 30), style="TLabel").grid(row = 0, column = 0, columnspan = 2)
    generate = ttk.Button(gui, text = "Generate QR", width = 15, command = write_QR).grid(row = 1, column = 0, pady = 10, padx = 10)
    read = ttk.Button(gui, text = "Read QR", width = 15, command = read_QR).grid(row = 1, column = 1, pady = 10, padx = 10)
    totalRows = 1
    totalCols = 1
    for row in range(totalRows + 1):
            gui.grid_rowconfigure(row, weight=1)
    for col in range(totalCols + 1):
            gui.grid_columnconfigure(col, weight=1)
    gui.mainloop()
