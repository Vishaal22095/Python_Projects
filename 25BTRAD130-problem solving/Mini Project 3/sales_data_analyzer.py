
"""
MINI PROJECT - UNIT 3: SALES DATA ANALYZER
Problem Solving Component - Python Programming Laboratory

Student Name : VISHAAL MS
USN          : 25BTRAD130
Branch       : B.Tech CSE (AI & DE)
Semester     : 3rd Sem
Class        : CSE-AIDE (B)
Academic Year: 2026 - 2027
"""


# --------------------------------------------------
# 1. INITIALIZE SALES CATALOG
# --------------------------------------------------

def create_sales_catalog():
    """Create an empty dictionary to store product details."""
    sales_catalog = {}
    return sales_catalog


# --------------------------------------------------
# 2. ADD PRODUCT DETAILS
# --------------------------------------------------

def add_product(sales_catalog, product_id, product_name,
                price, quantity=0):

    """Add a product to the sales catalog."""

    if product_id in sales_catalog:
        print("Product ID already exists!")
        return

    if price < 0 or quantity < 0:
        print("Price and quantity cannot be negative!")
        return

    sales_catalog[product_id] = {
        "name": product_name,
        "price": float(price),
        "quantity": int(quantity)
    }


# --------------------------------------------------
# 3. RECORD PRODUCT SALES
# --------------------------------------------------

def record_sale(sales_catalog, product_id, quantity):

    """Update the quantity sold for a particular product."""

    if product_id not in sales_catalog:
        print("Product not found!")
        return

    if quantity <= 0:
        print("Quantity must be greater than zero!")
        return

    sales_catalog[product_id]["quantity"] += quantity


# --------------------------------------------------
# 4. UPDATE PRODUCT PRICE
# --------------------------------------------------

def update_product_price(sales_catalog, product_id,
                         new_price):

    """Change the selling price of an existing product."""

    if product_id not in sales_catalog:
        print("Product not found!")
        return

    if new_price < 0:
        print("Price cannot be negative!")
        return

    sales_catalog[product_id]["price"] = float(new_price)


# --------------------------------------------------
# 5. CALCULATE PRODUCT REVENUE
# --------------------------------------------------

def calculate_revenue(price, quantity):

    """Calculate the total revenue of a product."""

    revenue = price * quantity
    return round(revenue, 2)


# --------------------------------------------------
# 6. CALCULATE OVERALL SALES
# --------------------------------------------------

def calculate_sales_totals(sales_catalog):

    """Calculate total quantity and total revenue."""

    total_quantity = 0
    total_revenue = 0

    for product in sales_catalog.values():

        total_quantity += product["quantity"]

        total_revenue += calculate_revenue(
            product["price"],
            product["quantity"]
        )

    return total_quantity, round(total_revenue, 2)


# --------------------------------------------------
# 7. FIND TOP SELLING PRODUCTS
# --------------------------------------------------

def find_top_products(sales_catalog):

    """Find the products with the highest quantity
    sold and highest revenue."""

    if not sales_catalog:
        return None, None

    highest_quantity_product = max(
        sales_catalog.items(),
        key=lambda item: item[1]["quantity"]
    )

    highest_revenue_product = max(
        sales_catalog.items(),
        key=lambda item: calculate_revenue(
            item[1]["price"],
            item[1]["quantity"]
        )
    )

    return highest_quantity_product, highest_revenue_product


# --------------------------------------------------
# 8. DISPLAY SALES REPORT
# --------------------------------------------------

