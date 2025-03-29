from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import mysql.connector
import datetime
from texttable import Texttable
from prettytable import PrettyTable
import datetime
from tkinter import Toplevel, Text, WORD, BOTH, END, messagebox
from tabulate import tabulate
import os

class Vendor2:
    def __init__(self, root,customer_data="None"):
        self.root = root
        self.root.title("Vendor 2")
        self.root.geometry("1530x900+-1+0")

        title_lbl = Label(self.root, text="Products", font=("arial", 20, "bold"), bg="black", fg="gold")
        title_lbl.place(x=0, y=0, width=1530, height=50)

        back_btn = Button(self.root, text="BACK", font=("arial", 20, "bold"), command=self.back, fg="gold", bg="black")
        back_btn.place(x=10, y=0, height=50)

        # Connect to database
        self.conn = mysql.connector.connect(
            host="localhost",
            username="root",
            password="1234",
            database="grocarystore"
        )
        
        # Fetch products
        my_cursor = self.conn.cursor()
        my_cursor.execute("SELECT product_name, price, unit, image_path FROM vendor_2")
        self.products = my_cursor.fetchall()
        
        # Initialize product variables and prices dictionary
        self.product_vars = {}
        self.product_images = {}  # To keep image references
        self.prices = {product[0]: product[1] for product in self.products}  # THIS WAS MISSING
        
        # Main products frame with scrollbar
        container = Frame(self.root, bd=4, bg="#98f6b0", relief=RIDGE)
        container.place(x=10, y=55, width=1510, height=820)
        
        # Create a canvas and scrollbar
        canvas = Canvas(container, bg="#98f6b0", highlightthickness=0)
        scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="#98f6b0")
        
        # Configure canvas scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Display products in a grid (7 columns)
        if not self.products:
            Label(scrollable_frame, text="No products found in database", 
                 font=("arial", 16), bg="#98f6b0").pack(pady=20)
        else:
            # Reduce product frame width to fit 7 in a row
            for i, product in enumerate(self.products):
                product_name, price, unit, image_path = product
                self.product_vars[product_name] = IntVar(value=0)
                
                # Calculate grid position (7 columns)
                row = i // 7
                col = i % 7
                
                # Create product frame with smaller width
                prod_frame = Frame(scrollable_frame, bd=2, bg="white", relief=RIDGE, width=170, height=250)
                prod_frame.grid(row=row, column=col, padx=20, pady=5, sticky="nsew")
                prod_frame.grid_propagate(False)  # Prevent frame from resizing
                
                # Product Image (smaller size) with improved path resolution
                try:
                    resolved_path = None
                    if image_path:
                        # Try multiple possible locations
                        possible_paths = [
                            image_path,
                            os.path.join("product_images", os.path.basename(image_path)),
                            os.path.join(os.path.dirname(__file__), "product_images", os.path.basename(image_path)),
                            os.path.join(os.path.dirname(__file__), os.path.basename(image_path)),
                            os.path.join("vendor2_images", os.path.basename(image_path)),
                            os.path.join("vendor_images", os.path.basename(image_path))
                        ]
                        
                        for path in possible_paths:
                            try:
                                if os.path.exists(path):
                                    resolved_path = path
                                    print(f"Found image at: {path}")
                                    break
                            except Exception as e:
                                print(f"Error checking path {path}: {str(e)}")
                                
                    img = Image.open(resolved_path) if resolved_path else None
                    img = img.resize((160, 153), Image.Resampling.LANCZOS)
                    photo_img = ImageTk.PhotoImage(img)
                    self.product_images[product_name] = photo_img  # Keep reference
                    img_lbl = Label(prod_frame, image=photo_img, bg="white")
                    img_lbl.grid(row=0, column=0, pady=5, columnspan=2)
                except Exception as e:
                    print(f"Error loading image for {product_name}: {e}")
                    img_lbl = Label(prod_frame, text="No Image", bg="white", height=4, width=10)
                    img_lbl.grid(row=0, column=0, pady=5, columnspan=2)
                
                # Product Name (shorter text)
                name_label = Label(prod_frame, text=product_name, 
                                 font=("arial", 9, "bold"), bg="white", wraplength=180)
                name_label.grid(row=1, column=0, columnspan=2)
                
                # Price and Unit
                price_frame = Frame(prod_frame, bg="white")
                price_frame.grid(row=2, column=0, columnspan=2)
                Label(price_frame, text=f"${float(price):.2f}", 
                     font=("arial", 9), bg="white").pack(side=LEFT)
                Label(price_frame, text=f"/{unit}", 
                     font=("arial", 7), bg="white").pack(side=LEFT)
                
                # Quantity Selector (smaller)
                Spinbox(prod_frame, 
                       from_=0, 
                       to=10,
                       textvariable=self.product_vars[product_name],
                       width=3,
                       font=("arial", 9)).grid(row=3, column=0, columnspan=2, pady=5)

            # Configure grid weights for 7 columns
            max_rows = (len(self.products) // 7 + 1)
            for i in range(max_rows):
                scrollable_frame.grid_rowconfigure(i, weight=1)
            for i in range(7):  # 7 columns
                scrollable_frame.grid_columnconfigure(i, weight=1)

        bill_btn = Button(self.root, text="Bill", command=self.bill_area, 
                         font=("arial", 20, "bold"), fg="gold", bg="black")
        bill_btn.place(x=1400, y=0, height=50)

    def back(self):
        self.root.destroy()

    def calculate_bill(self):
        total = 0
        bill_details = {}

        for product, var in self.product_vars.items():
            quantity = var.get()
            if quantity > 0:
                price = self.prices.get(product, 0)
                total += quantity * price
                bill_details[product] = (quantity, price)

        return total, bill_details

    def bill_area(self):
        # Check if any products are selected
        if not any(var.get() > 0 for var in self.product_vars.values()):
            messagebox.showerror('Error', 'No Products are Selected.')
            return
        
        # Calculate total and get bill details
        total, bill_details = self.calculate_bill()
        
        # Create a new window for the bill
        bill_window = Toplevel(self.root)
        bill_window.title("Bill Details")
        bill_window.geometry("500x600")
        
        # Create text area with monospace font for perfect alignment
        textarea = Text(bill_window, font=("Courier New", 12), wrap=WORD)
        textarea.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Generate bill details
        billnumber = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Insert bill header
        textarea.insert(END, "# *Welcome Customer*\n")
        textarea.insert(END, "\n---\n")
        textarea.insert(END, f"Bill Number: {billnumber}\n")
        textarea.insert(END, f"Date: {current_date}\n")
        textarea.insert(END, f"Time: {current_time}\n\n")
        
        # Create the product table
        textarea.insert(END, "| Product        | Quantity | Price       |\n")
        textarea.insert(END, "|----------------|----------|-------------|\n")
        
        # Add each product to the bill with perfect alignment
        for product, (quantity, price) in bill_details.items():
            total_price = float(price) * quantity
            textarea.insert(END, f"| {product.ljust(14)} | {str(quantity).center(8)} | {f'{total_price:.2f} Rs'.rjust(11)} |\n")
        
        # Calculate taxes
        grocery_tax = sum(float(price)*quantity*0.05 
                    for product, (quantity, price) in bill_details.items() 
                    if product in ["Rice", "Ashirvad Wheat", "Bread", "Gemini Oil"])
        
        food_tax = sum(float(price)*quantity*0.12 
                    for product, (quantity, price) in bill_details.items() 
                    if product in ["Amul Butter", "Amul Icecream", "Amul Milk", "Cheese", "Egg"])
        
        produce_tax = sum(float(price)*quantity*0.08 
                        for product, (quantity, price) in bill_details.items() 
                        if product in ["Onion", "Capcicum", "Cauli Flower", "Coconut", "Lemon", 
                                    "Potato", "Tomato", "Coriander", "Strawberry"])
        
        total_tax = grocery_tax + food_tax + produce_tax
        total_with_tax = float(total) + total_tax
        
        # Add tax and total information
        textarea.insert(END, "\n---\n")
        
        if grocery_tax > 0:
            textarea.insert(END, f"Grocery Tax (5%): {grocery_tax:.2f} Rs\n")
        if food_tax > 0:
            textarea.insert(END, f"Food Tax (12%): {food_tax:.2f} Rs\n")
        if produce_tax > 0:
            textarea.insert(END, f"Produce Tax (8%): {produce_tax:.2f} Rs\n")
        
        textarea.insert(END, "---\n")
        textarea.insert(END, f"Total Amount: {total_with_tax:.2f} Rs\n")
        textarea.insert(END, "---\n")
        textarea.insert(END, "\nThank you for shopping with us!")
        
        # Make the text area read-only
        textarea.config(state=DISABLED)
        
        # Add buttons frame at the bottom
        btn_frame = Frame(bill_window)
        btn_frame.pack(pady=10)
        
        save_btn = Button(btn_frame, text="Save Bill", 
                        command=lambda: self.save_bill(textarea.get("1.0", END)), 
                        font=("arial", 12), bg="green", fg="white")
        save_btn.pack(side=LEFT, padx=10)
        
        print_btn = Button(btn_frame, text="Print Bill", 
                        command=lambda: self.print_bill(textarea), 
                        font=("arial", 12), bg="blue", fg="white")
        print_btn.pack(side=LEFT, padx=10)
        
        close_btn = Button(btn_frame, text="Close", 
                        command=bill_window.destroy, 
                        font=("arial", 12), bg="red", fg="white")
        close_btn.pack(side=LEFT, padx=10)

    def save_bill(self, bill_text):
        try:
            # Create bills directory if it doesn't exist
            if not os.path.exists("bills"):
                os.makedirs("bills")
            
            # Generate filename with timestamp
            filename = f"bills/bill_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, "w") as f:
                f.write(bill_text)
            
            messagebox.showinfo("Success", f"Bill saved successfully as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bill: {str(e)}")

    def print_bill(self, textarea):
        try:
            # Get the bill text
            bill_text = textarea.get("1.0", END)
            
            # For demonstration, we'll just show a message
            # In a real application, you would send this to a printer
            messagebox.showinfo("Print Bill", "Bill would be printed here\n\n" + bill_text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print bill: {str(e)}")

    def show_bill(self):
        total, bill_details = self.calculate_bill()
        if not bill_details:
            messagebox.showinfo("Bill Details", "No products selected!")
            return

        customer_name = "Customer"
        invoice_text = self.generate_invoice(customer_name, bill_details)

        bill_window = Toplevel(self.root)
        bill_window.title("Bill Details")
        bill_window.geometry("600x500")

        text_area = Text(bill_window, wrap=WORD, font=("arial", 12))
        text_area.insert(END, invoice_text)
        text_area.pack(fill=BOTH, expand=True, padx=10, pady=10)

        close_btn = Button(bill_window, text="Close", command=bill_window.destroy, font=("arial", 14), bg="black", fg="white")
        close_btn.pack(pady=10)

if __name__ == "__main__":
    root = Tk()
    app = Vendor2(root)
    root.mainloop()