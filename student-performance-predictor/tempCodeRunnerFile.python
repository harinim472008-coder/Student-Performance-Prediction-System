from flask import Flask, render_template, request, jsonify
import random
import time

app = Flask(__name__)

generated_otp = ""
otp_time = 0

OTP_VALIDITY = 60  # seconds
correct_pin = "10987"

daily_spent = 50000
DAILY_LIMIT = 95000

card_blocked = False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send_otp", methods=["POST"])
def send_otp():
    global generated_otp, otp_time, card_blocked, daily_spent

    if card_blocked:
        return jsonify({"status": "CARD BLOCKED"})

    amount = float(request.json["amount"])

    if daily_spent + amount > DAILY_LIMIT:
        return jsonify({"status": "FRAUD ALERT: Limit exceeded"})

    generated_otp = str(random.randint(100000, 999999))
    otp_time = time.time()

    return jsonify({
        "status": "OTP Sent",
        "otp": generated_otp
    })


@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    global generated_otp, otp_time, card_blocked

    entered_otp = request.json["otp"]

    # OTP Expiry Check
    if time.time() - otp_time > OTP_VALIDITY:
        return jsonify({"status": "OTP Expired"})

    if entered_otp != generated_otp:
        card_blocked = True
        return jsonify({"status": "WRONG OTP - CARD BLOCKED"})

    return jsonify({"status": "OTP Verified"})


@app.route("/verify_pin", methods=["POST"])
def verify_pin():
    global daily_spent

    entered_pin = request.json["pin"]
    amount = float(request.json["amount"])

    if entered_pin != correct_pin:
        return jsonify({"status": "Wrong PIN"})

    daily_spent += amount

    return jsonify({
        "status": "Transaction Successful"
    })


if __name__ == "__main__":
    app.run(debug=True)