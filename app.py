""" FLASK SERVER FOR WEB APP """
from flask import Flask, render_template, request, redirect, url_for
from db import CoffeeShop, Item, CoffeeData, UserFeedback, SiteFeedback, session, ExtendedCoffeeData, recommended_coffee
from sqlalchemy.orm import joinedload
import config

app = Flask(__name__)
app_version = '1.0'


@app.route("/")
def home():
    """ default server """
    return render_template('index.html')


@app.route('/discover', methods=['GET', 'POST'])
def discover():
    result = None
    if request.method == 'POST':
        print(request.form)
        if request.form.get('min-price') == '':
            min_price = 0.0
        else:
            min_price = float(request.form.get('min-price'))
        if request.form.get('max-price') == '':
            max_price = float('inf')  # float infinity to avoid bugs
        else:
            max_price = float(request.form.get('max-price'))
        rating_importance = int(request.form.get('coffee-preference4', 0))
        proximity_importance = int(request.form.get('coffee-preference3', 0))
        coffee_type = str(request.form.get('coffee-preference1', "Tea"))
        # min_price = 1
        # max_price = 4
        # rating_importance = 0
        # proximity_importance = 0
        # coffee_type = "Latte"
        result = recommended_coffee(
            min_price, max_price, rating_importance, proximity_importance, coffee_type)
        print(result)
    return render_template('discover.html', result=result)


@app.route('/coffee_shops')
def coffee_shops():
    coffee_shop_details = []
    api_key = config.GOOGLE_MAPS_API_KEY
    for shop in session.query(CoffeeShop).all():
        feedbacks = session.query(UserFeedback).filter(
            UserFeedback.coffee_shop_id == shop.id).all()
        coffee_shop_details.append({
            'shop': shop,
            'feedbacks': feedbacks
        })
    shop_id = request.args.get('shop_id')
    return render_template('coffee_shops.html', coffee_shop_details=coffee_shop_details, shop_id=shop_id)


@app.route('/browse_coffees')
def browse_coffees():
    items = session.query(Item).all()
    coffee_items = []
    for item in items:
        shops = session.query(CoffeeData).options(joinedload(
            CoffeeData.coffee_shop)).filter(CoffeeData.item_id == item.id).all()
        coffee_items.append((item, shops))

    return render_template('browse_coffees.html', coffee_items=coffee_items)


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
    session.commit()

    user_feedback = UserFeedback(
        coffee_shop_id=coffee_shop.id, rating=rating, feedback=feedback)
    session.add(user_feedback)
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

    site_feedback = SiteFeedback(feedback=feedback)
    session.add(site_feedback)
    session.commit()

    print(f"New feedback received: {feedback}")
    return render_template('feedback.html', feedback=feedback)


if __name__ == '__main__':
    app.run(debug=True)
