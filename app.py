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

        phone = request.form.get("phone")

        if phone:

            otp = str(random.randint(100000, 999999))

            session["phone"] = phone
            session["otp"] = otp
            session.permanent = True

            print("================================")
            print("PHONE:", phone)
            print("OTP:", otp)
            print("================================")

            return render_template(
                "verify_otp.html",
                otp=otp
            )

        return render_template(
            "customer_login.html",
            error="Please enter your mobile number"
        )

    return render_template("customer_login.html")


# =========================
# VERIFY OTP
# =========================

@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    if request.method == "POST":

        entered_otp = request.form.get("otp")
        correct_otp = session.get("otp")

        print("ENTERED OTP:", entered_otp)
        print("SESSION OTP:", correct_otp)

        if entered_otp == correct_otp:

            session["customer_logged_in"] = True
            session.modified = True

            print("================================")
            print("CUSTOMER LOGIN SUCCESS")
            print("================================")

            return redirect(url_for("customer_dashboard"))

        return render_template(
            "verify_otp.html",
            error="Invalid OTP. Please try again."
        )

    return render_template(
        "verify_otp.html",
        otp=session.get("otp")
    )


# =========================
# CUSTOMER DASHBOARD
# =========================

@app.route("/customer-dashboard")
def customer_dashboard():

    if session.get("customer_logged_in") is not True:
        return redirect(url_for("customer_login"))

    return render_template("customer_dashboard.html")


# =========================
# RESTAURANTS
# =========================

@app.route("/restaurants")
def restaurants():

    if session.get("customer_logged_in") is not True:
        return redirect(url_for("customer_login"))

    return render_template("restaurants.html")


# =========================
# FOOD MENU
# =========================

@app.route("/food-menu")
def food_menu():

    if session.get("customer_logged_in") is not True:
        return redirect(url_for("customer_login"))

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

    if session.get("customer_logged_in") is not True:
        return redirect(url_for("customer_login"))

    return render_template("cart.html")


# =========================
# ADD TO CART
# =========================

@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():

    if session.get("customer_logged_in") is not True:
        return redirect(url_for("customer_login"))

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

    if session.get("customer_logged_in") is not True:
        return redirect(url_for("customer_login"))

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

    if session.get("customer_logged_in") is not True:
        return redirect(url_for("customer_login"))

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

    if session.get("customer_logged_in") is not True:
        return redirect(url_for("customer_login"))

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
    app.run(host="0.0.0.0", port=5000, debug=True)