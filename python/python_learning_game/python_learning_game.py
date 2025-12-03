import streamlit as st
import random
import re

# --- 1. Question/Lesson Data (The Content - Now 27 Lessons) ---
LESSONS_DATA = [
    {
        "concept": "Hello World - The Print Statement 🌎",
        "instruction": "The `print()` function is used to output text or values to the console. To output text, it must be enclosed in quotes.",
        "example": '`print("Python is fun!")`',
        "challenge": "Challenge: Type the command to print the exact phrase **'Hello Streamlit!'**",
        "answer": 'print("Hello Streamlit!")',
        "hint": "Remember the quotes around the text and the parentheses for the function call.",
        "type": "exact_match"
    },
    {
        "concept": "Variables - Storing Data 📦",
        "instruction": "Variables are containers for storing data values. Use the assignment operator (`=`) to assign a value to a variable. **Python accepts both single (') and double (\") quotes for strings.**",
        "example": '`country = "France"` or `continent = \'Europe\'`',
        "challenge": "Challenge: Create a variable named **`city`** and assign it the string value **'London'**.",
        "answer": "city = 'London'",
        "hint": "No `print()` is needed. Just the variable name, the equals sign, and the value in quotes.",
        "type": "quote_flexible"
    },
    {
        "concept": "Data Types - Assigning an Integer 🔢",
        "instruction": "Integers are whole numbers (e.g., 5, -10). To create a variable and assign it an integer value, you use the assignment operator (`=`), just like with strings.",
        "example": '`age = 25`',
        "challenge": "Challenge: Create a variable named **`count`** and assign it the integer value **42**.",
        "answer": "count = 42",
        "hint": "Integers do not require quotes.",
        "type": "exact_match"
    }, 
    {
        "concept": "Checking Data Type with type() 🔬", 
        "instruction": "The **`type()`** function is a built-in Python tool used to determine the data type of an object or variable.", 
        "example": '`type(age)`\n# Output: <class \'int\'>',
        "challenge": "Challenge: Type the command to find the data type of the **`count`** variable you created in the last lesson.",
        "answer": "type(count)",
        "hint": "The command is the function name followed by the variable name in parentheses.",
        "type": "exact_match"
    },
    {
        "concept": "Arithmetic: Addition Operator (+) ➕",
        "instruction": "The plus sign (`+`) is used to add numbers or numerical variables together.",
        "example": '`total = 10 + 5` or `new_age = age + 1`',
        "challenge": "Challenge: Assuming the variable `count` is 42, create a new variable named **`sum`** and assign it the result of **`count` + 8**.",
        "answer": "sum = count + 8",
        "hint": "The answer should only contain the variable assignment.",
        "type": "exact_match"
    },
    {
        "concept": "Arithmetic: Subtraction (-) and Multiplication (*) ✖️",
        "instruction": "The minus sign (`-`) is for subtraction, and the asterisk (`*`) is for multiplication.",
        "example": '`difference = 20 - 7`\n`area = 5 * 6`',
        "challenge": "Challenge: Calculate the total cost of 12 items at $5 each. Create a variable named **`cost`** and assign it the result of **12 * 5**.",
        "answer": "cost = 12 * 5",
        "hint": "Use the asterisk (*) for multiplication.",
        "type": "exact_match"
    },
    {
        "concept": "String Concatenation (Joining Text) 🔗", 
        "instruction": "The plus sign (`+`) joins two or more strings together (concatenation).",
        "example": '`first_name = "Jane"`\n`full_name = first_name + " Doe"`',
        "challenge": "Challenge: Create a variable named **`full_city`** and assign it the result of joining the variables **`city`** and the string **' Bridge'**.",
        "answer": "full_city = city + ' Bridge'",
        "hint": "The variable name comes first, then the operator, then the new string in quotes.",
        "type": "concatenation_flexible" 
    },
    {
        "concept": "Arithmetic: Division (/) and Floor Division (//) ➗", 
        "instruction": "Standard division (`/`) produces a **float**. Floor division (`//`) results in an **integer**.",
        "example": '`result_float = 7 / 2`\n# Output: 3.5\n`result_int = 7 // 2`\n# Output: 3',
        "challenge": "Challenge: Calculate the floor division of 17 divided by 5 (the whole number result). Create a variable named **`whole_parts`** and assign it the result of **17 // 5**.",
        "answer": "whole_parts = 17 // 5",
        "hint": "Use the double-slash operator (`//`).",
        "type": "exact_match"
    },
    {
        "concept": "Arithmetic: Modulus Operator (Remainder) %",
        "instruction": "The modulus operator (`%`) returns the **remainder** after performing a division.",
        "example": '`remainder_a = 10 % 3`\n# Output: 1',
        "challenge": "Challenge: Find the remainder when 20 is divided by 6. Create a variable named **`left_over`** and assign it the result of **20 % 6**.",
        "answer": "left_over = 20 % 6",
        "hint": "What number is left over after dividing 20 by 6?",
        "type": "exact_match"
    },
    {
        "concept": "Data Types: Boolean (True/False) 🚦", 
        "instruction": "A Boolean variable can only hold one of two values: **`True`** or **`False`** (capitalized and no quotes).",
        "example": '`is_active = True`',
        "challenge": "Challenge: Create a variable named **`is_valid`** and assign it the Boolean value **`True`**.",
        "answer": "is_valid = True",
        "hint": "Ensure the value is capitalized and has no quotes around it.",
        "type": "exact_match"
    },
    {
        "concept": "Comparison Operators: Equality (==) ⚖️",
        "instruction": "The **double equals sign** (`==`) checks if two values are equal. The result is always a Boolean value.",
        "example": '`is_equal = 10 == 10`\n# Output: True',
        "challenge": "Challenge: Create a variable named **`result_match`** and assign it the result of comparing if the string **'Python'** is equal to the string **'python'**.",
        "answer": "result_match = 'Python' == 'python'",
        "hint": "Remember that strings are case-sensitive.",
        "type": "quote_flexible"
    },
    {
        "concept": "Comparison Operators: Inequality (!=) ❌",
        "instruction": "The **exclamation mark followed by an equals sign** (`!=`) checks if two values are **NOT** equal to each other. The result is always a Boolean value (`True` or `False`).",
        "example": '`is_not_equal = 10 != 5`\n# Output: True',
        "challenge": "Challenge: Create a variable named **`result_diff`** and assign it the result of checking if the integer **20** is not equal to the integer **'20'** (the string).",
        "answer": "result_diff = 20 != '20'",
        "hint": "Remember that data types matter! An integer is not the same as a string.",
        "type": "exact_match"
    },
    {
        "concept": "Comparison Operators: Greater Than/Less Than (<, >) ⬆️⬇️",
        "instruction": "The **Greater Than** (`>`) and **Less Than** (`<`) operators are used to check the size relationship between two numbers.",
        "example": '`is_small = 5 < 10`\n# Output: True',
        "challenge": "Challenge: Create a variable named **`is_valid_score`** and assign it the result of checking if the number **75** is greater than the number **50**.",
        "answer": "is_valid_score = 75 > 50",
        "hint": "Use the correct operator to compare the two numbers.",
        "type": "exact_match"
    },
    {
        "concept": "Comparison Operators: Greater Than/Less Than or Equal To (<=, >=) 💯",
        "instruction": "These combined operators are used when the boundary condition itself is acceptable. The order matters: the sign (>, <) must come before the equals sign (=).",
        "example": '`passing = score >= 70`\n# True if 70 or higher',
        "challenge": "Challenge: Create a variable named **`is_passing`** and assign it the result of checking if a score of **85** is greater than or equal to **70**.",
        "answer": "is_passing = 85 >= 70",
        "hint": "Ensure the comparison operator is written correctly: the greater-than sign comes before the equals sign.",
        "type": "exact_match"
    },
    {
        "concept": "Control Flow: The `if` Statement and Indentation ✅",
        "instruction": "The `if` statement executes a block of code only if its condition is `True`. It must end with a colon (`:`). The code block that executes if the condition is true MUST be indented by 4 spaces or one tab.",
        "example": '`score = 90`\n`if score > 80:`\n`    print("Great job!")`\n# Output: Great job!',
        "challenge": "Challenge: Write a complete `if` statement that checks if the variable **`is_rainy`** is equal to **`True`**. If it is, print the string **'Bring an umbrella.'** (Remember the colon and the 4-space indentation for the print line!)",
        "answer": "if is_rainy == True:\n    print('Bring an umbrella.')",
        "hint": "The first line needs `if` and a condition ending in a colon. The second line must start with 4 spaces.",
        "type": "if_statement"
    },
    {
        "concept": "Control Flow: The `else` Statement 🚫",
        "instruction": "The `else` statement is paired with an `if` statement and runs when the `if` condition is `False`. It must be aligned with the `if` and end with a colon (`:`).",
        "example": '`score = 65`\n`if score >= 70:`\n`    print("Passed")`\n`else:`\n`    print("Failed")`\n# Output: Failed',
        "challenge": "Challenge: Complete the structure. If **`is_sunny`** is `True`, print **'Go hiking.'**. Otherwise (using `else`), print **'Stay inside and read.'**",
        "answer": "if is_sunny == True:\n    print('Go hiking.')\nelse:\n    print('Stay inside and read.')",
        "hint": "Ensure the `else:` aligns with the `if`, and the `print()` line underneath `else:` is indented.",
        "type": "if_else_statement"
    },
    {
        "concept": "Control Flow: The `elif` (Else If) Statement ➡️",
        "instruction": "The `elif` statement lets you check multiple conditions sequentially. It runs only if the preceding `if` or `elif` conditions were `False`. It requires its own condition and colon (`:`).",
        "example": '`temp = 40`\n`if temp > 50:`\n`    print("Hot")`\n`elif temp > 30:`\n`    print("Warm")`\n# Output: Warm',
        "challenge": "Challenge: Write a structure. If **`grade`** is greater than 90, print **'A'**. Use **`elif`** to check if `grade` is greater than 80, and if so, print **'B'**.",
        "answer": "if grade > 90:\n    print('A')\nelif grade > 80:\n    print('B')",
        "hint": "Ensure the `elif` line is not indented, has a condition, and ends in a colon. The print line below it must be indented.",
        "type": "if_elif_statement"
    },
    {
        "concept": "Control Flow: The Full `if/elif/else` Structure 🧠",
        "instruction": "This combines all three control flow statements: `if` for the first test, `elif` for secondary tests, and `else` for the final default case (if all other conditions are false).",
        "example": '`color = "red"`\n`if color == "blue":`\n`    print("Cold")`\n`elif color == "red":`\n`    print("Hot")`\n`else:`\n`    print("Neutral")`',
        "challenge": "Challenge: Complete a structure. If **`day`** is 'Sat', print **'Weekend'**. If `day` is 'Sun', print **'Weekend'**. Otherwise, print **'Weekday'**.",
        "answer": "if day == 'Sat':\n    print('Weekend')\nelif day == 'Sun':\n    print('Weekend')\nelse:\n    print('Weekday')",
        "hint": "Remember: The first `if` starts the block, `elif` checks the next condition, and `else` must be the last, unconditioned block.",
        "type": "if_elif_else_statement"
    },
    # --- LESSON 19 ---
    {
        "concept": "Iteration: The `while` Loop 🔄",
        "instruction": "The `while` loop executes its block as long as its condition is `True`. Like `if`, it needs a colon (`:`) and indentation. **Crucially**, the variable used in the condition must be changed inside the loop to prevent an infinite loop.",
        "example": '`count = 0`\n`while count < 3:`\n`    print("Looping")`\n`    count = count + 1`\n# Output: Looping (3 times)',
        "challenge": "Challenge: Write a complete `while` loop. Initialize a variable **`x`** to `0`. Loop while `x` is less than **2**. Inside the loop, print **'Counting'** and then update `x` by adding `1` to it.",
        "answer": "x = 0\nwhile x < 2:\n    print('Counting')\n    x = x + 1",
        "hint": "Your challenge requires four lines: initialization, the while statement, the indented print, and the indented counter update (e.g., `x = x + 1`).",
        "type": "while_loop"
    },
    # --- LESSON 20 ---
    {
        "concept": "Iteration: The `for` Loop and `range()` 🔢",
        "instruction": "The `for` loop iterates through items in a sequence. It often uses the built-in `range()` function to define the number of repetitions. It requires a temporary loop variable (like `i`), the `in` keyword, the sequence, a colon (`:`), and indentation.",
        "example": '`for i in range(3):`\n`    print("Hello")`\n# Output: Hello (3 times)',
        "challenge": "Challenge: Write a `for` loop that iterates over the numbers 0, 1, and 2. Use **`i`** as the loop variable. Inside the loop, print the string **'Repeat'**.",
        "answer": "for i in range(3):\n    print('Repeat')",
        "hint": "The `for` line needs a variable, the `in` keyword, `range(3)`, and a colon. The print line needs indentation.",
        "type": "for_loop"
    },
    # --- LESSON 21 ---
    {
        "concept": "Data Structures: Lists (Creation) 🖼️",
        "instruction": "A List is an ordered collection of items enclosed in square brackets (`[]`). Lists can hold different data types. They are defined by assigning the bracketed values to a variable.",
        "example": '`numbers = [1, 2, 3]`\n`names = ["Alice", "Bob"]`',
        "challenge": "Challenge: Create a list named **`colors`** and assign it the string values **'Red'**, **'Green'**, and **'Blue'**.",
        "answer": "colors = ['Red', 'Green', 'Blue']",
        "hint": "Remember to use square brackets (`[]`) and quote the string items.",
        "type": "list_creation"
    },
    # --- LESSON 22 ---
    {
        "concept": "Data Structures: Lists (Accessing Elements) 🔍",
        "instruction": "List items are accessed using their **index number** (position) inside square brackets (`[]`). The first item is always at **index 0**.",
        "example": '`fruits = ["apple", "banana", "cherry"]`\n`print(fruits[1])`\n# Output: banana',
        "challenge": "Challenge: Assuming the list **`colors`** is **`['Red', 'Green', 'Blue']`**, write the command to print the item at **index 0**.",
        "answer": "print(colors[0])",
        "hint": "Use the `print()` function with the list variable name followed by the index in square brackets (`[]`).",
        "type": "list_access"
    },
    # --- LESSON 23 ---
    {
        "concept": "Data Structures: Lists (Modification and Append) 📝",
        "instruction": "Lists are **mutable** (changeable). You can add a new item to the end using the built-in **`.append()`** method. This method is called directly on the list variable.",
        "example": '`my_list = [1, 2]`\n`my_list.append(3)`\n# my_list is now [1, 2, 3]',
        "challenge": "Challenge: Assuming the list **`colors`** is **`['Red', 'Green', 'Blue']`**, write the command to add the string **'Yellow'** to the end of the list.",
        "answer": "colors.append('Yellow')",
        "hint": "The method is `.append()`. Don't forget the parentheses and quotes around the item!",
        "type": "list_append"
    },
    # --- LESSON 24 ---
    {
        "concept": "Data Structures: Dictionaries (Creation) 📘",
        "instruction": "Dictionaries store data in **key: value** pairs, enclosed in **curly braces** (`{}`). Keys and values are separated by a colon, and pairs are separated by commas. Keys must be unique.",
        "example": '`person = {"name": "Alice", "age": 30}`',
        "challenge": "Challenge: Create a dictionary named **`profile`** with two key-value pairs: the key **'user'** set to the value **'admin'**, and the key **'id'** set to the integer value **101**.",
        "answer": "profile = {'user': 'admin', 'id': 101}",
        "hint": "Remember the curly braces (`{}`), quotes around string keys/values, and the colon separator.",
        "type": "dict_creation"
    },
    # --- LESSON 25 (NEW) ---
    {
        "concept": "Data Structures: Dictionaries (Accessing Values by Key) 🔑",
        "instruction": "Values in a dictionary are retrieved using their unique key inside square brackets (`[]`). Keys are usually strings and must be quoted.",
        "example": '`user = {"name": "Alex", "level": 5}`\n`print(user["name"])`\n# Output: Alex',
        "challenge": "Challenge: Assuming the dictionary **`profile`** is **`{'user': 'admin', 'id': 101}`**, write the command to print the value associated with the key **'user'**.",
        "answer": "print(profile['user'])",
        "hint": "Use `print()`, the dictionary name, and the quoted key inside square brackets.",
        "type": "dict_access"
    },
    # --- LESSON 26 (NEW) ---
    {
        "concept": "Data Structures: Dictionaries (Modification and Adding) ✏️",
        "instruction": "Dictionaries are mutable. You can update an existing value or add a new key-value pair by accessing the key in square brackets and assigning a new value.",
        "example": '`user = {"level": 5}`\n`user["level"] = 6`\n# user is now {"level": 6}',
        "challenge": "Challenge: Assuming the dictionary **`settings`** is **`{'dark_mode': True}`**, write the command to change the value of the key **'dark_mode'** to **`False`**.",
        "answer": "settings['dark_mode'] = False",
        "hint": "You need the dictionary name, the quoted key in brackets, the assignment operator (`=`), and the new boolean value.",
        "type": "dict_modify"
    },
    # --- LESSON 27 (NEW) ---
    {
        "concept": "Built-in Functions: Finding Length (`len()`) 📏",
        "instruction": "The `len()` function returns the number of items in a list, dictionary, or the number of characters in a string. It is essential for determining loop boundaries or collection sizes.",
        "example": '`items = [1, 2, 3]`\n`length = len(items)`\n# length is 3',
        "challenge": "Challenge: Assuming the list **`data`** is **`[10, 20, 30, 40]`**, create a variable named **`data_size`** and assign it the length of **`data`**.",
        "answer": "data_size = len(data)",
        "hint": "Use the assignment operator (`=`) and the `len()` function.",
        "type": "len_function"
    }
    # --- END LESSONS (27 Total) ---
]