def display_sales_report(sales_catalog):

    """Display the complete sales analysis report."""

    if not sales_catalog:
        print("\nNo products available in the catalog.")
        return

    total_quantity, total_revenue = calculate_sales_totals(
        sales_catalog
    )

    top_quantity, top_revenue = find_top_products(
        sales_catalog
    )

    print("\n" + "=" * 100)
    print("ELECTRONICS AND ACCESSORIES SALES REPORT".center(100))
    print("=" * 100)

    print(
        f"{'ID':<8}"
        f"{'Product Name':<25}"
        f"{'Price (Rs.)':<15}"
        f"{'Quantity':<12}"
        f"{'Revenue (Rs.)':<18}"
        f"{'Share':<10}"
    )

    print("-" * 100)

    # Arrange products according to revenue
    sorted_products = sorted(
        sales_catalog.items(),
        key=lambda item: calculate_revenue(
            item[1]["price"],
            item[1]["quantity"]
        ),
        reverse=True
    )

    for product_id, details in sorted_products:

        name = details["name"]
        price = details["price"]
        quantity = details["quantity"]

        revenue = calculate_revenue(price, quantity)

        if total_revenue > 0:
            percentage = (revenue / total_revenue) * 100
        else:
            percentage = 0

        print(
            f"{product_id:<8}"
            f"{name:<25}"
            f"{price:<15,.2f}"
            f"{quantity:<12}"
            f"{revenue:<18,.2f}"
            f"{percentage:.1f}%"
        )

    print("-" * 100)

    print("\nSALES SUMMARY")
    print("-" * 50)

    print("Total Products      :", len(sales_catalog))
    print("Total Units Sold    :", total_quantity)
    print("Total Revenue       : Rs.", format(total_revenue, ",.2f"))

    print("-" * 50)

    # Display top selling products
    volume_product = top_quantity[1]
    revenue_product = top_revenue[1]

    print("\nTOP PRODUCT PERFORMANCE")
    print("-" * 50)

    print(
        "Highest Quantity Sold:",
        volume_product["name"],
        "-",
        volume_product["quantity"],
        "units"
    )

    print(
        "Highest Revenue:",
        revenue_product["name"],
        "- Rs.",
        format(
            calculate_revenue(
                revenue_product["price"],
                revenue_product["quantity"]
            ),
            ",.2f"
        )
    )

    print("=" * 100)


# --------------------------------------------------
# 9. LOAD SAMPLE PRODUCT DATA
# --------------------------------------------------

def load_sample_products(sales_catalog):

    """Insert sample electronics products into the catalog."""

    products = [
        ("P101", "Wireless Mouse", 750.00, 45),
        ("P102", "Mechanical Keyboard", 3200.00, 20),
        ("P103", "27-inch 4K Monitor", 24500.00, 6),
        ("P104", "USB-C Multiport Hub", 1499.00, 35),
        ("P105", "Noise-Cancelling Mic", 4800.00, 12),
        ("P106", "HDMI 2.1 Cable (2m)", 450.00, 80)
    ]

    for product in products:

        product_id, name, price, quantity = product

        add_product(
            sales_catalog,
            product_id,
            name,
            price,
            quantity
        )

    print("\n[+] Sample product catalog loaded successfully!")


# --------------------------------------------------
# 10. PROCESS SALES TRANSACTIONS
# --------------------------------------------------

def process_sales(sales_catalog):

    """Process additional sales transactions."""

    record_sale(sales_catalog, "P101", 15)
    record_sale(sales_catalog, "P103", 2)
    record_sale(sales_catalog, "P106", 25)

    print("[+] Additional sales transactions completed!")

    # Apply promotional price to Mechanical Keyboard
    print("\n[Promo Event] Mechanical Keyboard discount applied.")

    update_product_price(
        sales_catalog,
        "P102",
        2800.00
    )

    record_sale(sales_catalog, "P102", 15)

    print("[+] Promotional sales recorded successfully!")
    print("[+] Updated keyboard price: Rs. 2800.00")


# --------------------------------------------------
# 11. MAIN PROGRAM
# --------------------------------------------------

def main():

    print("\n")
    print("*" * 65)
    print("       SALES DATA ANALYZER - PYTHON MINI PROJECT")
    print("*" * 65)

    print("Student Name : VISHAAL MS")
    print("USN          : 25BTRAD130")
    print("Branch       : B.Tech CSE (AI & DE)")
    print("Semester     : 3rd Sem")
    print("Class        : CSE-AIDE (B)")
    print("Academic Year: 2026 - 2027")

    print("*" * 65)

    # Create sales catalog
    catalog = create_sales_catalog()

    # Load product information
    load_sample_products(catalog)

    # Process sales transactions
    process_sales(catalog)

    # Generate final sales report
    display_sales_report(catalog)

    print("\nSales Data Analysis Completed Successfully!")
    print("Thank You!")


# --------------------------------------------------
# 12. PROGRAM EXECUTION
# --------------------------------------------------

if __name__ == "__main__":
    main()
