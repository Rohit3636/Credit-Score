let currentQuestionIndex = 0;
let responses = {};  // Object to store user responses

// Function to display the current question and options
function displayQuestion(index) {
    if (!questions[index]) {
        console.error("Question not found at index:", index);
        return;
    }

    const question = questions[index];
    console.log("Displaying question:", question);  // Debug log

    document.getElementById('questionNumber').innerText = index + 1;
    document.getElementById('questionText').innerText = question.text;

    const optionsContainer = document.getElementById('optionsContainer');
    optionsContainer.innerHTML = '';  // Clear previous options

    // Loop to display each option for the current question
    question.options.forEach(option => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'form-check';
        optionDiv.innerHTML = `
            <input class="form-check-input" type="radio" name="question${question.id}" id="option${option.id}" value="${option.text}"
            ${responses[question.id] === option.text ? 'checked' : ''}>
            <label class="form-check-label" for="option${option.id}">${option.text}</label>
        `;
        optionsContainer.appendChild(optionDiv);
    });

    // Manage the visibility of navigation and submit buttons
    document.getElementById('prevBtn').style.display = index === 0 ? 'none' : 'inline-block';
    document.getElementById('nextBtn').style.display = index === questions.length - 1 ? 'none' : 'inline-block';
    document.getElementById('submitBtn').style.display = index === questions.length - 1 ? 'inline-block' : 'none';
}

// Function to navigate between questions
function navigateQuestion(direction) {
    console.log("Navigating direction:", direction);
    console.log("Current index before navigation:", currentQuestionIndex);

    // Save the current response before navigating
    const selectedOption = document.querySelector(`input[name="question${questions[currentQuestionIndex].id}"]:checked`);
    if (selectedOption) {
        responses[questions[currentQuestionIndex].id] = selectedOption.value;
        console.log("Saved response for question", questions[currentQuestionIndex].id, ":", selectedOption.value);
    }

    // Update the current question index and display the next/previous question
    currentQuestionIndex += direction;
    displayQuestion(currentQuestionIndex);
}


// Function to submit responses
function submitResponses() {
    const selectedOption = document.querySelector(`input[name="question${questions[currentQuestionIndex].id}"]:checked`);
    if (selectedOption) {
        responses[questions[currentQuestionIndex].id] = selectedOption.value;
    }

    // Hide the question container, header, and footer; display the animation
    document.getElementById('questionContainer').style.display = 'none';
    document.getElementById('modalHeader').style.display = 'none';
    document.getElementById('modalFooter').style.display = 'none';
    document.getElementById('animationContainer').style.display = 'block';

    // Prepare the data to be sent via AJAX
    const csrftoken = document.getElementById('csrfToken').value;  // Get CSRF token
    const responseData = {
        responses: responses
    };

    // Send the data using AJAX
    fetch('/submit-responses/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(responseData)
    })
    .then(response => response.json())
    .then(data => {
        // Hide the animation after a delay and display the credit score
        setTimeout(() => {
            document.getElementById('animationContainer').style.display = 'none';
            document.getElementById('modalHeader').style.display = 'flex';  // Show only the close button
            document.getElementById('modalBody').style.textAlign = 'center';

            if (data.success) {
                document.getElementById('creditScore').innerText = `Your Credit Score: ${data.credit_score} / 900`;
                document.getElementById('creditScoreContainer').style.display = 'block';
            } else {
                alert('An error occurred while submitting your responses. Please try again.');
            }
        }, 1500);  // Delay to show the animation for a while
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('animationContainer').style.display = 'none';
        alert('An error occurred. Please check your network and try again.');
    });
}

// Initialize the first question when the document is loaded or modal is shown
document.addEventListener('DOMContentLoaded', () => {
    if (questions.length > 0) {
        currentQuestionIndex = 0;  // Reset the current question index
        responses = {};  // Clear previous responses
        displayQuestion(currentQuestionIndex);
    } else {
        console.error("No questions available to display.");
    }
});


