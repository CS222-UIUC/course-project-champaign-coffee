# Champaign Coffee Matcher :coffee:

Champaign Coffee Matcher is a Flask web application that recommends the best coffee for University of Illinois at Urbana-Champaign (UIUC) students. 

The app scrapes data from coffee shop menus in Champaign (see ``coffee_data``) then stores the data into a database (see ``db.py``) and uses a matching algorithm to give personalized recommendations based on the user's preferences as described in [algo-sketch.md](https://github.com/CS222-UIUC/course-project-champaign-coffee/blob/main/algo-sketch.md). 

Furthermore, users can rate the coffee and provide site feedback to help improve the recommendations.

# Tech Stack
* Flask
* Beautiful Soup (data webscraping)
* SQLite + SQLAlchemy
* Classic HTML/CSS/Javascript (frontend)

# Developers
* Danny Kim (backend/algo implementation)
* Eyad Loutfi (frontend/algo implementation)
* Minhyung Lee (database/backend)
* Monica Para (frontend/web scraping)

# Project Demo
https://mediaspace.illinois.edu/media/t/1_aipil0f2

# Installation
To run the project locally on your machine, make a copy of the repo in your terminal as
```bash
git clone https://github.com/CS222-UIUC/course-project-champaign-coffee
```

Install any necessary Python libraries and ``flask run`` to run the server locally as ``http://127.0.0.1:5000``

# Flask Handles
* ``/`` - landing page
* ``/discover`` - questionnaire for coffee selection
* ``/coffee_shops`` - view all Champaign coffee shops with toggle-able details
* ``/browse_coffees`` - browse all available items and view which shops offer them
* ``/ratings`` - select coffee shop and give feedback out of 5
* ``/submit_rating`` - coffee shop review submitted and stored in db
* ``/feedback`` - allows users to provide feedback on the site in general
* ``/submit-feedback`` - site feedback submitted
