from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

questions = [
    {
        "question": "How do you get around?",
        "buttons": ["Walking/Cycling", "Public Transport", "Gas/Diesel Car", "Hybrid car", "Electric car"]
    },
    {
        "question": "How often do you fly by plane? (per year)",
        "buttons": ["Never", "1-2 Short flights", "1-2 Long flights", "3 or more"]
    },
    {
        "question": "How old is your house?",
        "buttons": ["1-15 y.o.", "16-30 y.o.", "31-60 y.o.", "60+ y.o."]
    }
]

@app.route('/')
def index():
    return render_template('index.html', question=questions[0], current_question_index=0, questions=questions)

@app.route('/next_question', methods=['POST'])
def next_question():
    data = request.json
    current_question_index = data.get('current_question_index', 0)
    selected_text = data.get('selected_text')
    print(f"Button pressed: {selected_text}")

    next_question_index = current_question_index + 1
    if next_question_index < len(questions):
        next_question = questions[next_question_index]
        return jsonify({
            "question": next_question["question"],
            "buttons": next_question["buttons"],
            "current_question_index": next_question_index
        })
    else:
        return jsonify({
            "question": "Calculation complete!",
            "buttons": [],
            "current_question_index": next_question_index
        })

if __name__ == '__main__':
    app.run(debug=True)