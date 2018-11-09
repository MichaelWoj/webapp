from flask import Flask, render_template, request
from operator import itemgetter
import time as t
import random
import pickle

app = Flask(__name__)

def checkLetters(source_word, word):
    source_charlist = list(source_word)

    for c in word:
        if c in source_charlist:
            source_charlist.remove(c)
        else:
            return False
    return True

def isAcceptable(tested):
    with open('accepted_words.txt', 'r') as f:
        for line in f:
            if tested in line.lower():
                return True
    return False

@app.route("/")
def welcome_screen():
    return render_template('welcome_screen.html', title='Welcome')

@app.route('/displayform')
def start_game_screen():
    session['sourceword'] = random.choice(
        list(open("sourcewords.txt"))).lower().strip()
    session['start_time'] = t.time()
    return render_template('game_screen.html', title='WordGame', header='WordGame')

@app.route('/processform', methods = ['POST'])
def process_form():
    session['score'] = round((t.time() - session['start_time']), 2)
    data = []
    invalid = []

    for k, v in request.form.items():
        v_low = v.lower()
        if (len(v_low) > 2 and
            v_low != session['sourceword'] and
            v_low not in data and
            checkLetters(session['sourceword'], low) and
                isAcceptable(v_low)):
            data.append(v_low)
        else:
            invalid.append(v_low)

    if len(data) == 7:
        return render_template('result_screen', title='Results', header='Success', data=data)
    else:
        return render_template('failure_screen', title='Reults', header= 'Failed', invalid=invalid)

@app.route('/topscorers', methods=['POST'])
def top_scores():
    usrname = request.form['name']
    score_list = []

    score_list = pickle.load(open('top_scores.p', 'wb'))

    score_list.append((usrname, session['score']))
    score_topten = score_list[:10]
    for index, item in enumerate(score_list):
        if item == (usrname, session['score']):
            current_index = index + 1

    if  current_index > 10:
        current_index = str(current_index)
        messege = ' '.join(['Rank: ', current_index, 'Score: ', str(session['score'])])
    else:
        messege = "Your result earned you a top 10 spot "

    pickle.dump(score_list, open('top_scores.p', 'wb'))

    return render_template('topten_screen.html', title='Top scores', score_topten=score_topten, messege=messege)


if __name__ =='__main__':
    app.run(debug=True)

app.secret_key = '\xa3k\xec\x81f\x84:\xc5@\x83\x9dhQ\x17\xd2\xc7'
