from flask import Flask, render_template, request, jsonify, session
import sys
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    if 'current_challenge' not in session:
        session['current_challenge'] = 0
    return render_template('index.html')

@app.route('/get_challenge', methods=['GET'])
def get_challenge():
    challenge_index = session.get('current_challenge', 0)
    return jsonify({"current_challenge": challenge_index})

@app.route('/submit_code', methods=['POST'])
def submit_code():
    data = request.get_json()
    user_code = data['code']
    challenge_index = session.get('current_challenge', 0)

    challenges = [
        {
            "description": "First Challenge: Unlock the Door\n\nTo unlock the door, you need to write a simple Python function.\nThe function should take a number as input and return the number doubled.\nHere's the function signature:\ndef double_number(num):",
            "test_code": """
def double_number(num):
    return num * 2
test_result = double_number(2) == 4
"""
        },
        {
            "description": "If Statement Challenge\n\nWrite a function that takes a number as input and returns 'Even' if the number is even and 'Odd' if the number is odd.\nHere's the function signature:\ndef check_even_odd(num):",
            "test_code": """
def check_even_odd(num):
    return "Even" if num % 2 == 0 else "Odd"
test_result = check_even_odd(2) == "Even" and check_even_odd(3) == "Odd"
"""
        },
        {
            "description": "Loop Challenge\n\nWrite a function that takes a list of numbers as input and returns a new list with each number doubled.\nHere's the function signature:\ndef double_list(numbers):",
            "test_code": """
def double_list(numbers):
    return [num * 2 for num in numbers]
test_result = double_list([1, 2, 3]) == [2, 4, 6]
"""
        },
        {
            "description": "Nested Loop Challenge\n\nWrite a function that generates a multiplication table (as a list of lists) for numbers 1 through 5.\nHere's the function signature:\ndef multiplication_table():",
            "test_code": """
def multiplication_table():
    return [[i * j for j in range(1, 6)] for i in range(1, 6)]
test_result = multiplication_table() == [[1, 2, 3, 4, 5], [2, 4, 6, 8, 10], [3, 6, 9, 12, 15], [4, 8, 12, 16, 20], [5, 10, 15, 20, 25]]
"""
        },
        {
            "description": "Function Parameters Challenge\n\nWrite a function that calculates the factorial of a number.\nHere's the function signature:\ndef factorial(n):",
            "test_code": """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
test_result = factorial(5) == 120
"""
        },
        {
            "description": "List Manipulation Challenge\n\nWrite a function that removes duplicates from a list.\nHere's the function signature:\ndef remove_duplicates(lst):",
            "test_code": """
def remove_duplicates(lst):
    return list(set(lst))
test_result = remove_duplicates([1, 2, 2, 3, 4, 4]) == [1, 2, 3, 4]
"""
        },
        {
            "description": "Dictionary Usage Challenge\n\nWrite a function that counts the frequency of elements in a list.\nHere's the function signature:\ndef count_frequency(lst):",
            "test_code": """
def count_frequency(lst):
    freq = {}
    for item in lst:
        if item in freq:
            freq[item] += 1
        else:
            freq[item] = 1
    return freq
test_result = count_frequency([1, 2, 2, 3, 3, 3]) == {1: 1, 2: 2, 3: 3}
"""
        }
    ]

    combined_code = user_code + '\n' + challenges[challenge_index]['test_code']
    print("Combined code:\n", combined_code, file=sys.stderr)
    
    try:
        exec(combined_code, globals())
        print("Test result:", test_result, file=sys.stderr)
        if 'test_result' in globals():
            print("test_result:", test_result, file=sys.stderr)
        else:
            print("test_result not found in globals", file=sys.stderr)
        
        if 'test_result' in globals() and test_result:
            session['current_challenge'] = challenge_index + 1
            return jsonify({"result": "correct"})
        else:
            return jsonify({"result": "incorrect"})
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        return jsonify({"result": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