# --- 2. Game State Management & Callbacks ---

def initialize_state():
    """Initializes or ensures the existence of all session state variables."""
    if 'q_index' not in st.session_state:
        st.session_state.q_index = 0
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'passed_lessons' not in st.session_state:
        st.session_state.passed_lessons = 0
    if 'passed_indices' not in st.session_state:
        st.session_state.passed_indices = set() 
    if 'correct' not in st.session_state:
        st.session_state.correct = False

def set_lesson(index):
    """Callback: Sets the current lesson index and resets attempts/correct state."""
    st.session_state.q_index = index
    st.session_state.attempts = 0
    st.session_state.correct = False

def next_lesson():
    """Advances the lesson index and resets attempts and correct state."""
    if st.session_state.q_index < len(LESSONS_DATA) - 1:
        st.session_state.q_index += 1
        st.session_state.attempts = 0
        st.session_state.correct = False
    else:
        st.session_state.q_index += 1 

def unlock_all_lessons():
    """Adds all lesson indices to the passed_indices set, skipping them."""
    total_lessons = len(LESSONS_DATA)
    all_indices = set(range(total_lessons))
    
    # 1. Update the set to include all lessons
    st.session_state.passed_indices.update(all_indices)
    
    # 2. Update the passed count
    st.session_state.passed_lessons = total_lessons
    
    # 3. Set the current index to the last lesson (or high number)
    if total_lessons > 0:
        st.session_state.q_index = total_lessons - 1 
    
    # 4. Reset temporary state
    st.session_state.attempts = 0
    st.session_state.correct = False

