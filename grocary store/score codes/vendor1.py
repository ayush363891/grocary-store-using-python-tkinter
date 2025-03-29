import os
import sys
from tkinter import *
from tkinter.ttk import Combobox, Spinbox
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import mysql.connector
import datetime
from tkinter import Toplevel, Text, WORD, BOTH, END

class Vendor1:
    def __init__(self, root):
        self.root = root
        #self.customer_data = customer_data or {}
        self.root.title("Vendor 1")
        self.root.geometry("1530x900+-1+0")
        
        # Image handling with absolute paths
        self.all_images = []  # Prevents garbage collection
        self.base_dir = self.get_base_directory()
        self.setup_image_directory()
        
        # Debug prints for troubleshooting
        self.print_debug_info()
        
        # Initialize UI and database
        self.setup_ui()
        self.connect_to_database()
        self.initialize_products()
        
        # Window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def get_base_directory(self):
        """Get the correct base directory regardless of how script is run"""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

    def setup_image_directory(self):
        """Set up image directory structure"""
        self.image_dir = os.path.join(self.base_dir, "product_images")
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
            print(f"Created image directory at: {self.image_dir}")

    def print_debug_info(self):
        """Print debug information for troubleshooting"""
        print("\n=== DEBUG INFORMATION ===")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Script location: {self.base_dir}")
        print(f"Image directory: {self.image_dir}")
        print(f"Customer data: {self.customer_data}")
        
        # Check if we can list files in image directory
        try:
            print("\nImage directory contents:")
            for f in os.listdir(self.image_dir):
                print(f"- {f}")
        except Exception as e:
            print(f"Could not list image directory: {str(e)}")
        print("=======================\n")

    def setup_ui(self):
        """Initialize UI elements"""
        # Title Label
        self.title_lbl = Label(self.root, text="Products", font=("arial", 20, "bold"), 
                            bg="black", fg="gold")
        self.title_lbl.place(x=0, y=0, width=1530, height=50)

        # Back Button
        self.back_btn = Button(self.root, text="BACK", font=("arial", 20, "bold"), 
                            command=self.back, fg="gold", bg="black")
        self.back_btn.place(x=10, y=0, height=50)
        
        # Bill Button
        self.bill_btn = Button(self.root, text="Bill", command=self.bill_area, 
                            font=("arial", 20, "bold"), fg="gold", bg="black")
        self.bill_btn.place(x=1400, y=0, height=50)
        
        # Main Container
        self.container = Frame(self.root, bd=4, bg="#98f6b0", relief=RIDGE)
        self.container.place(x=10, y=55, width=1510, height=820)

    def connect_to_database(self):
        """Establish database connection with proper configuration"""
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="grocarystore",
                buffered=True
            )
            # Test the connection
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchall()
            print("Database connection successful")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")
            self.root.destroy()

    def resolve_image_path(self, image_path):
        """Resolve image path with comprehensive error handling"""
        if not image_path:
            print("No image path provided")
            return None
            
        try:
            # If path is already absolute
            if os.path.isabs(image_path):
                if os.path.exists(image_path):
                    return image_path
                print(f"Absolute path not found: {image_path}")
                return None
                
            # Get just the filename
            image_name = os.path.basename(image_path)
            
            # Define all possible locations to check
            search_locations = [
                # Local product_images directory
                os.path.join(self.image_dir, image_name),
                # product_images in base directory  
                os.path.join(self.base_dir, "product_images", image_name),
                # Base directory
                os.path.join(self.base_dir, image_name),
                # Relative to module location
                os.path.join(os.path.dirname(__file__), "product_images", image_name),
                os.path.join(os.path.dirname(__file__), image_name),
                # Original relative path
                image_path,
                # Current working directory variations
                os.path.join(os.getcwd(), "product_images", image_name),
                os.path.join(os.getcwd(), image_name),
                # Vendor-specific paths
                os.path.join("vendor1_images", image_name),
                os.path.join("vendor_images", image_name)
            ]
            
            # Check each possible location
            for path in search_locations:
                try:
                    if os.path.exists(path):
                        print(f"Found image at: {path}")
                        return path
                except Exception as e:
                    print(f"Error checking path {path}: {str(e)}")
                    continue
                    
            print(f"Image not found in any location: {image_name}")
            return None
            
        except Exception as e:
            print(f"Error resolving image path: {str(e)}")
            return None

    def initialize_products(self):
        """Load products from database with error handling"""
        if not self.conn:
            return
            
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT product_name, price, unit, image_path FROM vendor_1")
                self.products = cursor.fetchall()
                
            # Initialize product variables
            self.product_vars = {}
            self.prices = {}
            
            for product in self.products:
                product_name = product[0]
                self.product_vars[product_name] = StringVar(value="0")
                self.prices[product_name] = product[1]
                
            print(f"Loaded {len(self.products)} products from database")
            self.create_product_display()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products: {str(e)}")

    def create_product_display(self):
        """Create scrollable product grid"""
        canvas = Canvas(self.container, bg="#98f6b0", highlightthickness=0)
        scrollbar = Scrollbar(self.container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="#98f6b0")
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        if not self.products:
            Label(scrollable_frame, text="No products found", font=("arial", 16), bg="#98f6b0").pack(pady=20)
        else:
            self.display_products(scrollable_frame)

    def display_products(self, parent_frame):
        """Display products in responsive grid"""
        for i, product in enumerate(self.products):
            product_name, price, unit, image_path = product
            
            row, col = i // 7, i % 7
            
            prod_frame = Frame(parent_frame, bd=2, bg="white", relief=RIDGE, 
                              width=170, height=250)
            prod_frame.grid(row=row, column=col, padx=20, pady=5, sticky="nsew")
            prod_frame.grid_propagate(False)
            
            # Load product image
            self.load_product_image(prod_frame, product_name, image_path)
            
            # Product name
            Label(prod_frame, text=product_name, font=("arial", 9, "bold"), 
                bg="white", wraplength=160).grid(row=1, column=0, columnspan=2)
            
            # Price
            price_frame = Frame(prod_frame, bg="white")
            price_frame.grid(row=2, column=0, columnspan=2)
            Label(price_frame, text=f"${float(price):.2f}", font=("arial", 9), bg="white").pack(side=LEFT)
            Label(price_frame, text=f"/{unit}", font=("arial", 7), bg="white").pack(side=LEFT)
            
            # Quantity selector
            Spinbox(prod_frame, from_=0, to=10,
                   textvariable=self.product_vars[product_name],
                   width=3, font=("arial", 9)).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Configure grid weights
        max_rows = (len(self.products) // 7 + 1)
        for i in range(max_rows):
            parent_frame.grid_rowconfigure(i, weight=1)
        for i in range(7):
            parent_frame.grid_columnconfigure(i, weight=1)

    def load_product_image(self, parent, product_name, image_path):
        """Load product image with comprehensive error handling"""
        try:
            # Resolve the actual image path
            actual_path = self.resolve_image_path(image_path)
            
            if not actual_path:
                raise FileNotFoundError(f"Could not locate image for {product_name}")
            
            # Open and resize image
            img = Image.open(actual_path)
            img = img.resize((160, 153), Image.Resampling.LANCZOS)
            photo_img = ImageTk.PhotoImage(img)
            
            # Store reference and display
            self.all_images.append(photo_img)
            img_lbl = Label(parent, image=photo_img, bg="white")
            img_lbl.image = photo_img  # Keep reference
            img_lbl.grid(row=0, column=0, pady=5, columnspan=2)
            
        except Exception as e:
            print(f"Error loading image for {product_name}: {str(e)}")
            # Create placeholder with error message
            error_frame = Frame(parent, bg="white", height=153, width=160)
            error_frame.grid(row=0, column=0, pady=5, columnspan=2)
            
            error_msg = f"{os.path.basename(image_path)}\nNot Found" if image_path else "No Image"
            Label(error_frame, text=error_msg, 
                 bg="white", fg="red", font=("arial", 8)).pack(expand=True)

    def back(self):
        """Return to previous window"""
        self.root.destroy()

    def on_close(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to close the application?"):
            if self.conn:
                self.conn.close()
            self.root.destroy()

    def calculate_bill(self):
        """Calculate total bill amount with improved validation"""
        total = 0
        bill_details = {}

        for product_name, var in self.product_vars.items():
            try:
                quantity_str = var.get()
                quantity = int(quantity_str) if quantity_str.isdigit() else 0
                
                if quantity > 0:
                    price = self.prices.get(product_name, 0)
                    total += quantity * float(price)
                    bill_details[product_name] = (quantity, price)
            except ValueError:
                print(f"Invalid quantity for {product_name}: {var.get()}")
                continue

        print(f"Calculated bill: {bill_details}")
        return total, bill_details

    def bill_area(self):
        """Generate and display bill with improved validation"""
        total, bill_details = self.calculate_bill()
        
        if not bill_details:
            messagebox.showerror('Error', 'No Products are Selected or quantities are invalid.')
            return
        
        bill_window = Toplevel(self.root)
        bill_window.title("Bill Details")
        bill_window.geometry("500x600")
        
        textarea = Text(bill_window, font=("Courier New", 12), wrap=WORD)
        textarea.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Bill header with customer info if available
        billnumber = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        textarea.insert(END, f"Bill Number: {billnumber}\n")
        textarea.insert(END, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
        textarea.insert(END, f"Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n")
        
        if self.customer_data:
            textarea.insert(END, f"\nCustomer: {self.customer_data.get('name', '')} {self.customer_data.get('last_name', '')}\n")
            textarea.insert(END, f"Contact: {self.customer_data.get('contact', '')}\n")
            textarea.insert(END, f"Email: {self.customer_data.get('email', '')}\n")
        
        textarea.insert(END, "\n")
        
        # Products table
        textarea.insert(END, "| Product        | Quantity | Price       |\n")
        textarea.insert(END, "|----------------|----------|-------------|\n")
        
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
        
        # Add tax info
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
        
        textarea.config(state=DISABLED)
        
        # Buttons
        btn_frame = Frame(bill_window)
        btn_frame.pack(pady=10)
        
        Button(btn_frame, text="Save Bill", 
              command=lambda: self.save_bill(textarea.get("1.0", END)), 
              font=("arial", 12), bg="green", fg="white").pack(side=LEFT, padx=10)
        
        Button(btn_frame, text="Print Bill", 
              command=lambda: self.print_bill(textarea), 
              font=("arial", 12), bg="blue", fg="white").pack(side=LEFT, padx=10)
        
        Button(btn_frame, text="Close", 
              command=bill_window.destroy, 
              font=("arial", 12), bg="red", fg="white").pack(side=LEFT, padx=10)

    def save_bill(self, bill_text):
        """Save bill to file with improved error handling"""
        try:
            bills_dir = os.path.join(self.base_dir, "bills")
            if not os.path.exists(bills_dir):
                os.makedirs(bills_dir)
            
            filename = os.path.join(bills_dir, f"bill_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            
            with open(filename, "w") as f:
                f.write(bill_text)
            
            messagebox.showinfo("Success", f"Bill saved as:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bill: {str(e)}")

    def print_bill(self, textarea):
        """Simulate bill printing with improved feedback"""
        try:
            bill_text = textarea.get("1.0", END)
            # In a real application, you would send to a printer here
            # For now, just show a message with the bill content
            messagebox.showinfo("Print Bill", "Bill would be printed here\n\n" + bill_text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print bill: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = Vendor1(root)
    root.mainloop()