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
        os.popen('cp Rankings/DefendersRank.csv Rankings/DefendersRank\ copy.csv')
        os.popen('cp Rankings/ForwardsRank.csv Rankings/ForwardsRank\ copy.csv')
        os.popen('cp Rankings/GoalieRank.csv Rankings/GoalieRank\ copy.csv')
        os.popen('cp Rankings/midRank.csv Rankings/midRank\ copy.csv')
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
