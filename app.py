from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
@app.route("/displayform")
def display_form():
    return render_template("Welcome_screen.html", the_title="Welcome")


@app.route("/displayform")
def game_screen():
    return render_template("Game_screen.html", the_title="Lets play")
@app.route("/processform", methods=["POST"])
def find_words(length, letters):
    seven_words = set()
    for w in words:
        w = w.




app.run(debug=True)
