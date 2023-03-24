from flask import Flask, render_template, redirect
from flask import request, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "mokomichi1"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


currentSurvey = None
question = None
choices = None
text = None
startedSurvey = False

@app.route('/')
def home():
    

    surveyList = [survey for survey in surveys.surveys.keys()]
    surveyTitles = [surveys.surveys[survey].title for survey in surveyList]
    surveyInfo = [surveys.surveys[survey].instructions for survey in surveyList]
    numSurveys = len(surveyList)


    return render_template('home.html', num_surveys = numSurveys, surveys = surveyList, titles = surveyTitles, instructions = surveyInfo)


@app.route('/from_home' , methods =['GET','POST'])
def homeRouter():
   
    session['responses'] = []
    global currentSurvey
    global question
    global choices
    global text

    currentSurvey = str(request.form['survey-type'])
    
    question = surveys.surveys[currentSurvey].questions[len(session['responses'])].question
    choices = surveys.surveys[currentSurvey].questions[len(session['responses'])].choices
    text = surveys.surveys[currentSurvey].questions[len(session['responses'])].allow_text
    
    return redirect('/question')



@app.route('/handler', methods=['GET','POST'])
def handler():
    global question
    global choices
    global text
   
    if startedSurvey:
        answer = request.form['answer']
        response = session['responses']
        response.append(answer)
        session['responses'] = response

        if len(session['responses']) == len(surveys.surveys[currentSurvey].questions):
            session['responses'] = []

            return render_template('show_thanks.html')
    
    question = surveys.surveys[currentSurvey].questions[len(session['responses'])].question
    choices = surveys.surveys[currentSurvey].questions[len(session['responses'])].choices
    text = surveys.surveys[currentSurvey].questions[len(session['responses'])].allow_text
    
    return redirect('/question')
# use cookie to pass currentSurvey



@app.route('/question')
def return_question():
    global startedSurvey
    startedSurvey = True

    currRes = len(session['responses'])    

    if currentSurvey == None:
        return redirect('/')
    else:
        return render_template(f'question/{currRes}.html', question = question, choices = choices, text = text, current_s = currentSurvey )
   
    



    



