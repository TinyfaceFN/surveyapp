from flask import Flask, request, render_template,redirect,session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY']='12345'
debug = DebugToolbarExtension(app)
app.debug=True

sat_survey = satisfaction_survey 

@app.route('/')
def home():
    session['question'] = 0
    session['responses'] = []
    questiontitle = sat_survey.title
    return render_template('home.html',questiontitle=questiontitle)

@app.route(f'/question')
def survey1():
    questionnum= session.get('question')
    questiontitle = sat_survey.title
    question1= sat_survey.questions[questionnum]
    responses = session.get('responses')
    # if len(responses) != len(sat_survey.questions):
    #     return render_template('complete.html')
    return render_template('questions/1.html', questiontitle=questiontitle, question1=question1)

@app.route('/answer',methods=['POST'])
def answers():
    session['question'] += 1
    responses = session.get('responses', [])
    responses.append(request.form['answer'])
    session['responses'] = responses
    print(session['responses']) 
    if len(responses) >= len(sat_survey.questions):
        session['question'] = 0
        session['responses'] = []
        return render_template('complete.html')
    return redirect('/question')

if __name__ == '__main__':
    app.run(debug = True)