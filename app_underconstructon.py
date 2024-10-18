import uuid
import os
from flask import send_from_directory



from flask import Flask, request, jsonify, render_template

from rag import rag

import db

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.route('/')
def home():
    return render_template('index.html')  # This looks for index.html inside the templates folder
@app.route("/question", methods=["POST"])
def handle_question():
    data = request.json
    question = data["question"]

    if not question:
        return jsonify({"error": "No question provided"}), 400

    conversation_id = str(uuid.uuid4())

    answer_data = rag(question)
    

    result = {
        "conversation_id": conversation_id,
        "question": question,
        "answer": answer_data,
    }

    db.save_conversation(
        conversation_id=conversation_id,
        question=question,
        answer_data=answer_data,
    )

    return jsonify(result)


@app.route("/feedback", methods=["POST"])
def handle_feedback():
    data = request.json
    print(type(data))
    print(data)
    conversation_id = data['conversation_id']
    feedback = data['feedback']

    if not conversation_id or feedback not in [1, -1]:
        return jsonify({"error": "Invalid input"}), 400

    db.save_feedback(
        conversation_id=conversation_id,
        feedback=feedback,
    )

    result = {
        "message": f"Feedback received for conversation {conversation_id}: {feedback}"
    }
    return jsonify(result)


if __name__ == "__main__":
    #app.run(debug=True)
    app.run(debug=True, use_reloader=True)
