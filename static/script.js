document.addEventListener('DOMContentLoaded', () => {
    const questionInput = document.getElementById('question-input');
    const submitButton = document.getElementById('submit-question');
    const answerSection = document.getElementById('answer-section');
    const answerText = document.getElementById('answer-text');
    const thumbUp = document.getElementById('thumb-up');
    const thumbDown = document.getElementById('thumb-down');

    let currentConversationId = null;

    // Handle question submission
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
                
                // Enable feedback buttons when a new answer is fetched
                thumbUp.disabled = false;
                thumbDown.disabled = false;

            } catch (error) {
                console.error('Error:', error);
                answerText.textContent = 'An error occurred while fetching the answer.';
            }
        }
    });

    // Function to send feedback
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
            .then(data => {
                console.log(data.message);

                // Clear question and answer after feedback is submitted
                clearQuestionAndAnswer();

                // Disable feedback buttons after feedback is submitted
                thumbUp.disabled = true;
                thumbDown.disabled = true;
            })
            .catch(error => console.error('Error:', error));
        }
    }

    // Feedback buttons
    thumbUp.addEventListener('click', () => sendFeedback(1));
    thumbDown.addEventListener('click', () => sendFeedback(-1));

    // Function to clear the question and answer
    function clearQuestionAndAnswer() {
        questionInput.value = '';  // Clear the input field
        answerText.textContent = '';  // Clear the answer text
        answerSection.style.display = 'none';  // Optionally hide the answer section
    }
});
