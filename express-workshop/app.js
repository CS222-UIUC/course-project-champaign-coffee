// import express module
var express = require("express");
// initializes Express app
var app = express();

const bodyParser = require('body-parser'); 
app.use(bodyParser.json()); 

// runs express server by running 'node app.js' on terminal
app.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
 });
 
  // homepage GET request
  app.get("/", (req, res) => {
     res.send("Hello, Express!"); 
  });
  
  // initialize array of things that make you happy
  // @TODO: reformat in JSON
  var happyArr = ["turtles", "dogs", "peppa pig"];

  // GET request for values that make you happy 
  app.get('/happiness', function (req, res) {
    return res.send(happyArr);
  });

  // POST request - can edit on Postman
  app.post('/happiness', function(req, res) {
      var happy = req.body;
      console.log(happy);
      happyArr.push(happy);
      res.send("An item that makes you happy was added :)");
  });

  app.put('/happiness', function(req, res) {
    // @TODO: include PUT request
  });

app.delete('/happiness', function(req, res) {
  // @TODO: include DELETE request
});