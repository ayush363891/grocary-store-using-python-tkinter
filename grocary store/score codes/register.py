from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
from PIL.Image import Resampling




class Register:
    def __init__(self,root):
        self.root=root
        self.root.title("Register page ")
        self.root.geometry("1600x900+0+0")

        #=========== variables =======================
        self.var_fname=StringVar()
        self.var_lname=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        self.var_ssq=StringVar()
        self.var_sanswer=StringVar()
        self.var_pass=StringVar()
        self.var_cpass=StringVar()


        #================ main image ===============

        img1=Image.open(r"C:\Users\ayush\OneDrive\Desktop\grocary store\images\regi_bg_img.jpg")
        img1=img1.resize((1600,900),Resampling.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)

        img1_lbl=Label(self.root,image=self.photoimg1,bd=0,relief=RIDGE)
        img1_lbl.place(x=0,y=0,width=1600,height=900)

        #================ left side Image =======================
        img2=Image.open(r"C:\Users\ayush\OneDrive\Desktop\grocary store\images\thought-good-morning-messages-LoveSove.jpg")
        img2=img2.resize((500,600),Resampling.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)

        img2_lbl=Label(self.root,image=self.photoimg2,bd=0,relief=RIDGE)
        img2_lbl.place(x=80,y=120,width=500,height=600)

        #================ Main Frame ====================
        frame=Frame(self.root,bg="#9c6d57")
        frame.place(x=580,y=120,width=750,height=600)

        #================= Labels and Entrys ================
        regi_lbl=Label(frame,text="REGISTER HERE",font=("times new roman",20,"bold"),fg="#25ff29",bg="#9c6d57")
        regi_lbl.place(x=0,y=0)

        #first name
        name_lbl=Label(frame,text="First Name",font=("times new roman",14,"bold"),bg="#9c6d57")
        name_lbl.place(x=10,y=100)

        entry_name=ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",14,"bold"),width=25)
        entry_name.place(x=10,y=130)

        #last name
        lname_lbl = Label(frame, text="Last Name", font=("times new roman", 14, "bold"), bg="#9c6d57")
        lname_lbl.place(x=400, y=100)

        entry_lname = ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman", 14, "bold"), width=25)
        entry_lname.place(x=400, y=130)

        #contact no
        contact_lbl = Label(frame, text="Contact No", font=("times new roman", 14, "bold"), bg="#9c6d57")
        contact_lbl.place(x=10, y=180)

        entry_contact = ttk.Entry(frame,textvariable=self.var_contact,font=("times new roman", 14, "bold"), width=25)
        entry_contact.place(x=10, y=210)

        #email
        email_lbl = Label(frame, text="Email", font=("times new roman", 14, "bold"), bg="#9c6d57")
        email_lbl.place(x=400, y=180)

        entry_email = ttk.Entry(frame,textvariable=self.var_email,font=("times new roman", 14, "bold"), width=25)
        entry_email.place(x=400, y=210)

        #select security question
        ssq_lbl = Label(frame, text="Select Security Question", font=("times new roman", 14, "bold"), bg="#9c6d57")
        ssq_lbl.place(x=10, y=260)

        entry_ssq=ttk.Combobox(frame,textvariable=self.var_ssq,font=("times new roman",14,"bold"),width=24,state="readonly")
        entry_ssq["values"]=["Select","Your Birth Place","Your Girlfriend Name","Your Pet Name"]
        entry_ssq.current(0)
        entry_ssq.place(x=10,y=290)

        #Sequrity answer
        ssqans_lbl = Label(frame, text="Security Answer", font=("times new roman", 14, "bold"), bg="#9c6d57")
        ssqans_lbl.place(x=400, y=260)

        entry_ssqans = ttk.Entry(frame,textvariable=self.var_sanswer, font=("times new roman", 14, "bold"), width=25)
        entry_ssqans.place(x=400, y=290)


        #password
        pass_lbl = Label(frame, text="Password", font=("times new roman", 14, "bold"), bg="#9c6d57")
        pass_lbl.place(x=10, y=340)

        entry_pass = ttk.Entry(frame,textvariable=self.var_pass, font=("times new roman", 14, "bold"),show="x",width=25)
        entry_pass.place(x=10, y=370)

        #conform password
        cpass_lbl = Label(frame, text="Confirm Password", font=("times new roman", 14, "bold"), bg="#9c6d57")
        cpass_lbl.place(x=400, y=340)

        entry_cpass = ttk.Entry(frame,textvariable=self.var_cpass, font=("times new roman", 14, "bold"),show="x",width=25)
        entry_cpass.place(x=400, y=370)

       #======================= buttons ============================
        self.var_check=IntVar()
        checkin_btn=Checkbutton(frame,variable=self.var_check,text="I Agree The Terms & Conditions",font=("times new roman",15),bg="#9c6d57",activebackground="#9c6d57")
        checkin_btn.place(x=30,y=410)

        regi_img=Image.open(r"C:\Users\ayush\OneDrive\Desktop\grocary store\images\register-now-button1.jpg")
        regi_img=regi_img.resize((200,50),Resampling.LANCZOS)
        self.photoimg3=ImageTk.PhotoImage(regi_img)
        regi_btn=Button(frame,image=self.photoimg3,command=self.register_data,borderwidth=0,font=("times new roman",15,"bold"),bg="#9c6d57",activebackground="#9c6d57")
        regi_btn.place(x=0,y=440,width=300)

        login_img=Image.open(r"C:\Users\ayush\OneDrive\Desktop\grocary store\images\login.jpg")
        login_img=login_img.resize((200,45),Resampling.LANCZOS)
        self.photoimg4=ImageTk.PhotoImage(login_img)
        login_btn=Button(frame,image=self.photoimg4,command=self.login_window,borderwidth=0,activebackground="#9c6d57",font=("times new roamn",15,"bold"),bg="#9c6d57")
        login_btn.place(x=370,y=440,width=300)

    def register_data(self):
        if self.var_fname.get() == "":
            messagebox.showerror("Error", "Please enter first name", parent=self.root)
        elif self.var_lname.get() == "":
            messagebox.showerror("Error", "Please enter last name", parent=self.root)
        elif self.var_contact.get() == "":
            messagebox.showerror("Error", "Please enter contact number", parent=self.root)
        elif not self.var_contact.get().isdigit() or len(self.var_contact.get()) != 10:
            messagebox.showerror("Error", "Please enter a valid 10-digit contact number", parent=self.root)
        elif self.var_email.get() == "":
            messagebox.showerror("Error", "Please enter email ID", parent=self.root)
        elif not self.var_email.get().endswith("@gmail.com"):
            messagebox.showerror("Error", "Email must end with @gmail.com", parent=self.root)
        elif self.var_ssq.get().lower() == "select":
            messagebox.showerror("Error", "Please select a security question", parent=self.root)
        elif self.var_sanswer.get() == "":
            messagebox.showerror("Error", "Please enter security answer", parent=self.root)
        elif self.var_pass.get() == "":
            messagebox.showerror("Error", "Please enter a password", parent=self.root)
        elif self.var_cpass.get() == "":
            messagebox.showerror("Error", "Please confirm your password", parent=self.root)
        elif self.var_pass.get() != self.var_cpass.get():
            messagebox.showerror("Error", "Password and confirm password should be the same", parent=self.root)
        elif self.var_check.get() == 0:
            messagebox.showerror("Error", "Please agree to our terms and conditions", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="1234",
                    database="grocarystore"
                )
                my_cursor = conn.cursor()

                # Check if user already exists
                query = "SELECT * FROM cust_register WHERE email = %s"
                values = (self.var_email.get(),)
                my_cursor.execute(query, values)
                rows = my_cursor.fetchall()

                if len(rows) > 0:  # If user exists
                    messagebox.showerror("Error", "User already exists, please try another email", parent=self.root)
                else:
                    # Insert new user
                    my_cursor.execute(
                        "INSERT INTO cust_register(name, last_name, contact_no, email, ssq, ssa, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (
                            self.var_fname.get(),
                            self.var_lname.get(),
                            self.var_contact.get(),
                            self.var_email.get(),
                            self.var_ssq.get(),
                            self.var_sanswer.get(),
                            self.var_pass.get()
                        )
                    )

                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Your data has been registered successfully", parent=self.root)

            except Exception as ex:
                messagebox.showerror("Error", str(ex), parent=self.root)

    def login_window(self):
        self.new_window = Toplevel(self.root)
        from login import Login_page
        self.app = Login_page(self.new_window)


if __name__=="__main__":
    root=Tk()
    obj=Register(root)
    root.mainloop()