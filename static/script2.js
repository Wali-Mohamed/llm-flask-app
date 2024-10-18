document.addEventListener('DOMContentLoaded', () => {
    const questionInput = document.getElementById('question-input');
    const submitButton = document.getElementById('submit-question');
    const answerSection = document.getElementById('answer-section');
    const answerText = document.getElementById('answer-text');
    const thumbUp = document.getElementById('thumb-up');
    const thumbDown = document.getElementById('thumb-down');

    let currentConversationId = null;

    submitButton.addEventListener('click', async () => {
        const question = questionInput.value.trim();
        if (question) {
            try {
                const response = await fetch('/question', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ question }),
                });
                const data = await response.json();
                answerText.textContent = data.answer;
                currentConversationId = data.conversation_id;
                answerSection.style.display = 'block';
            } catch (error) {
                console.error('Error:', error);
                answerText.textContent = 'An error occurred while fetching the answer.';
            }
        }
    });
function sendFeedback(feedback) {
    if (currentConversationId) {
        fetch('/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                conversation_id: currentConversationId,
                feedback: feedback,
            }),
        })
        .then(response => response.json())
        .then(data => console.log(data.message))
        .catch(error => console.error('Error:', error));
    }
}

thumbUp.addEventListener('click', () => sendFeedback(1));
thumbDown.addEventListener('click', () => sendFeedback(-1));
// Function to clear the question and answer
function clearQuestionAndAnswer() {
    questionInput.value = '';  // Clear the input field
    answerText.textContent = '';  // Clear the answer text
    answerSection.style.display = 'none';  // Optionally hide the answer section
}
});