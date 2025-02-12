from flask import Flask, request, jsonify
import webbrowser
import threading

app = Flask(__name__)

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Letter Sorting App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background-color: #f4f4f4;
            text-align: center;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 350px;
        }
        .box {
            width: 100%;
            height: 50px;
            border: 2px solid black;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: bold;
            background: #fff;
            border-radius: 10px;
            margin-top: 10px;
        }
        input {
            font-size: 20px;
            padding: 10px;
            width: 90%;
            text-align: center;
        }
        button {
            margin-top: 10px;
            padding: 10px;
            width: 100%;
            font-size: 18px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        p {
            font-size: 18px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Letter Sorting App</h2>
        <p>Enter the letters <b>T, A, or M</b> in any order below. Click "Sort" to arrange them correctly.</p>
        <p>The letters will then be placed in order of <b>T, A, then M. <b><p>
        <input type="text" id="userInput">
        <button onclick="sortLetters()">Sort</button>
        <div class="box" id="output">Sorted Here</div>
    </div>

    <script>
        function sortLetters() {
            let input = document.getElementById("userInput").value.toUpperCase();
            fetch("/sort_letters", {
                method: "POST",
                body: JSON.stringify({ letters: input }),
                headers: { "Content-Type": "application/json" }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    document.getElementById("output").textContent = data.sorted_letters;
                }
            });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return html_content

@app.route("/sort_letters", methods=["POST"])
def sort_letters():
    data = request.json
    user_input = data.get("letters", "").upper()

    if not all(char in "TAM" for char in user_input):
        return jsonify({"error": "Invalid input! Only T, A, and M are allowed."})

    sorted_string = ''.join(sorted(user_input, key="TAM".index))
    return jsonify({"sorted_letters": sorted_string})

def open_browser():
    """Opens the default web browser automatically."""
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()  # Open browser after 1 second
    app.run(debug=True)
