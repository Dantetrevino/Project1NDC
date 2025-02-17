# Import necessary modules for web application and real-time communication
from flask import Flask
from flask_socketio import SocketIO, emit
import webbrowser # Module to open URLs in a web browser     
import threading  # Module to handle threading for asynchronous tasks

app = Flask(__name__) # Initialize the Flask application
socketio = SocketIO(app)  # Enable WebSockets

# Store history of inputs and results
history = []

# Function to sort only the letters T, A, and M
def sort_letters(input_str):
    allowed_letters = {'T', 'A', 'M'}
    sorted_letters = ''.join(sorted([char for char in input_str if char in allowed_letters]))
    return sorted_letters

# HTML for the main menu
menu_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Letter Sorting App - Menu</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f4; }
        .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); width: 400px; margin: auto; margin-top: 10%; }
        button { margin: 10px; padding: 15px; width: 100%; font-size: 18px; background-color: #008CBA; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #005f73; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Letter Sorting App</h2>
        <p>Select an option:</p>
        <button onclick="window.location.href='/overview'">Overview</button>
        <button onclick="window.location.href='/program'">Go to Program</button>
    </div>
</body>
</html>
"""

# HTML for the Overview page
overview_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Overview</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f4; padding: 20px; }
        .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); max-width: 600px; margin: auto; }
        button { margin-top: 20px; padding: 10px; font-size: 16px; background-color: #008CBA; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #005f73; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Overview</h2>
        <p>This application allows you to input the letters T, A, and M in any order and sorts them correctly.</p>
        <p>The left side of the program displays the server status, while the right side shows the sorting interface.</p>
        <p><b>How does it work?</b></p>
        <p>The client communicates with the server using <b>WebSockets</b>. The client sends input letters to the server over a persistent connection. The server processes the data and returns the sorted result instantly.</p>
        <button onclick="window.location.href='/'">Back to Menu</button>
    </div>
</body>
</html>
"""

# HTML for the program (Client-Server UI)
program_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Letter Sorting Program</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.4.1/socket.io.js"></script>
    <style>
        body { font-family: Arial, sans-serif; display: flex; height: 100vh; margin: 0; background-color: #f4f4f4; }
        .half { width: 50%; padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .server { background-color: #ddd; }
        .client { background-color: #fff; }
        .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); width: 350px; text-align: center; }
        .box { width: 100%; height: 50px; border: 2px solid black; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; border-radius: 10px; margin-top: 10px; }
        input { font-size: 20px; padding: 10px; width: 90%; text-align: center; }
        button { margin-top: 10px; padding: 10px; width: 100%; font-size: 18px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="half server">
        <h2>Server Status</h2>
        <p>The server is running and ready to process WebSocket requests.</p>
        <h3>Recent Inputs:</h3>
        <ul id="historyList"></ul>
        <button onclick="window.location.href='/'">Back to Menu</button>
    </div>
    <div class="half client">
        <div class="container">
            <h2>Letter Sorting App</h2>
            <p>Enter the letters <b>T, A, or M</b> in any order below.</p>
            <input type="text" id="userInput">
            <button onclick="sendLetters()">Sort</button>
            <div class="box" id="output">Sorted Here</div>
        </div>
    </div>

    <script>
        var socket = io.connect('http://' + document.domain + ':' + location.port);

        function sendLetters() {
            let input = document.getElementById("userInput").value.toUpperCase();
            socket.emit('sort_letters', input);
        }

        socket.on('sorted_response', function(data) {
            document.getElementById("output").textContent = data.sorted_letters;
            updateHistory(data.input, data.sorted_letters);
        });

        socket.emit("get_history");

        socket.on("history_response", function(data) {
            let historyList = document.getElementById("historyList");
            historyList.innerHTML = "";
            data.history.forEach(entry => {
                let listItem = document.createElement("li");
                listItem.textContent = `Input: ${entry.input} → Sorted: ${entry.sorted}`;
                historyList.appendChild(listItem);
            });
        });

        function updateHistory(input, sorted) {
            let historyList = document.getElementById("historyList");
            let listItem = document.createElement("li");
            listItem.textContent = `Input: ${input} → Sorted: ${sorted}`;
            historyList.appendChild(listItem);
        }

        document.getElementById("userInput").addEventListener("click", function() {
            this.select();
        });
    </script>
</body>
</html>
"""

##This code defines a route for the root URL ("/") of a Flask web application. 
#When a user visits this URL, the home function is called, which returns the HTML content stored 
#in the menu_html variable, rendering it in the user's browser.
@app.route("/") 
def home():
    return menu_html


#This code snippet is using Flask, a Python web framework. It defines a route for the URL "/overview" 
#in a Flask application. When a user visits this URL, the overview() function is called. 
#This function returns the value of the overview_html variable, which contains HTML content. 
#This code is likely part of a web application that displays an overview page when the user navigates 
#to "/overview".
@app.route("/overview")
def overview():
    return overview_html

#This code defines a route for the URL "/program" in a Flask web application. When a user visits this URL, 
#the program function is called, which returns the HTML content stored in the program_html variable, 
#rendering it in the user's browser.
@app.route("/program")
def program():
    return program_html

#This code defines a WebSocket event handler for a "sort_letters" event. When this event is received, it:
#Sorts the input string using the sort_letters function.
#Appends the input and sorted result to a history list.
#Emits a "sorted_response" event to all connected clients, broadcasting the input and sorted result.
#socketio.on is a decorator from the Flask-SocketIO library, which registers the handle_sort function to handle incoming "sort_letters" events.
@socketio.on("sort_letters")
def handle_sort(input_str):
    sorted_result = sort_letters(input_str)
    history.append({"input": input_str, "sorted": sorted_result})
    emit("sorted_response", {"input": input_str, "sorted_letters": sorted_result}, broadcast=True)

#This code snippet is a WebSocket event handler that responds to a "get_history" event by emitting a 
#"history_response" event with the current history data.
@socketio.on("get_history")
def send_history():
    emit("history_response", {"history": history})

#This code snippet defines a function called open_browser that uses the webbrowser 
#module to open a web browser and navigate to the URL "http://127.0.0.1:5000/".
def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    socketio.run(app, debug=True)
