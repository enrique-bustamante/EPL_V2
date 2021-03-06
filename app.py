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
        return (
      '''
      Copying Successful!<br>
      <br>
      <a href='/'>Return to main page</a>
      ''')
