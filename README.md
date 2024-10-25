6# Rule_Engine_with_AST

This project is a 3-tier rule engine application that determines user eligibility based on various attributes (e.g., age, department, income, experience). It uses an Abstract Syntax Tree (AST) to represent and evaluate conditional rules and provides a RESTful API to create, combine, and evaluate these rules dynamically.

Features
    Dynamic Rule Creation: Define conditional rules using AND/OR operators.
    Rule Combination: Combine multiple rules into a single AST representation.
    Rule Evaluation: Evaluate rules against user data to check eligibility.
    Error Handling: Handles invalid rules and data format issues gracefully.

Project Structure
    backend_rule_engine.py: Contains core logic to parse rules, build AST, and evaluate conditions.
    app.py: Sets up the Flask API for rule creation, combination, and evaluation.
    /templates/index.html: A simple UI to interact with the API.
    /data/rules.db: Stores rules data if using a database.

Prerequisites
    Python 3.x
    Flask
    SQLite (Optional, for persistent rule storage)

Dependencies
    Install the necessary dependencies using:
    pip install flask

Setup Instructions
    Clone the Repository:
    git clone https://github.com/rahulw11/Rule_Engine_AST.git
    cd Rule_Engine_AST

Run the Application:
    python app.py

Access the Application:
    Open your browser and go to http://localhost:5000.
    Use Postman or similar tools to interact with the API directly.

![Engine_rule](https://github.com/user-attachments/assets/d1de4a00-df00-4bac-96d8-183a9e48a0c4)
