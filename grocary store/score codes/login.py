from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from PIL.Image import Resampling
from tkinter import messagebox

import mysql.connector

class Login_page:
    def __init__(self, root):
        self.root = root
        self.root.title("Login page")
        self.root.geometry("1920x1080+0+0")

        img1 = Image.open(r"C:\Users\ayush\OneDrive\Desktop\grocary store\images\Login_bg_img.jpg")
        img1 = img1.resize((1530, 900), Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img1)

        imglbl = Label(self.root, image=self.photoimg, bd=1, relief=RIDGE)
        imglbl.place(x=0, y=0, width=1530, height=900)

        # ===================== Login Frame =========================
        lgn_frame = Frame(self.root, bg="#ffffe4")
        lgn_frame.place(x=570, y=200, width=380, height=500)

        img2 = Image.open(r"C:\Users\ayush\OneDrive\Desktop\grocary store\images\logo.jpg")
        img2 = img2.resize((100, 100), Image.LANCZOS)  # Resize image
        self.photoimg2 = ImageTk.PhotoImage(img2)
        # Display in Label
        lbl_img2 = Label(self.root, image=self.photoimg2, bg="black", borderwidth=0)
        lbl_img2.place(x=715, y=210, width=100, height=100)

        lbl_get_started = Label(self.root, text="Get Started", font=("times now roman", 16, "bold"), bg="#ffffe4", fg="black")
        lbl_get_started.place(x=705, y=310)
        # ============================ username ===========================
        img3 = Image.open(r"C:\Users\ayush\OneDrive\Desktop\grocary store\images\288592.jpg").resize((28, 28), Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        lbl_img3 = Label(self.root, image=self.photoimg3, bg="black")
        lbl_img3.place(x=630, y=370, width=28, height=28)

        lbl_user = Label(self.root, text="Username", font=("times new roman", 15, "bold"), bg="#ffffe4", fg="black")
        lbl_user.place(x=665, y=370)
        self.txt_user = ttk.Entry(self.root, font=("times new roman", 15, "bold"), width=25)
        self.txt_user.place(x=630, y=400)
        # ============================== Password ===========================
        img4 = Image.open(r"C:\Users\ayush\OneDrive\Desktop\grocary store\images\lock-512.jpg").resize((28, 28), Resampling.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)
        lbl_img4 = Label(self.root, image=self.photoimg4, bg="black")
        lbl_img4.place(x=630, y=450, width=28, height=28)

        lbl_pass = Label(self.root, text="Password", font=("times new roman", 15, "bold"), bg="#ffffe4", fg="black")
        lbl_pass.place(x=665, y=450)
        self.txt_pass = ttk.Entry(self.root, font=("times new roman", 15, "bold"), width=25, show="*")
        self.txt_pass.place(x=630, y=480)

        # ================= buttons =================
        lgn_btn = Button(self.root, text="Login", command=self.log, font=("times new roman", 12, "bold"), bg="green", fg="white", relief=RIDGE)
        lgn_btn.place(x=720, y=530)

        regi_btn = Button(self.root, text="New User Registration", command=self.regi, font=("times new roman", 12, "bold"), borderwidth=0, bg="#ffffe4", fg="black", activebackground="black", activeforeground="white", relief=RIDGE)
        regi_btn.place(x=640, y=580)

        frg_pas_btn = Button(self.root, command=self.forgot_password, text="Forgot Password", font=("times new roman", 12, "bold"), bg="#ffffe4", fg="#fa4224", activebackground="black", activeforeground="white", relief=RIDGE, borderwidth=0)
        frg_pas_btn.place(x=640, y=610)

    def log(self):
        if self.txt_user.get() == "" or self.txt_pass.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        elif self.txt_user.get()=="admin" and self.txt_pass.get()=="admin":
            self.new_window=Toplevel(self.root)
            from shop1 import Shop1
            self.app=Shop1(self.new_window)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="1234", database="grocarystore")
                my_cursor = conn.cursor()
                my_cursor.execute("SELECT * FROM cust_register WHERE email=%s AND password=%s", (
                    self.txt_user.get(),
                    self.txt_pass.get()
                ))
                row = my_cursor.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid username and password", parent=self.root)
                else:
                    # Corrected to match your table structure
                    customer_data = {
                        'name': row[0],      # name (first column)
                        'last_name': row[1], # last_name (second column)
                        'contact': row[2],   # contact_no (third column)
                        'email': row[3],     # email (fourth column)
                        'ssq': row[4],       # security question
                        'ssa': row[5]        # security answer
                    }
                    print("Login successful, customer data:", customer_data)  # Debug
                    
                    open_main = messagebox.askyesno("YesNo", "Customer login successful. Press yes to continue", parent=self.root)
                    if open_main:
                        self.new_window = Toplevel(self.root)
                        from vender import Vendor
                        # Pass customer data to Vendor
                        self.app = Vendor(self.new_window)

            except Exception as ex:
                messagebox.showerror("Error", str(ex), parent=self.root)

    def regi(self):
        self.new_window = Toplevel(self.root)
        from register import Register
        self.app = Register(self.new_window)

    # ====================== reset password ====================================
    def reset(self):
        if self.security_combo.get() == "select":
            messagebox.showerror("Error", "Select security Question", parent=self.root2)
        elif self.entry_sa.get() == "":
            messagebox.showerror("Error", "Please enter the answer", parent=self.root2)
        elif self.entry_new_pass.get() == "":
            messagebox.showerror("Error", "Please enter the new password", parent=self.root2)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="1234", database="grocarystore")
                my_cursor = conn.cursor()
                query = "SELECT * FROM cust_register WHERE email=%s AND securityq=%s AND securitya=%s"
                value = (self.txt_user.get(), self.security_combo.get(), self.entry_sa.get())
                my_cursor.execute(query, value)
                row = my_cursor.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Please enter correct answer", parent=self.root2)
                else:
                    query2 = "UPDATE cust_register SET password=%s WHERE email=%s"
                    value2 = (self.entry_new_pass.get(), self.txt_user.get())
                    my_cursor.execute(query2, value2)
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Info", "Your password has been reset, please login with the new password", parent=self.root2)
            except Exception as ex:
                messagebox.showerror("Error", str(ex), parent=self.root2)

    # ====================== forgot password window==================================
    def forgot_password(self):
        if self.txt_user.get() == "":
            messagebox.showerror("Error", "Please enter the Email address to reset password", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="1234", database="grocarystore")
                my_cursor = conn.cursor()
                query = "SELECT * FROM cust_register WHERE email=%s"
                value = (self.txt_user.get(),)
                my_cursor.execute(query, value)
                row = my_cursor.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Please enter a valid username", parent=self.root)
                else:
                    self.root2 = Toplevel()
                    self.root2.title("Forgot Password")
                    self.root2.geometry("400x490+560+210")

                    l = Label(self.root2, text="FORGOT PASSWORD", font=("times new roman", 18, "bold"), bg="white", fg="red")
                    l.place(x=0, y=15, relwidth=1)

                    security_q = Label(self.root2, text="Select Security Question", font=("times new roman", 14, "bold"))
                    security_q.place(x=50, y=100, width=300)

                    self.security_combo = ttk.Combobox(self.root2, font=("times new roman", 14, "bold"), state="readonly")
                    self.security_combo["values"] = ["Select", "Your Birth Place", "Your Mother Name", "Your Pet Name"]
                    self.security_combo.current(0)
                    self.security_combo.place(x=50, y=130, width=300)

                    security_A = Label(self.root2, text="Security Answer", font=("times new roman", 14, "bold"))
                    security_A.place(x=50, y=170, width=300)
                    self.entry_sa = ttk.Entry(self.root2, font=("times new roman", 14, "bold"))
                    self.entry_sa.place(x=50, y=200, width=300)

                    new_pass = Label(self.root2, text="New Password", font=("times new roman", 14, "bold"))
                    new_pass.place(x=50, y=250,width=300)
                    self.entry_new_pass = ttk.Entry(self.root2, font=("times new roman", 14, "bold"))
                    self.entry_new_pass.place(x=50, y=280, width=300)

                    self.reset_btn = Button(self.root2, text="Reset", command=self.reset, font=("times new roman", 14, "bold"), bg="green", fg="white")
                    self.reset_btn.place(x=165, y=330)
            except Exception as ex:
                messagebox.showerror("Error", str(ex), parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Login_page(root)
    root.mainloop()