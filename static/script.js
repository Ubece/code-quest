let currentChallenge = 0;

const challenges = [
    {
        description: "First Challenge: Unlock the Door\n\nTo unlock the door, you need to write a simple Python function.\nThe function should take a number as input and return the number doubled.\nHere's the function signature:\ndef double_number(num):"
    },
    {
        description: "If Statement Challenge\n\nWrite a function that takes a number as input and returns 'Even' if the number is even and 'Odd' if the number is odd.\nHere's the function signature:\ndef check_even_odd(num):"
    },
    {
        description: "Loop Challenge\n\nWrite a function that takes a list of numbers as input and returns a new list with each number doubled.\nHere's the function signature:\ndef double_list(numbers):"
    },
    {
        description: "Nested Loop Challenge\n\nWrite a function that generates a multiplication table (as a list of lists) for numbers 1 through 5.\nHere's the function signature:\ndef multiplication_table():"
    },
    {
        description: "Function Parameters Challenge\n\nWrite a function that calculates the factorial of a number.\nHere's the function signature:\ndef factorial(n):"
    },
    {
        description: "List Manipulation Challenge\n\nWrite a function that removes duplicates from a list.\nHere's the function signature:\ndef remove_duplicates(lst):"
    },
    {
        description: "Dictionary Usage Challenge\n\nWrite a function that counts the frequency of elements in a list.\nHere's the function signature:\ndef count_frequency(lst):"
    }
];

function displayChallenge() {
    const challenge = challenges[currentChallenge];
    document.getElementById("game-output").innerText = challenge.description;
}

async function submitCode() {
    const userCode = document.getElementById("user-code").value;

    const response = await fetch('/submit_code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            code: userCode,
            challenge_index: currentChallenge
        })
    });

    const result = await response.json();

    if (result.result === "correct") {
        document.getElementById("game-feedback").innerText = "Correct! Moving to the next challenge.";
        document.getElementById("game-feedback").classList.add("correct");
        currentChallenge++;
        if (currentChallenge < challenges.length) {
            setTimeout(() => {
                window.location.reload();
            }, 1000); // 1-second delay before reloading the page
        } else {
            document.getElementById("game-output").innerText = "Congratulations! You have completed all the challenges.";
            document.getElementById("game-input").style.display = "none";
        }
    } else if (result.result === "incorrect") {
        document.getElementById("game-feedback").innerText = "Incorrect code. Please try again.";
        document.getElementById("game-feedback").classList.remove("correct");
    } else {
        document.getElementById("game-feedback").innerText = `Error: ${result.message}`;
        document.getElementById("game-feedback").classList.remove("correct");
    }
}

async function fetchCurrentChallenge() {
    const response = await fetch('/get_challenge');
    const data = await response.json();
    currentChallenge = data.current_challenge;
    displayChallenge();
}

window.onload = function() {
    fetchCurrentChallenge();
}
