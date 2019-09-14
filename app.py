from flask import Flask, request, redirect
from processing import generate_questions, get_definition, generate_choices

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/quizsetup', methods=['GET', 'POST'])
def quizsetup():
    global questions
    global definition
    global choices
    global answer
    global score
    global count
    global no
    score = 0
    count = 0
    answer = 0
    if request.method == 'POST':
        try:
            no = int(request.form['answer'])
        except:
            return f'''
                <html>
                    <body>
                        <p>How many questions?</p>
                        <form method='POST' action='/quizsetup'>
                        <p><input name='answer' /></p>
                        <p><input type='submit' value='Start'/></p>
                        </form>
                        <p>Do you really think {request.form['answer']} is a valid response?</p>
                    </body>
                </html>
                '''
        if not no > 0:
            return f'''
                <html>
                    <body>
                        <p>How many questions?</p>
                        <form method='POST' action='/quizsetup'>
                        <p><input name='answer' /></p>
                        <p><input type='submit' value='Start'/></p>
                        </form>
                        <p>Do you really think {request.form['answer']} is a valid response?</p>
                    </body>
                </html>
                '''
        questions = generate_questions(no)
        definition = get_definition(questions[0])
        choices = generate_choices(definition)
        return redirect('/quiz2')
    return f'''
        <html>
            <body>
                <p>How many questions?</p>
                <form method='POST' action='/quizsetup'>
                <p><input name='answer' /></p>
                <p><input type='submit' value='Start'/></p>
                </form>
            </body>
        </html>
    '''


@app.route('/quiz2', methods=['GET', 'POST'])
def quiz2():
    global count
    count += 1
    if request.method == 'POST':
        # definition = get_definition(questions[0])
        # choices = generate_choices(definition)
        try:
            answer = int(request.form['answer'])
        except:
            return f'''
            <html>
                <body>
                    <h3>Q{count}. {definition[0]}</h3>
                    <p>1. {choices[0]}</p>
                    <p>2. {choices[1]}</p>
                    <p>3. {choices[2]}</p>
                    <p>4. {choices[3]}</p>
                    <form method='POST' action='/quiz2'>
                    <p><input name='answer' /></p>
                    <p><input type='submit' value='Next'/></p>
                    </form>
                    <p>Do you really think {request.form['answer']} is a valid response?</p>
                </body>
            </html>
            '''
        if not 0 < answer < 5:
            return f'''
            <html>
                <body>
                    <h3>{definition[0]}</h3>
                    <p>1. {choices[0]}</p>
                    <p>2. {choices[1]}</p>
                    <p>3. {choices[2]}</p>
                    <p>4. {choices[3]}</p>
                    <form method='POST' action='/quiz2'>
                    <p><input name='answer' /></p>
                    <p><input type='submit' value='Next'/></p>
                    </form>
                    <p>Do you really think {request.form['answer']} is a valid response?</p>
                </body>
            </html>
            '''
        return redirect('/checkanswer')

    return f'''
            <html>
                <body>
                    <h3>{definition[0]}</h3>
                    <p>1. {choices[0]}</p>
                    <p>2. {choices[1]}</p>
                    <p>3. {choices[2]}</p>
                    <p>4. {choices[3]}</p>
                    <form method='POST' action='/quiz2'>
                    <p><input name='answer' /></p>
                    <p><input type='submit' value='Next'/></p>
                    </form>
                </body>
            </html>
        '''


@app.route('/checkanswer', methods=['GET', 'POST'])
def checkanswer():
    message = ''
    if request.method == 'POST':
        return redirect('/next')
    if choices[answer-1] == definition[1]:
        message = 'Correct'
        global score
        score += 1
    else:
        message = 'Incorrect'
    return f'''
            <html>
                <body>
                    <h3>{message}</h3>
                    <p>{definition[0]}</p>
                    <p>{definition[1]}</p>
                    <p>"{definition[2]}" "{definition[3]}"</p>
                    <p>(you answered {choices[answer-1]})</p>
                    <form method='POST' action='/checkanswer'>
                    <p><input type='submit' value='Next'/></p>
                    </form>
                </body>
            </html>
        '''


@app.route('/next', methods=['GET', 'POST'])
def next():
    global questions
    global definition
    global choices

    if len(questions) > 1:
        questions = questions[1:]
        definition = get_definition(questions[0])
        choices = generate_choices(definition)
        return redirect('/quiz2')

    return f'''
        <html>
            <body>
                <p>Quiz complete! You received {score} out of {no} ({(score / no) * 100}%).</p>
            </body>
        </html>
        '''
