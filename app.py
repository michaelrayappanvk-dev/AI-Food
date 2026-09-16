from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)

app.secret_key = "foodai-secret-key-123"


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# CUSTOMER LOGIN
# =========================

@app.route("/customer-login", methods=["GET", "POST"])
def customer_login():

    if request.method == "POST":

        email = request.form.get("email")

        if not email:
            return render_template(
                "customer_login.html",
                error="Please enter your email."
            )

        # Generate 6 digit OTP
        otp = str(random.randint(100000, 999999))

        # Save email and OTP in session
        session["customer_email"] = email
        session["customer_otp"] = otp
        session.modified = True

        # Temporary testing
        # OTP will appear in terminal
        print("================================")
        print("CUSTOMER EMAIL:", email)
        print("CUSTOMER OTP:", otp)
        print("================================")

        return redirect(url_for("verify_otp"))

    return render_template("customer_login.html")


# =========================
# VERIFY OTP
# =========================

@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    if request.method == "POST":

        entered_otp = request.form.get("otp")
        saved_otp = session.get("customer_otp")

        if entered_otp == saved_otp:

            session["customer_logged_in"] = True

            # Remove OTP after successful login
            session.pop("customer_otp", None)

            session.modified = True

            return redirect(url_for("customer_dashboard"))

        return render_template(
            "verify_otp.html",
            error="Invalid OTP. Please try again."
        )

    return render_template("verify_otp.html")


# =========================
# CUSTOMER DASHBOARD
# =========================

@app.route("/customer-dashboard")
def customer_dashboard():

    return render_template("customer_dashboard.html")


# =========================
# RESTAURANTS
# =========================

@app.route("/restaurants")
def restaurants():

    return render_template("restaurants.html")


# =========================
# FOOD MENU
# =========================

@app.route("/food-menu")
def food_menu():

    cart_count = len(session.get("cart", []))

    return render_template(
        "food_menu.html",
        cart_count=cart_count
    )


# =========================
# CART
# =========================

@app.route("/cart")
def cart():

    return render_template("cart.html")


# =========================
# ADD TO CART
# =========================

@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():

    food_name = request.form.get("food_name")
    price = request.form.get("price")

    if food_name and price:

        cart = session.get("cart", [])

        cart.append({
            "name": food_name,
            "price": int(price)
        })

        session["cart"] = cart
        session.modified = True

    return redirect(url_for("food_menu"))


# =========================
# DELIVERY ADDRESS
# =========================

@app.route("/delivery-address", methods=["GET", "POST"])
def delivery_address():

    if request.method == "POST":

        session["delivery_address"] = {

            "door_number": request.form.get("door_number"),

            "street": request.form.get("street"),

            "landmark": request.form.get("landmark"),

            "district": request.form.get("district"),

            "state": request.form.get("state"),

            "pincode": request.form.get("pincode"),

            "phone": request.form.get("phone")
        }

        session.modified = True

        print("================================")
        print("DELIVERY ADDRESS SAVED:")
        print(session["delivery_address"])
        print("================================")

        return redirect(url_for("confirm_order"))

    return render_template("delivery_address.html")


# =========================
# CONFIRM ORDER
# =========================

@app.route("/confirm-order")
def confirm_order():

    address = session.get("delivery_address", {})

    return render_template(
        "confirm_order.html",
        address=address
    )


# =========================
# TRACK DELIVERY
# =========================

@app.route("/track-delivery")
def track_delivery():

    address = session.get("delivery_address", {})

    return render_template(
        "track_delivery.html",
        address=address
    )


# =========================
# ADMIN LOGIN
# =========================

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":

            session["admin_logged_in"] = True
            session.modified = True

            return redirect(url_for("admin_dashboard"))

        return render_template(
            "admin_login.html",
            error="Invalid Admin Username or Password"
        )

    return render_template("admin_login.html")


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin-dashboard")
def admin_dashboard():

    if session.get("admin_logged_in") is not True:

        return redirect(url_for("admin_login"))

    return render_template("admin_dashboard.html")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )