import sqlite3
from flask import Flask, render_template, request, jsonify
from backend_rule_engine import create_rule, combine_rules, evaluate_rule, init_db

app = Flask(__name__)

# Initialize database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    rule_string = request.json['rule']
    rule_ast = create_rule(rule_string)
    return jsonify({'message': 'Rule created successfully', 'rule_ast': repr(rule_ast)})

@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    rule_ids = request.json['rule_ids']
    selected_rules = [get_rule_ast(rule_id) for rule_id in rule_ids]
    combined_rule = combine_rules(selected_rules)
    return jsonify({'message': 'Rules combined successfully', 'combined_rule': repr(combined_rule)})

@app.route('/evaluate_rule/<int:rule_id>', methods=['POST'])
def evaluate_rule_api(rule_id):
    user_data = request.json['user_data']
    rule_ast = get_rule_ast(rule_id)
    result = evaluate_rule(rule_ast, user_data)
    return jsonify({'result': result})

def get_rule_ast(rule_id):
    with sqlite3.connect('rules.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT rule_ast FROM rules WHERE id = ?", (rule_id,))
        row = cursor.fetchone()
    return eval(row[0]) if row else None

if __name__ == '__main__':
    app.run(debug=True)
