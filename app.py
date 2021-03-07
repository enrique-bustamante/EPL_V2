# Import dependencies
from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/copies', methods=['POST'])
def copies():
    if request.method=='POST':
        os.popen('cp rankings/DefendersRank.csv Rankings/DefendersRank\ copy.csv')
        os.popen('cp rankings/ForwardsRank.csv Rankings/ForwardsRank\ copy.csv')
        os.popen('cp rankings/GoalieRank.csv Rankings/GoalieRank\ copy.csv')
        os.popen('cp rankings/midRank.csv Rankings/MidfielderRank\ copy.csv')
        return render_template('copies.html')

@app.route('/update', methods=['POST'])
def update():
    if request.method=='POST':
        os.popen('python eplWebscrape.py')
        return render_template('update.html')

@app.route('/defenders')
def defenders():
    return render_template('defenders.html')

@app.route('/goalies')
def goalies():
    return render_template('goalies.html')

@app.route('/midfielders')
def midfielders():
    return render_template('midfielders.html')

@app.route('/forwards')
def forwards():
    return render_template('forwards.html')


if __name__ == '__main__':
    app.run