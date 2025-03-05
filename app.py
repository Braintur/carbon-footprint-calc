from flask import Flask, render_template, request, jsonify
from google import genai

API_KEY= "AIzaSyCkdc_A-FjHHbS5_EweBmn2OEjEJ4_GgnU"
client = genai.Client(api_key=API_KEY)

app = Flask(__name__)

answers = []
answered = False
footprint = 0

questions = [
    {
        "question": "How do you get around?",
        "buttons": ["Walking/Cycling", "Public Transport", "Gas/Diesel Car", "Hybrid car", "Electric car"],
        "footprint": [0, 380, 2300, 1000, 650]
    },
    {
        "question": "How often do you fly by plane? (per year)",
        "buttons": ["Never", "1-2 Short flights", "1-2 Long flights", "3 or more"],
        "footprint": [0, 450, 2200, 3000]
    },
    {
        "question": "How old is your house?",
        "buttons": ["1-15 y.o.", "16-30 y.o.", "31-60 y.o.", "60+ y.o."],
        "footprint": [1000, 2000, 3000, 4000]
    }
]

@app.route('/')
def index():
    return render_template('index.html', question=questions[0], current_question_index=0, questions=questions)

@app.route('/next_question', methods=['POST'])
def next_question():
    global answered, footprint
    data = request.json
    current_question_index = data.get('current_question_index', 0)
    selected_text = data.get('selected_text')
    print(f"Button pressed: {selected_text}")
    answers.append(selected_text)
    print(current_question_index)
    if selected_text == "Continue":
        print("Continue")
    else:
        footprint += questions[current_question_index]["footprint"][questions[current_question_index]["buttons"].index(selected_text)]
        
    next_question_index = current_question_index + 1
    if next_question_index < len(questions):
        next_question = questions[next_question_index]
        return jsonify({
            "question": next_question["question"],
            "buttons": next_question["buttons"],
            "current_question_index": next_question_index
        })
    else:
        if answered:
            answered=False
            return jsonify({
                "question": f"Thank you for completing the survey. Based on the answers, your carbon footprint is {footprint/1000} tons of CO2 per year.",
                "buttons": [],
                "current_question_index": next_question_index
            })
        else: 
            prompt = "A person who cares about the environment has completed a survey. Here are the answers: \n"
            
            for i, question in enumerate(questions):
                prompt += f"{question['question']}: {answers[i]}\n"
            prompt += "Based on the answers, how the person can decrease their carbon footprint? (no longer then 40 words, your answer should address the person, be friendly and encouraging)"
            
            print(prompt)
            
            response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
            )
            
            answered = True
            return jsonify({
                "question": str(response.text),
                "buttons": ["Continue"],
                "current_question_index": next_question_index
            })
    

if __name__ == '__main__':
    app.run(debug=True)