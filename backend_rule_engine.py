import re
import sqlite3

class Node:
    def __init__(self, type, left=None, right=None, value=None):
        """
        AST Node representing either an operator (AND/OR) or an operand (condition).
        :param type: 'operator' for AND/OR or 'operand' for condition
        :param left: left child node (for operator)
        :param right: right child node (for operator)
        :param value: condition (for operand) or operator type ('AND', 'OR')
        """
        self.type = type
        self.left = left
        self.right = right
        self.value = value


# SQLite database setup
DATABASE = 'rules.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS rules (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            rule_string TEXT,
                            rule_ast TEXT
                        )''')
        conn.commit()

# Helper function to parse and create AST for complex rules
def parse_tokens(tokens):
    """
    Parse tokens to generate an AST for nested rules.
    :param tokens: List of tokens in the rule string
    :return: Root node of the generated AST
    """
    stack = []
    operators = []
    
    precedence = {'OR': 1, 'AND': 2}

    def apply_operator():
        if operators:
            operator = operators.pop()
            right = stack.pop()
            left = stack.pop()
            stack.append(Node(type='operator', left=left, right=right, value=operator))
    
    for token in tokens:
        if token in precedence:
            while (operators and operators[-1] in precedence and
                   precedence[operators[-1]] >= precedence[token]):
                apply_operator()
            operators.append(token)
        else:
            stack.append(Node(type='operand', value=token))
    
    while operators:
        apply_operator()

    return stack[0] if stack else None

def create_rule(rule_string):
    """
    Parse the rule string to generate an AST representing the rule.
    :param rule_string: Rule in string format
    :return: Root node of the generated AST
    """
    # Split by spaces and brackets for better tokenization
    tokens = re.findall(r"[\w]+|[><=!]+|[()]|AND|OR", rule_string)
    ast = parse_tokens(tokens)

    # Persist rule in the database
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rules (rule_string, rule_ast) VALUES (?, ?)", (rule_string, repr(ast)))
        conn.commit()
    
    return ast

def combine_rules(rules):
    """
    Combine multiple rules (ASTs) into one by OR-ing them.
    :param rules: List of individual AST nodes
    :return: Root node of the combined AST
    """
    if not rules:
        return None
    combined_rule = rules[0]
    for rule in rules[1:]:
        combined_rule = Node(type='operator', left=combined_rule, right=rule, value='OR')
    return combined_rule

def evaluate_rule(node, data):
    """
    Evaluate the AST based on user data to determine if the user satisfies the rule.
    :param node: Root node of the AST
    :param data: Dictionary with user attributes
    :return: Boolean result of evaluation (True if user satisfies the rule, False otherwise)
    """
    if node.type == 'operator':
        left_eval = evaluate_rule(node.left, data)
        right_eval = evaluate_rule(node.right, data)
        if node.value == 'AND':
            return left_eval and right_eval
        elif node.value == 'OR':
            return left_eval or right_eval
    elif node.type == 'operand':
        return eval_operand(node.value, data)

def eval_operand(condition, data):
    """
    Evaluate operand conditions such as "age > 30".
    :param condition: The condition string (e.g., "age > 30")
    :param data: Dictionary with user attributes
    :return: Boolean result of the condition evaluation
    """
    try:
        return eval(condition, {}, data)
    except Exception as e:
        print(f"Error evaluating condition: {condition}, Error: {e}")
        return False
