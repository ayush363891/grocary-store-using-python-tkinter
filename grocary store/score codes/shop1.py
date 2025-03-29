from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import mysql.connector
import os
from tkinter import messagebox

class Shop1:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopkeeper Management")
        self.root.geometry("1550x900+0+0")

        # Initialize data structures
        self.products_vendor1 = {}  # {product_name: {"unit": unit, "price": price}}
        self.products_vendor2 = {}
        self.vars_vendor1 = {}      # {product_name: StringVar()}
        self.vars_vendor2 = {}
        
        # Create image directory
        self.image_dir = "product_images"
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
        
        # Connect to database and load data first
        self.conn = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="1234", 
            database="grocarystore"
        )
        
        self.create_ui()
        self.load_prices()

    def create_ui(self):
        self.prod_frame = Frame(self.root, bd=2, bg="aliceblue", relief=RIDGE)
        self.prod_frame.place(x=0, y=0, width=1545, height=885)

        # Vendor 1 Frame
        self.lbl_frame1 = LabelFrame(self.prod_frame, text="शेतकरी दादा", font=("arial", 12), 
                                   bg="#c6fcff", width=200, height=500)
        self.lbl_frame1.place(x=65, y=12, width=650, height=700)
        
        # Vendor 1 Canvas and Scrollbar
        self.canvas1 = Canvas(self.lbl_frame1, bg="#c6fcff", highlightthickness=0)
        self.scrollbar1 = Scrollbar(self.lbl_frame1, orient="vertical", command=self.canvas1.yview)
        self.scrollable_frame1 = Frame(self.canvas1, bg="#c6fcff")
        
        self.scrollable_frame1.bind("<Configure>", lambda e: self.canvas1.configure(scrollregion=self.canvas1.bbox("all")))
        self.canvas1.create_window((0, 0), window=self.scrollable_frame1, anchor="nw")
        self.canvas1.configure(yscrollcommand=self.scrollbar1.set)
        self.canvas1.pack(side="left", fill="both", expand=True)
        self.scrollbar1.pack(side="right", fill="y")

        # Vendor 2 Frame
        self.lbl_frame2 = LabelFrame(self.prod_frame, text="शेतकरी काका", font=("arial", 12), 
                                   bg="#c6fcff", width=200, height=500)
        self.lbl_frame2.place(x=815, y=12, width=650, height=700)
        
        # Vendor 2 Canvas and Scrollbar
        self.canvas2 = Canvas(self.lbl_frame2, bg="#c6fcff", highlightthickness=0)
        self.scrollbar2 = Scrollbar(self.lbl_frame2, orient="vertical", command=self.canvas2.yview)
        self.scrollable_frame2 = Frame(self.canvas2, bg="#c6fcff")
        
        self.scrollable_frame2.bind("<Configure>", lambda e: self.canvas2.configure(scrollregion=self.canvas2.bbox("all")))
        self.canvas2.create_window((0, 0), window=self.scrollable_frame2, anchor="nw")
        self.canvas2.configure(yscrollcommand=self.scrollbar2.set)
        self.canvas2.pack(side="left", fill="both", expand=True)
        self.scrollbar2.pack(side="right", fill="y")

        # Add Product Buttons
        Button(self.lbl_frame1, text="Add Product", command=lambda: self.add_product("vendor_1"), 
              font=("arial", 10), bg="green", fg="white").place(x=520, y=3, width=100, height=25)
        Button(self.lbl_frame2, text="Add Product", command=lambda: self.add_product("vendor_2"), 
              font=("arial", 10), bg="green", fg="white").place(x=520, y=3, width=100, height=25)

        # Bottom Buttons
        Button(self.prod_frame, text="Back", font=("arial", 20, "bold"), 
              bg="black", fg="gold").place(x=100, y=750)
        Button(self.prod_frame, text="Update", command=self.update, 
              font=("arial", 20, "bold"), bg="black", fg="gold").place(x=1300, y=750)

    def load_prices(self):
        try:
            cursor = self.conn.cursor()

            # Load vendor 1 products
            cursor.execute("SELECT product_name, unit, price FROM vendor_1")
            for name, unit, price in cursor.fetchall():
                self.products_vendor1[name] = {"unit": unit, "price": price}
                self.vars_vendor1[name] = StringVar(value=price)

            # Load vendor 2 products
            cursor.execute("SELECT product_name, unit, price FROM vendor_2")
            for name, unit, price in cursor.fetchall():
                self.products_vendor2[name] = {"unit": unit, "price": price}
                self.vars_vendor2[name] = StringVar(value=price)

            # Create UI for both vendors after loading data
            self.create_vendor_ui("vendor_1")
            self.create_vendor_ui("vendor_2")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def create_vendor_ui(self, vendor_name):
        # Determine which frame and products to use
        if vendor_name == "vendor_1":
            frame = self.scrollable_frame1
            products = self.products_vendor1
            vars_dict = self.vars_vendor1
        else:
            frame = self.scrollable_frame2
            products = self.products_vendor2
            vars_dict = self.vars_vendor2

        # Clear existing widgets
        for widget in frame.winfo_children():
            widget.destroy()

        # Create headers
        Label(frame, text="Name", font=("arial", 12, "bold"), bg="#c6fcff").grid(row=0, column=0, padx=10, pady=5)
        Label(frame, text="Unit", font=("arial", 12, "bold"), bg="#c6fcff").grid(row=0, column=1, padx=5, pady=5)
        Label(frame, text="Price", font=("arial", 12, "bold"), bg="#c6fcff").grid(row=0, column=2, padx=5, pady=5)
        Label(frame, text="Action", font=("arial", 12, "bold"), bg="#c6fcff").grid(row=0, column=3, padx=5, pady=5)

        # Add products with delete buttons
        for i, (product, details) in enumerate(products.items()):
            Label(frame, text=product, font=("arial", 12), bg="#c6fcff").grid(row=i+1, column=0, padx=10, pady=5)
            Label(frame, text=self.format_unit(details["unit"]), font=("arial", 12), bg="#c6fcff").grid(row=i+1, column=1, padx=5, pady=5)
            Entry(frame, textvariable=vars_dict[product], font=("arial", 12), width=8).grid(row=i+1, column=2, padx=5, pady=5)
            
            # Add delete button for each product
            Button(frame, text="Delete", command=lambda p=product, v=vendor_name: self.delete_product(p, v),
                  font=("arial", 10), bg="red", fg="white").grid(row=i+1, column=3, padx=5, pady=5)

    def delete_product(self, product_name, vendor):
        try:
            # Confirm deletion
            if not messagebox.askyesno("Confirm", f"Delete {product_name} from {vendor}?"):
                return
            
            # Delete from database
            cursor = self.conn.cursor()
            cursor.execute(f"DELETE FROM {vendor} WHERE product_name = %s", (product_name,))
            self.conn.commit()
            
            # Delete from memory
            if vendor == "vendor_1":
                del self.products_vendor1[product_name]
                del self.vars_vendor1[product_name]
            else:
                del self.products_vendor2[product_name]
                del self.vars_vendor2[product_name]
            
            # Refresh the UI
            self.create_vendor_ui(vendor)
            messagebox.showinfo("Success", "Product deleted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete product: {str(e)}")

    def format_unit(self, unit):
        # Format units for display
        units_map = {
            "kg": "1 kg",
            "g": "100 g",
            "pc": "1 pc",
            "500ml": "500 ml",
            "1L": "1 L",
            "250g": "250 g",
            "bunch": "1 bunch"
        }
        return units_map.get(unit, unit)

    def add_product(self, vendor):
        popup = Toplevel(self.root)
        popup.title(f"Add Product to {vendor}")
        popup.geometry("500x400")

        # Product Name
        Label(popup, text="Product Name:", font=("arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        name_entry = Entry(popup, font=("arial", 12))
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Unit Selection
        Label(popup, text="Unit:", font=("arial", 12)).grid(row=1, column=0, padx=10, pady=5)
        unit_options = ["1 kg", "100 g", "1 pc", "500 ml", "1 L", "250 g", "1 bunch"]
        unit_combobox = Combobox(popup, values=unit_options, font=("arial", 12))
        unit_combobox.grid(row=1, column=1, padx=10, pady=5)
        unit_combobox.set("1 pc")

        # Price
        Label(popup, text="Price:", font=("arial", 12)).grid(row=2, column=0, padx=10, pady=5)
        price_entry = Entry(popup, font=("arial", 12))
        price_entry.grid(row=2, column=1, padx=10, pady=5)

        # Image Selection
        Label(popup, text="Product Image:", font=("arial", 12)).grid(row=3, column=0, padx=10, pady=5)
        img_frame = Frame(popup)
        img_frame.grid(row=3, column=1, padx=10, pady=5)
        
        browse_btn = Button(img_frame, text="Browse", command=lambda: self.select_image(img_label), 
                          font=("arial", 10), bg="blue", fg="white")
        browse_btn.pack(side="left")
        
        img_label = Label(img_frame, text="No image selected", bg="white", width=20, height=5)
        img_label.pack(side="left", padx=10)
        self.selected_image_path = None

        def save_product():
            name = name_entry.get().strip()
            display_unit = unit_combobox.get().strip()
            price = price_entry.get().strip()

            if not name or not price:
                messagebox.showerror("Error", "Name and price are required!")
                return

            # Map display units to database units
            unit_map = {
                "1 kg": "kg", "100 g": "g", "1 pc": "pc",
                "500 ml": "500ml", "1 L": "1L", "250 g": "250g",
                "1 bunch": "bunch"
            }
            db_unit = unit_map.get(display_unit, "pc")

            try:
                # Handle image
                img_path = None
                if self.selected_image_path:
                    ext = os.path.splitext(self.selected_image_path)[1]
                    img_filename = f"{name.replace(' ', '_')}{ext}"
                    img_path = os.path.join(self.image_dir, img_filename)
                    import shutil
                    shutil.copy(self.selected_image_path, img_path)

                # Save to database
                cursor = self.conn.cursor()
                cursor.execute(
                    f"INSERT INTO {vendor} (product_name, unit, price, image_path) VALUES (%s, %s, %s, %s)",
                    (name, db_unit, price, img_path)
                )
                self.conn.commit()

                # Update UI
                if vendor == "vendor_1":
                    self.products_vendor1[name] = {"unit": db_unit, "price": price}
                    self.vars_vendor1[name] = StringVar(value=price)
                else:
                    self.products_vendor2[name] = {"unit": db_unit, "price": price}
                    self.vars_vendor2[name] = StringVar(value=price)

                self.create_vendor_ui(vendor)
                messagebox.showinfo("Success", "Product added!")
                popup.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to add product: {str(e)}")

        Button(popup, text="Save Product", command=save_product, 
              font=("arial", 12), bg="green", fg="white").grid(row=4, column=0, columnspan=2, pady=10)

    def select_image(self, img_label):
        filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
        if filename:
            self.selected_image_path = filename
            try:
                img = Image.open(filename)
                img.thumbnail((100, 100))
                photo = ImageTk.PhotoImage(img)
                img_label.configure(image=photo, text="")
                img_label.image = photo
            except Exception as e:
                messagebox.showerror("Error", f"Invalid image: {str(e)}")

    def update(self):
        try:
            cursor = self.conn.cursor()
            
            # Update vendor 1 prices
            for product, var in self.vars_vendor1.items():
                cursor.execute(
                    "UPDATE vendor_1 SET price=%s WHERE product_name=%s",
                    (var.get(), product)
                )
            
            # Update vendor 2 prices
            for product, var in self.vars_vendor2.items():
                cursor.execute(
                    "UPDATE vendor_2 SET price=%s WHERE product_name=%s",
                    (var.get(), product)
                )
            
            self.conn.commit()
            messagebox.showinfo("Success", "Prices updated!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {str(e)}")

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

if __name__ == "__main__":
    root = Tk()
    app = Shop1(root)
    root.mainloop()