// Add the "active" class to the current button (highlight it)
var header = document.getElementById("myTopnav");
var btns = header.getElementsByClassName("btn");
for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function() {
        var current = document.getElementsByClassName("active");
        current[0].className = current[0].className.replace(" active", "");
        this.className += " active";
    });
}

const form = document.querySelector('form');
const feedbackReceived = document.getElementById('feedback-received');
const feedbackText = document.getElementById('feedback-text');

