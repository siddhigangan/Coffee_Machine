from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Menu with ingredients and cost
MENU = {
    "espresso": {
        "ingredients": {"water": 50, "coffee": 18},
        "cost": 1.5,
        "image": "espresso.jpg"
    },
    "latte": {
        "ingredients": {"water": 200, "milk": 150, "coffee": 24},
        "cost": 2.5,
        "image": "latte.jpg"
    },
    "cappuccino": {
        "ingredients": {"water": 250, "milk": 100, "coffee": 24},
        "cost": 3.0,
        "image": "cappuccino.jpg"
    }
}

# Resources in stock
resources = {"water": 1000, "milk": 800, "coffee": 500}
profit = 0

@app.route("/")
def index():
    return render_template("index.html", menu=MENU, resources=resources, profit=profit)

@app.route("/order", methods=["POST"])
def order():
    global resources, profit
    data = request.json
    choice = data.get("drink")

    if choice not in MENU:
        return jsonify({"error": "Invalid drink selection"}), 400

    drink = MENU[choice]
    ingredients = drink["ingredients"]

    # Check if enough resources are available
    for item in ingredients:
        if resources.get(item, 0) < ingredients[item]:
            return jsonify({"error": f"Sorry, not enough {item}."}), 400

    # Process the payment
    money_received = data.get("money", 0)
    if money_received < drink["cost"]:
        return jsonify({"error": "Not enough money. Money refunded."}), 400

    # Deduct resources and add profit
    for item in ingredients:
        resources[item] -= ingredients[item]
    profit += drink["cost"]

    # Calculate change
    change = round(money_received - drink["cost"], 2)

    # Return updated resources and profit
    return jsonify({
        "message": f"Here is your {choice}. Enjoy!",
        "change": change,
        "resources": resources,
        "profit": profit
    })

if __name__ == "__main__":
    app.run(debug=True)
