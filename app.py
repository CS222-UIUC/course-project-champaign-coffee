""" FLASK SERVER FOR WEB APP """
from flask import Flask, render_template, request, redirect, url_for
from db import CoffeeShop, Item, CoffeeData, session

app = Flask(__name__)
app_version = '1.0'


@app.route("/")
def home():
    """ default server """
    return render_template('index.html')


@app.route('/discover')
def discover():
   #  price1 = request.form['price1']
   #  price2 = request.form['price2']

   #  try:
   #      price1 = float(price1)
   #      price2 = float(price2)
   #      rating = float(rating)
   #  except ValueError:
   #      return render_template('ratings.html', error="Invalid input for price range.")

   #  if price1 < 0 or price2 < 0:
   #      return render_template('ratings.html', error="Price range must be non-negative.")

   #  if price1 > price2:
   #      return render_template('ratings.html', error="Minimum price cannot be greater than maximum price.")

   #   #local testing
   #  print(f"Price range: {price1}-{price2}")
    return render_template('discover.html')


@app.route('/ratings')
def ratings():
    return render_template('ratings.html')


@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    coffee_shop_name = request.form['coffee_shop']
    rating = request.form['rating']
    feedback = request.form['feedback']

    coffee_shop = session.query(CoffeeShop).filter(
        CoffeeShop.name == coffee_shop_name).first()

    if not coffee_shop:
        return render_template('ratings.html', error="Invalid coffee shop name.")

    coffee_shop.update_ratings(float(rating))
   #  session.add(self)
    session.commit()

    # local testing
    print(f"Coffee shop: {coffee_shop}")
    print(f"Rating: {rating}/5")
    print(f"Feedback: {feedback}")

    return render_template('ratings.html', submitted=True)


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    feedback = request.form.get('textbox')
    print(f"New feedback received: {feedback}")
    return render_template('feedback.html', feedback=feedback)


if __name__ == '__main__':
    app.run(debug=True)
