# Champaign Coffee Matcher

Champaign Coffee Matcher is a Flask web application that recommends the best coffee for University of Illinois at Urbana-Champaign (UIUC) students. 

The app scrapes data from coffee shop menus in Champaign (see ``coffee_data``) then stores the data into a database ``db.py`` and uses a matching algorithm to give personalized recommendations based on the user's preferences as described in [algo-sketch.md](https://github.com/CS222-UIUC/course-project-champaign-coffee/blob/main/algo-sketch.md). 

Furthermore, users can rate the coffee and provide site feedback to help improve the recommendations.

# Developers
Danny Kim, Eyad Loutfi, Minhyung Lee, Monica Para

# Project Demo
(GIF demo to be included)

# Installation
To run the project locally on your machine, make a copy of the repo in your terminal as
```bash
git clone https://github.com/CS222-UIUC/course-project-champaign-coffee
```

Install any necessary Python libraries and ``flask run`` to run the server locally as ``http://127.0.0.1:5000``

# Flask Handles
* ``/`` - landing page
* ``/discover`` - questionnaire for coffee selection
* ``/ratings`` - select coffee shop and give feedback out of 5
* ``/submit_rating`` - coffee shop review submitted and stored in db
* ``/feedback`` - allows users to provide feedback on the site in general
* ``/submit-feedback`` - site feedback submitted
* more handles to be included when finalized
