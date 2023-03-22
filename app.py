from flask import Flask, render_template, redirect, flash
from flask import request
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "mokomichi1"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


responses = []
currentSurvey = None
question = None
choices = None
text = None
startedSurvey = False

@app.route('/')
def home():
    global startedSurvey
    global responses

    startedSurvey = False
    responses = []
    
    surveyList = [survey for survey in surveys.surveys.keys()]
    surveyTitles = [surveys.surveys[survey].title for survey in surveyList]
    surveyInfo = [surveys.surveys[survey].instructions for survey in surveyList]
    numSurveys = len(surveyList)

    return render_template('home.html', num_surveys = numSurveys, surveys = surveyList, titles = surveyTitles, instructions = surveyInfo)


@app.route('/handler', methods=['GET','POST'])
def handler():
    global currentSurvey
    global question
    global choices
    global text
    global responses
    
    if startedSurvey:
        answer = request.form['answer']
        responses.append(answer)
    else:
        answer = ''
    
    currRes = len(responses)
    currentSurvey = str(request.form['survey-type'])
    

    if len(responses) == len(surveys.surveys[currentSurvey].questions):
        responses = []
        return render_template('show_thanks.html')
    
    question = surveys.surveys[currentSurvey].questions[currRes].question
    choices = surveys.surveys[currentSurvey].questions[currRes].choices
    text = surveys.surveys[currentSurvey].questions[currRes].allow_text
    
    return redirect('/question')
# use cookie to pass currentSurvey



@app.route('/question')
def return_question():
    global startedSurvey
    startedSurvey = True

    currRes = len(responses)    
    currResLen = str(currRes)
    questionLen = str(len(surveys.surveys[currentSurvey].questions))


    if currentSurvey == None:
        return redirect('/')
    else:
        return render_template(f'question/{currRes}.html', currRes = currResLen, question = question, choices = choices, text = text, current_s = currentSurvey )
    # from question.html route to /answer
    



    



