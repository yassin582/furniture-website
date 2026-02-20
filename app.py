# Import Flask and helpers
from flask import Flask, render_template, request, redirect, url_for, flash
import json
import smtplib
from email.mime.text import MIMEText
import os

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder = template_dir)

# Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"  # For flash messages

# -----------------------------
# Load products from JSON
# -----------------------------
def load_products():
    with open("data/products.json") as f:
        return json.load(f)

# -----------------------------
# Home page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -----------------------------
# About page
# -----------------------------
@app.route("/about")
def about():
    return render_template("about.html")

# -----------------------------
# Products page
# -----------------------------
@app.route("/products")
def products():
    items = load_products()
    return render_template("products.html", products=items)

# -----------------------------
# Contact page with email
# -----------------------------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        # -----------------------------
        # Save to local backup
        # -----------------------------
        with open("data/contacts.txt", "a") as f:
            f.write(f"{name}, {email}: {message} {phone}\n")

        # -----------------------------
        # Send email to your dad
        # -----------------------------
        try:
            msg_content = f"Name: {name}\nEmail: {email}Phone:\n{phone}\nMessage:\n{message}"
            msg = MIMEText(msg_content)
            msg['Subject'] = "New Contact Form Message"
            msg['From'] = "yassinytplayzofficial@gmail.com"       # Replace with your Gmail
            msg['To'] = "imostafa39@yahoo.com"         # Replace with your dad's email

            # Send via Gmail SMTP
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login("YOUR_GMAIL@gmail.com", "Mostafa_furniture10")  # Replace with app password
                server.send_message(msg)

            flash("Message sent successfully!")
        except Exception as e:
            flash(f"Message saved but failed to send email: {e}")

        return redirect(url_for("contact"))

    return render_template("contact.html")

# -----------------------------
# Run the app
# -----------------------------
if __name__ == "__main__":
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app = Flask(__name__, template_folder=template_dir)
    app.secret_key = "your_secret_key"
    app.run(debug=True)