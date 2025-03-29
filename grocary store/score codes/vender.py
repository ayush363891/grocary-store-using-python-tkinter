from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import os
import sys

class Vendor:
    def __init__(self, root):
        self.root = root
        #self.customer_data = customer_data or {}
        #print("Vendor customer_data:", self.customer_data)
        
        self.root.title("Vendor Zone")
        self.root.geometry("1550x900+0+0")
        
        # Store image references to prevent garbage collection
        self.photo_images = []
        
        # Title Bar
        lbl_title = Label(self.root, text="Grocery Store", font=("times new roman", 20, "bold"), 
                         bg="black", fg="gold")
        lbl_title.place(x=0, y=0, width=1550, height=50)

        # Back button
        lbl_btn = Button(self.root, text="Back To Login", font=("times new roman", 20, "bold"),
                        command=self.back, bg="black", fg="gold", cursor="hand2")
        lbl_btn.place(x=0, y=0, width=200, height=50)

        # Vendor 1 Section
        lbl_ven1 = Label(self.root, text="Vendor 1", font=("times new roman", 18, "bold"), 
                         bg="black", fg="gold")
        lbl_ven1.place(x=400, y=150, width=100, height=40)

        try:
            img1 = Image.open("images/vendor1.jpg")
            img1 = img1.resize((500, 400), Image.Resampling.LANCZOS)
            self.photo_img1 = ImageTk.PhotoImage(img1)
            self.photo_images.append(self.photo_img1)
            
            btn1 = Button(self.root, image=self.photo_img1, command=self.open_vendor1, 
                         borderwidth=0, cursor="hand2")
            btn1.place(x=200, y=230, width=500, height=400)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Vendor 1 image: {str(e)}")
            btn1 = Button(self.root, text="Vendor 1\n(Image Missing)", 
                         font=("times new roman", 20, "bold"), command=self.open_vendor1)
            btn1.place(x=200, y=230, width=500, height=400)

        # Vendor 2 Section
        lbl_ven2 = Label(self.root, text="Vendor 2", font=("times new roman", 18, "bold"), 
                         bg="black", fg="gold")
        lbl_ven2.place(x=1050, y=150, width=100, height=40)

        try:
            img2 = Image.open("images/vendor2.jpg")
            img2 = img2.resize((500, 400), Image.Resampling.LANCZOS)
            self.photo_img2 = ImageTk.PhotoImage(img2)
            self.photo_images.append(self.photo_img2)
            
            btn2 = Button(self.root, image=self.photo_img2, command=self.open_vendor2, 
                         borderwidth=0, cursor="hand2")
            btn2.place(x=850, y=230, width=500, height=400)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Vendor 2 image: {str(e)}")
            btn2 = Button(self.root, text="Vendor 2\n(Image Missing)", 
                         font=("times new roman", 20, "bold"), command=self.open_vendor2)
            btn2.place(x=850, y=230, width=500, height=400)

    def open_vendor1(self):
        """Open Vendor 1 interface"""
        try:
            # Destroy current window first
            self.root.destroy()
            
            # Create new root window for Vendor1
            new_root = Tk()
            try:
                from .vendor1 import Vendor1
                app = Vendor1(new_root)
            except ImportError as e:
                messagebox.showerror("Import Error", f"Failed to import Vendor1: {str(e)}")
                self.root.deiconify()
                return
            new_root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Vendor 1: {str(e)}")
            # Restore the main window if Vendor1 fails
            self.root.deiconify()

    def open_vendor2(self):
        """Open Vendor 2 interface"""
        try:
            self.root.destroy()
            new_root = Tk()
            try:
                from .vendor2 import Vendor2
                app = Vendor2(new_root)
            except ImportError as e:
                messagebox.showerror("Import Error", f"Failed to import Vendor2: {str(e)}")
                self.root.deiconify()
                return
            new_root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Vendor 2: {str(e)}")
            # Restore the main window if Vendor2 fails
            self.root.deiconify()

    def back(self):
        """Return to login page"""
        try:
            self.root.destroy()  # Close current window
            from login import Login_page
            login_root = Tk()
            Login_page(login_root)
            login_root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return to login: {str(e)}")

    def on_close(self):
        """Handle window close event"""
        if messagebox.askokcancel("Quit", "Do you want to close the Vendor window?"):
            self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    app = Vendor(root)
    root.mainloop()