# --- 3. Core Logic ---

def normalize_code(code: str) -> str:
    """Normalizes whitespace and quotes for comparison."""
    # Replace common quote variations with single quotes for consistent comparison
    normalized = code.replace('"', "'").strip()
    
    # Normalize indentation to 4 spaces
    lines = normalized.split('\n')
    normalized_lines = []
    for line in lines:
        if line.lstrip() != line: # If line is indented
            # Replace any leading tabs or mixed spaces/tabs with 4 spaces
            line = '    ' + line.lstrip()
        normalized_lines.append(line)
        
    return '\n'.join(normalized_lines).strip()

def check_code_submission(user_code: str):
    """Checks the submitted code."""
    st.session_state.attempts += 1
    
    current_lesson = LESSONS_DATA[st.session_state.q_index]
    required_answer = normalize_code(current_lesson["answer"])
    user_code_normalized = normalize_code(user_code)
    
    is_correct = False
    match_type = current_lesson.get("type")

    # Helper function for conditional statement checks (L15, L16)
    def check_conditional(required_template: str, user_code: str):
        is_match = (user_code_normalized == required_answer)
        
        # Check for the simplified Pythonic form (e.g., `if is_sunny:` instead of `if is_sunny == True:`)
        if not is_match:
            if st.session_state.q_index == 14: # L15 (if)
                simplified_required = normalize_code("if is_rainy:\n    print('Bring an umbrella.')")
                is_match = (user_code_normalized == simplified_required)
            elif st.session_state.q_index == 15: # L16 (if/else)
                simplified_required = normalize_code("if is_sunny:\n    print('Go hiking.')\nelse:\n    print('Stay inside and read.')")
                is_match = (user_code_normalized == simplified_required)
                
        return is_match

    # --- NEW LESSON LOGIC (L25, L26, L27) ---
    
    # LESSON 27: len_function
    if match_type == "len_function":
        # Check for data_size = len(data) with flexible spacing
        pattern = re.compile(
            r"^data_size\s*=\s*len\s*\(\s*data\s*\)$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip()))

    # LESSON 26: dict_modify
    elif match_type == "dict_modify":
        # Check for settings['dark_mode'] = False with flexible quotes and spacing
        pattern = re.compile(
            r"^settings\s*\[\s*['\"]dark_mode['\"]\s*\]\s*=\s*False$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip().replace('"', "'")))

    # LESSON 25: dict_access
    elif match_type == "dict_access":
        # Check for print(profile['user']) with flexible quotes and spacing
        pattern = re.compile(
            r"^print\s*\(\s*profile\s*\[\s*['\"]user['\"]\s*\]\s*\)$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip().replace('"', "'")))

    # LESSON 24: dict_creation
    elif match_type == "dict_creation":
        # Check for profile={'user':'admin','id':101} or profile={'id':101,'user':'admin'}
        user_code_simple = user_code.strip().replace('"', "'")
        user_code_no_ws = re.sub(r'\s+', '', user_code_simple)
        # Allows reordering of key-value pairs
        is_correct = bool(re.match(r"^profile=\{('user':'admin','id':101|'id':101,'user':'admin')\}$", user_code_no_ws))


    # LESSON 23: list_append
    elif match_type == "list_append":
        # Check for colors.append('Yellow') with flexible quotes and spacing
        pattern = re.compile(
            r"^colors\s*\.\s*append\s*\(\s*['\"]Yellow['\"]\s*\)$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip().replace('"', "'")))


    # LESSON 22: list_access
    elif match_type == "list_access":
        # Check for print(colors[0]) with flexible spacing
        pattern = re.compile(
            r"^print\s*\(\s*colors\s*\[\s*0\s*\]\s*\)$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip()))


    # LESSON 21: list_creation
    elif match_type == "list_creation":
        # Allow flexible spacing around the list items and quotes
        pattern = re.compile(
            r"^colors\s*=\s*\[\s*['\"]Red['\"]\s*,\s*['\"]Green['\"]\s*,\s*['\"]Blue['\"]\s*\]$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip().replace('"', "'"))) 
        
    # LESSON 20-17, 12-16: for_loop, while_loop, conditionals
    elif match_type in ["for_loop", "while_loop", "if_elif_else_statement", "if_elif_statement"]:
        is_correct = (user_code_normalized == required_answer)
    
    elif match_type in ["if_else_statement", "if_statement"]:
        is_correct = check_conditional(current_lesson["answer"], user_code)

    elif match_type == "concatenation_flexible":
        # Logic for L7: full_city = city + ' Bridge'
        pattern = re.compile(
            r"^full_city\s*=\s*city\s*\+\s*['\"] Bridge['\"]\s*$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip()))
        
    elif match_type == "quote_flexible":
        # Logic for L11 (Comparison)
        if st.session_state.q_index == 10:
            p = re.compile(
                r"^result_match\s*=\s*['\"]Python['\"]\s*==\s*['\"]python['\"]\s*$", 
                re.IGNORECASE 
            )
            is_correct = bool(p.match(user_code.strip()))
        
        # Logic for L2 (Variable Assignment)
        elif st.session_state.q_index == 1: 
             var_name, var_value_quoted = required_answer.split('=', 1)
             var_value = var_value_quoted.strip().strip("'\"") 
             var_name = var_name.strip()
             pattern = re.compile(
                rf"^{re.escape(var_name)}\s*=\s*['\"]{re.escape(var_value)}['\"]$", 
                re.IGNORECASE 
             )
             is_correct = bool(pattern.match(user_code.strip()))
        else:
             is_correct = (user_code_normalized == required_answer)
                
    else:
        # Exact Match Logic (The rest of the lessons)
        is_correct = (user_code_normalized == required_answer)

    if is_correct:
        current_index = st.session_state.q_index
        
        if current_index not in st.session_state.passed_indices:
            st.session_state.passed_lessons += 1
            st.session_state.passed_indices.add(current_index)
        
        st.session_state.correct = True 
        st.balloons() 
        
    else:
        st.session_state.correct = False
        
        # Provide a specific warning for indentation/structure lessons
        if match_type in ["if_statement", "if_else_statement", "if_elif_statement", "if_elif_else_statement", "while_loop", "for_loop"]:
             st.error(
                f"❌ **RETRY.** Attempt **{st.session_state.attempts}**. "
                "Double-check your **COLONS** (`:`) and ensure lines are indented by 4 spaces (or a tab) *only* when they belong to a block (`if`, `elif`, `else`, `while`, or `for`)!"
            )
        else:
            st.toast("🚨 Try Again! Your syntax didn't match the required command.", icon="❌")


# --- 4. Display Functions ---

def display_lesson(lesson_data):
    """Renders the instruction, example, and code input area for the current lesson."""
    
    st.title(f"Lesson {st.session_state.q_index + 1}: {lesson_data['concept']}")
    st.markdown("---")
    
    st.markdown(f"### 📚 Concept Focus")
    st.info(lesson_data['instruction'])
    
    st.markdown(f"### 💻 Example")
    st.code(lesson_data['example'], language='python')
    
    st.markdown(f"### 3. Your Challenge")
    st.warning(lesson_data['challenge'])
    
    is_permanently_passed = st.session_state.q_index in st.session_state.passed_indices
    
    # 2. User Input Area (Code Editor)
    input_key = f"code_input_{st.session_state.q_index}" 
    
    # Pre-fill with answer if passed, otherwise use a multi-line placeholder if it's a block structure
    prefill_value = LESSONS_DATA[st.session_state.q_index]["answer"] if is_permanently_passed else ""
    
    # Custom Placeholders for complex multi-line inputs
    if not is_permanently_passed:
        if st.session_state.q_index == 14: # L15 (if)
            prefill_value = "if is_rainy == True:\n    "
        elif st.session_state.q_index == 15: # L16 (if/else)
            prefill_value = "if is_sunny == True:\n    \nelse:\n    "
        elif st.session_state.q_index == 16: # L17 (if/elif)
            prefill_value = "if grade > 90:\n    \nelif grade > 80:\n    "
        elif st.session_state.q_index == 17: # L18 (if/elif/else)
            prefill_value = "if day == 'Sat':\n    \nelif day == 'Sun':\n    \nelse:\n    "
        elif st.session_state.q_index == 18: # L19 (while loop)
            prefill_value = "x = 0\nwhile x < 2:\n    \n    "
        elif st.session_state.q_index == 19: # L20 (for loop)
            prefill_value = "for i in range(3):\n    "
        # L21-L27 are single-line, so they use the default empty string

    user_code = st.text_area(
        "Type your Python command(s) below and click 'Submit'. Be precise with indentation!",
        height=250 if st.session_state.q_index in [17, 18] else (200 if st.session_state.q_index in [14, 15, 16] else 100),
        key=input_key,
        value=prefill_value
    )
    
    # 3. Submission Logic
    submit_disabled_after_success = st.session_state.get('correct', False) 
    submit_disabled = submit_disabled_after_success and not is_permanently_passed
    
    if not submit_disabled:
        st.button("Submit Code", 
                  on_click=check_code_submission, 
                  args=(user_code,), 
                  type="primary")
        
    st.markdown("---")
    
    # === DEDICATED FEEDBACK AREA ===

    if is_permanently_passed or st.session_state.get('correct', False):
        
        if is_permanently_passed and not st.session_state.get('correct', False):
            st.success("🎉 **PASSED!** Click 'Next Lesson' to continue, or **edit the code and click 'Submit' to relearn/test.**")
        else:
            st.success("🎉 **PASS! Congratulations!** Excellent syntax. Click 'Next Lesson' to continue.")

        st.button("Next Lesson >>", on_click=next_lesson)
        
    elif st.session_state.attempts > 0:
        if st.session_state.attempts < 2:
            st.error(
                f"❌ **RETRY.** Attempt **{st.session_state.attempts}**. "
                "Please check your capitalization, quotes, and spacing, and type the command again."
            )
        else:
            # Display retry/error message with hint option
            st.error(
                f"❌ **RETRY.** Attempt **{st.session_state.attempts}**. "
                "The command didn't match the required syntax."
            )
            with st.expander("💡 Show Hint"):
                st.info(lesson_data["hint"])


def display_completion_screen():
    """Renders the final score and completion message."""
    st.balloons()
    st.title("✅ Congratulations! All Lessons Complete!")
    
    total_lessons = len(LESSONS_DATA)
    passed = len(st.session_state.passed_indices)
    st.markdown(f"## You completed **{passed}** out of **{total_lessons}** lessons.")
    
    st.info("You've built strong Python syntax muscle memory. Ready for the next level of challenges?")
    
    if st.button("Start Over"):
        st.session_state.clear()
        st.rerun()


def main():
    """The main function to run the Streamlit app."""
    st.set_page_config(page_title="Python Syntax Practice", layout="centered")
    
    initialize_state()

    total_lessons = len(LESSONS_DATA)
    current_lesson_num = st.session_state.q_index
    passed = len(st.session_state.passed_indices) 
    
    # --- SIDEBAR: Progress and Navigation ---
    with st.sidebar:
        st.title("Progress & Navigation")
        
        # --- UNLOCK FEATURE ---
        if st.button("🔓 Skip/Unlock All Lessons (For Testing)", type="secondary"):
            unlock_all_lessons()
            st.rerun() 
        st.markdown("---")
        # ----------------------
        
        # 1. Overall Progress
        st.write(f"**Passed Lessons:** {passed} of {total_lessons}")
        st.progress(passed / total_lessons if total_lessons > 0 else 0)
        st.markdown("---")
        
        # 2. Lesson Navigation Buttons
        st.markdown("### Jump to Lesson:")
        for i, lesson in enumerate(LESSONS_DATA):
            is_unlocked = i in st.session_state.passed_indices or i == current_lesson_num
            is_current = i == current_lesson_num
            
            icon = "➡️" if is_current else ("✅" if i in st.session_state.passed_indices else "🔒")
            label = f"L{i+1}: {lesson['concept']}"
            
            st.button(
                f"{icon} {label}", 
                key=f"nav_btn_{i}",
                on_click=set_lesson, 
                args=(i,),
                disabled=not is_unlocked and not st.session_state.get('passed_lessons', 0) == total_lessons,
                type="primary" if is_current else "secondary"
            )
            
    # --- MAIN CONTENT ---
    st.markdown("# 🚀 Interactive Python Syntax Practice")
    
    if st.session_state.q_index < total_lessons:
        display_lesson(LESSONS_DATA[st.session_state.q_index])
    else:
        display_completion_screen()

if __name__ == "__main__":
    main()
