from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route("/list")
def list_questions():
    questions = data_manager.get_questions()
    if 'order_by' in request.form:
        return render_template(f'/list?ored_by{request.form["order_by"]}&order_direction{request.form["order_direction"]}')
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>')
def display_question(question_id):
    answers_from_file = data_manager.get_answers()
    questions = data_manager.get_questions()
    answers_for_question, question_details = [], []

    for answer in answers_from_file:
        if question_id == answer['id']:
            answers_for_question.append(answer)

    for question in questions:
        if question_id == question['id']:
            question_details.append(question['title'])
            question_details.append(question['message'])
            return render_template('display_question.html', question_id=question_id, answers=answers_from_file, question_details=question_details)


@app.route('/test')
def test_answer():
    return render_template('test.html', question_id=1)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def post_answer(question_id):
    questions = data_manager.get_questions()
    answers = data_manager.get_answers()
    if request.method == 'GET':
        selected_answers = [answer for answer in answers if answer['question_id'] == question_id]
        for question in questions:
            if question['id'] == question_id:
                selected_question = question
                break
        return render_template('post_answer.html', question=selected_question, answers=selected_answers)
    else:
        new_answer = {}
        for key, value in request.form.items():
            new_answer[key] = value
        answers.append(new_answer)
        return redirect('/test')

@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        questions = data_manager.get_questions()
        question = {}
        for key, value in request.form.items():
            question[key] = value
        questions.append(question)
        data_manager.export_questions(questions)
        return redirect('/')
    return render_template('add_question.html')


@app.route('/sort-question')
def sort_question():
    return render_template('sort_question.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            debug=True,
            port=8000)
