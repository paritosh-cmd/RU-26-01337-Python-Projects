
import os

FILE_NAME = "products.txt"

# List to store all products
products = []

# Dictionary to store cart items
cart = {}


# Load products from file
def load_products():
    global products

    products = []

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            for line in file:
                data = line.strip().split(",")

                if len(data) == 4:
                    product = {
                        "id": data[0],
                        "name": data[1],
                        "price": float(data[2]),
                        "stock": int(data[3])
                    }
                    products.append(product)


# Save products to file
def save_products():
    with open(FILE_NAME, "w") as file:
        for p in products:
            file.write(
                f"{p['id']},{p['name']},"
                f"{p['price']},{p['stock']}\n"
            )


# Generate product ID
def generate_product_id():
    if not products:
        return "P101"

    max_id = max(int(p["id"][1:]) for p in products)
    return f"P{max_id + 1}"


# Add a new product
def add_product():
    print("\n--- Add Product ---")

    name = input("Enter product name: ").strip()

    if not name or "," in name:
        print("Invalid product name.")
        return

    try:
        price = float(input("Enter product price: "))
        stock = int(input("Enter product stock: "))

        if price <= 0:
            print("Invalid price. Price must be a positive number.")
            return

        if stock < 0:
            print("Stock cannot be negative.")
            return

    except ValueError:
        print("Invalid input. Enter valid numeric values.")
        return

    product_id = generate_product_id()

    product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }

    products.append(product)
    save_products()

    print("Product added.")
    print(
        f"ID: {product_id} | {name} | "
        f"Price: {price:g} | Stock: {stock}"
    )

    if stock == 0:
        print(f"Warning: {name} is out of stock.")


# View all products
def view_products():
    print("\n--- Product List ---")

    if not products:
        print("No products available.")
        return

    print("-" * 65)
    print(f"{'ID':<10}{'Name':<20}{'Price':<15}{'Stock':<10}")
    print("-" * 65)

    for p in products:
        print(
            f"{p['id']:<10}{p['name']:<20}"
            f"{p['price']:<15g}{p['stock']:<10}"
        )

    print("-" * 65)


# Update product
def update_product():
    print("\n--- Update Product ---")

    product_id = input("Enter product ID: ").strip().upper()

    for p in products:
        if p["id"] == product_id:

            print("Leave blank to keep the existing value.")

            name = input("Enter new name: ").strip()

            if name:
                if "," in name:
                    print("Invalid product name.")
                    return
                p["name"] = name

            price = input("Enter new price: ").strip()

            if price:
                try:
                    new_price = float(price)

                    if new_price <= 0:
                        print("Price must be positive.")
                        return

                    p["price"] = new_price

                except ValueError:
                    print("Invalid price.")
                    return

            stock = input("Enter new stock: ").strip()

            if stock:
                try:
                    new_stock = int(stock)

                    if new_stock < 0:
                        print("Stock cannot be negative.")
                        return

                    p["stock"] = new_stock

                except ValueError:
                    print("Invalid stock.")
                    return

            save_products()
            print("Product updated successfully.")
            return

    print(f"Product {product_id} not found.")


# Delete product
def delete_product():
    print("\n--- Delete Product ---")

    product_id = input("Enter product ID: ").strip().upper()

    for p in products:
        if p["id"] == product_id:
            name = p["name"]
            products.remove(p)

            # Remove product from cart if present
            cart.pop(product_id, None)

            save_products()

            print(f"Product '{name}' deleted.")
            print(f"Products left: {len(products)}")
            return

    print(f"Product {product_id} not found.")


# Add product to cart
def add_to_cart():
    print("\n--- Add to Cart ---")

    product_id = input("Enter product ID: ").strip().upper()

    product = None

    for p in products:
        if p["id"] == product_id:
            product = p
            break

    if product is None:
        print(f"Product {product_id} not found.")
        return

    if product["stock"] <= 0:
        print(f"Product {product['name']} is out of stock.")
        return

    try:
        quantity = int(input("Enter quantity: "))

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return

    except ValueError:
        print("Invalid quantity.")
        return

    current_quantity = cart.get(product_id, 0)

    if current_quantity + quantity > product["stock"]:
        print(
            f"Insufficient stock. Available stock: "
            f"{product['stock'] - current_quantity}"
        )
        return

    cart[product_id] = current_quantity + quantity

    amount = product["price"] * quantity

    print(
        f"{product['name']} x{quantity} added | "
        f"Amount: {amount:g}"
    )


# View cart
def view_cart():
    print("\n--- Shopping Cart ---")

    if not cart:
        print("Cart is empty.")
        return

    total = 0

    for product_id, quantity in cart.items():

        for p in products:
            if p["id"] == product_id:

                amount = p["price"] * quantity
                total += amount

                print(
                    f"{p['name']} x{quantity} | "
                    f"Price: {p['price']:g} | "
                    f"Amount: {amount:g}"
                )

                break

    print(f"Cart Total: {total:g}")


# Checkout
def checkout():
    print("\n--- Checkout ---")

    if not cart:
        print("Cart is empty.")
        return

    # Validate all products before reducing stock
    for product_id, quantity in cart.items():

        product = next(
            (p for p in products if p["id"] == product_id),
            None
        )

        if product is None:
            print(f"Product {product_id} not found.")
            return

        if quantity > product["stock"]:
            print(f"Insufficient stock for {product['name']}.")
            return

    total = 0

    # Process checkout
    for product_id, quantity in cart.items():

        for p in products:
            if p["id"] == product_id:

                amount = p["price"] * quantity
                total += amount

                p["stock"] -= quantity

                print(
                    f"{p['name']} x{quantity} | "
                    f"Amount: {amount:g} | "
                    f"Stock left: {p['stock']}"
                )

                break

    save_products()

    print("-" * 40)
    print(f"Order Total: {total:g}")
    print("Checkout successful!")

    cart.clear()


# Main menu
def main():
    load_products()

    while True:

        print("\n========== MINI E-COMMERCE SYSTEM ==========")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Add to Cart")
        print("6. View Cart")
        print("7. Checkout")
        print("8. Exit")
        print("============================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_product()

        elif choice == "2":
            view_products()

        elif choice == "3":
            update_product()

        elif choice == "4":
            delete_product()

        elif choice == "5":
            add_to_cart()

        elif choice == "6":
            view_cart()

        elif choice == "7":
            checkout()

        elif choice == "8":
            save_products()
            print("Thank you for using Mini E-Commerce System!")
            break

        else:
            print("Invalid menu choice. Please try again.")


# Program execution
if __name__ == "__main__":
    main()
