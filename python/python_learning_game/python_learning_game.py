import streamlit as st
import random
import re
import pandas as pd # <-- Note: Included for completeness, though not strictly needed for the syntax checker

# --- 1. Question/Lesson Data (The Content - Now 57 Lessons) ---
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
        "example": '`score = 90`\n`if score > 80:`\n`    print("Great job!")`\n`# Output: Great job!`',
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
    {
        "concept": "Iteration: The `while` Loop 🔄",
        "instruction": "The `while` loop executes its block as long as its condition is `True`. Like `if`, it needs a colon (`:`). **Crucially**, the variable used in the condition must be changed inside the loop to prevent an infinite loop.",
        "example": '`count = 0`\n`while count < 3:`\n`    print("Looping")`\n`    count = count + 1`\n# Output: Looping (3 times)',
        "challenge": "Challenge: Write a complete `while` loop. Initialize a variable **`x`** to `0`. Loop while `x` is less than **2**. Inside the loop, print **'Counting'** and then update `x` by adding `1` to it.",
        "answer": "x = 0\nwhile x < 2:\n    print('Counting')\n    x = x + 1",
        "hint": "Your challenge requires four lines: initialization, the while statement, the indented print, and the indented counter update (e.g., `x = x + 1`).",
        "type": "while_loop"
    },
    {
        "concept": "Iteration: The `for` Loop and `range()` 🔢",
        "instruction": "The `for` loop iterates through items in a sequence. It often uses the built-in `range()` function to define the number of repetitions. It requires a temporary loop variable (like `i`), the `in` keyword, the sequence, a colon (`:`), and indentation.",
        "example": '`for i in range(3):`\n`    print("Hello")`\n`# Output: Hello (3 times)`',
        "challenge": "Challenge: Write a `for` loop that iterates over the numbers 0, 1, and 2. Use **`i`** as the loop variable. Inside the loop, print the string **'Repeat'**.",
        "answer": "for i in range(3):\n    print('Repeat')",
        "hint": "The `for` line needs a variable, the `in` keyword, `range(3)`, and a colon. The print line needs indentation.",
        "type": "for_loop"
    },
    {
        "concept": "Data Structures: Lists (Creation) 🖼️",
        "instruction": "A List is an ordered collection of items enclosed in square brackets (`[]`). Lists can hold different data types. They are defined by assigning the bracketed values to a variable.",
        "example": '`numbers = [1, 2, 3]`\n`names = ["Alice", "Bob"]`',
        "challenge": "Challenge: Create a list named **`colors`** and assign it the string values **'Red'**, **'Green'**, and **'Blue'**.",
        "answer": "colors = ['Red', 'Green', 'Blue']",
        "hint": "Remember to use square brackets (`[]`) and quote the string items.",
        "type": "list_creation"
    },
    {
        "concept": "Data Structures: Lists (Accessing Elements) 🔍",
        "instruction": "List items are accessed using their **index number** (position) inside square brackets (`[]`). The first item is always at **index 0**.",
        "example": '`fruits = ["apple", "banana", "cherry"]`\n`print(fruits[1])`\n# Output: banana',
        "challenge": "Challenge: Assuming the list **`colors`** is **`['Red', 'Green', 'Blue']`**, write the command to print the item at **index 0**.",
        "answer": "print(colors[0])",
        "hint": "Use the `print()` function with the list variable name followed by the index in square brackets (`[]`).",
        "type": "list_access"
    },
    {
        "concept": "Data Structures: Lists (Modification and Append) 📝",
        "instruction": "Lists are **mutable** (changeable). You can add a new item to the end using the built-in **`.append()`** method. This method is called directly on the list variable.",
        "example": '`my_list = [1, 2]`\n`my_list.append(3)`\n# my_list is now [1, 2, 3]',
        "challenge": "Challenge: Assuming the list **`colors`** is **`['Red', 'Green', 'Blue']`**, write the command to add the string **'Yellow'** to the end of the list.",
        "answer": "colors.append('Yellow')",
        "hint": "The method is `.append()`. Don't forget the parentheses and quotes around the item!",
        "type": "list_append"
    },
    {
        "concept": "Data Structures: Dictionaries (Creation) 📘",
        "instruction": "Dictionaries store data in **key: value** pairs, enclosed in **curly braces** (`{}`). Keys and values are separated by a colon, and pairs are separated by commas. Keys must be unique.",
        "example": '`person = {"name": "Alice", "age": 30}`',
        "challenge": "Challenge: Create a dictionary named **`profile`** with two key-value pairs: the key **'user'** set to the value **'admin'**, and the key **'id'** set to the integer value **101**.",
        "answer": "profile = {'user': 'admin', 'id': 101}",
        "hint": "Remember the curly braces (`{}`), quotes around string keys/values, and the colon separator.",
        "type": "dict_creation"
    },
    {
        "concept": "Data Structures: Dictionaries (Accessing Values by Key) 🔑",
        "instruction": "Values in a dictionary are retrieved using their unique key inside square brackets (`[]`). Keys are usually strings and must be quoted.",
        "example": '`user = {"name": "Alex", "level": 5}`\n`print(user["name"])`\n# Output: Alex',
        "challenge": "Challenge: Assuming the dictionary **`profile`** is **`{'user': 'admin', 'id': 101}`**, write the command to print the value associated with the key **'user'**.",
        "answer": "print(profile['user'])",
        "hint": "Use `print()`, the dictionary name, and the quoted key inside square brackets.",
        "type": "dict_access"
    },
    {
        "concept": "Data Structures: Dictionaries (Modification and Adding) ✏️",
        "instruction": "Dictionaries are mutable. You can update an existing value or add a new key-value pair by accessing the key in square brackets and assigning a new value.",
        "example": '`user = {"level": 5}`\n`user["level"] = 6`\n# user is now {"level": 6}',
        "challenge": "Challenge: Assuming the dictionary **`settings`** is **`{'dark_mode': True}`**, write the command to change the value of the key **'dark_mode'** to **`False`**.",
        "answer": "settings['dark_mode'] = False",
        "hint": "You need the dictionary name, the quoted key in brackets, the assignment operator (`=`), and the new boolean value.",
        "type": "dict_modify"
    },
    {
        "concept": "Built-in Functions: Finding Length (`len()`) 📏",
        "instruction": "The `len()` function returns the number of items in a list, dictionary, or the number of characters in a string. It is essential for determining loop boundaries or collection sizes.",
        "example": '`items = [1, 2, 3]`\n`length = len(items)`\n# length is 3',
        "challenge": "Challenge: Assuming the list **`data`** is **`[10, 20, 30, 40]`**, create a variable named **`data_size`** and assign it the length of **`data`**.",
        "answer": "data_size = len(data)",
        "hint": "Use the assignment operator (`=`) and the `len()` function.",
        "type": "len_function"
    },
    {
        "concept": "Dictionary Methods: Retrieving Keys (`.keys()`) 🔑",
        "instruction": "Use the `.keys()` method to get an iterable view of all keys in a dictionary. Wrap the result in `list()` to get a standard list of keys.",
        "example": '`user = {"name": "Alex", "level": 5}`\n`keys = list(user.keys())`\n# keys is now ["name", "level"]',
        "challenge": "Challenge: Assuming the dictionary **`profile`** is **`{'user': 'admin', 'id': 101}`**, create a variable named **`key_list`** and assign it a list of all the keys in `profile`.",
        "answer": "key_list = list(profile.keys())",
        "hint": "Start with the variable assignment, then use `list()` around the dictionary name followed by `.keys()`.",
        "type": "dict_keys"
    },
    {
        "concept": "Dictionary Methods: Retrieving Values (`.values()`) 📦",
        "instruction": "Use the `.values()` method to get an iterable view of all values in a dictionary. Wrap the result in `list()` to get a standard list of values.",
        "example": '`scores = {"math": 90, "science": 85}`\n`vals = list(scores.values())`\n# vals is now [90, 85]',
        "challenge": "Challenge: Assuming the dictionary **`profile`** is **`{'user': 'admin', 'id': 101}`**, create a variable named **`value_list`** and assign it a list of all the values in `profile`.",
        "answer": "value_list = list(profile.values())",
        "hint": "The syntax is almost identical to `.keys()`, but replace `keys` with `values`.",
        "type": "dict_values"
    },
    {
        "concept": "Dictionary Methods: Removing Items (`.pop()`) 🗑️",
        "instruction": "The `.pop()` method removes the specified key-value pair from the dictionary and returns the value of the removed item. The key must be provided inside the parentheses.",
        "example": '`data = {"a": 1, "b": 2}`\n`removed = data.pop("a")`\n# removed is 1. data is now {"b": 2}',
        "challenge": "Challenge: Assuming the dictionary **`profile`** is **`{'user': 'admin', 'id': 101}`**, write the command to remove the **'id'** key and its associated value from the dictionary.",
        "answer": "profile.pop('id')",
        "hint": "Call the method directly on the dictionary, including the quoted key in the parentheses.",
        "type": "dict_pop"
    },
    {
        "concept": "Functions: Defining a Function (`def`) ✍️",
        "instruction": "Define a function using the `def` keyword, a name, parentheses, and a colon. The body of the function is indented. For this challenge, define a function named **`greet`** that prints **'Hello!'**.",
        "example": '`def hello():`\n`    print("World")`',
        "challenge": "Challenge: Write a complete function definition for a function named **`greet`**. The body of the function should be a single line that prints the string **'Hello!'**.",
        "answer": "def greet():\n    print('Hello!')",
        "hint": "The `def` line needs to end with a colon. The print statement needs 4 spaces of indentation.",
        "type": "function_define"
    },
    {
        "concept": "Functions: Calling/Executing a Function 📞",
        "instruction": "After a function is defined, you execute its code block by calling it using its name followed by parentheses `()`.",
        "example": '`def hello():\n    print("World")`\n`hello()`\n# Output: World',
        "challenge": "Challenge: Assuming the function **`greet`** is already defined, write the command to call (execute) the **`greet`** function.",
        "answer": "greet()",
        "hint": "The function name is followed by parentheses, with no quotes or keywords.",
        "type": "exact_match"
    },
    {
        "concept": "Functions: Using Arguments (Parameters) 🎁",
        "instruction": "Function arguments (also called parameters) are variables listed inside the parentheses during definition. They allow data to be passed into the function when it is called.",
        "example": '`def say_name(name):`\n`    print("Hello, " + name)`',
        "challenge": "Challenge: Define a function named **`show_level`** that accepts one argument named **`level`**. The function body should print the argument, `level`.",
        "answer": "def show_level(level):\n    print(level)",
        "hint": "The argument name goes inside the parentheses of the `def` line. The print statement uses the argument name.",
        "type": "function_define_with_arg"
    },
    {
        "concept": "Functions: Returning a Value (`return`) ↩️",
        "instruction": "The `return` keyword exits a function and sends a specified value back to the code that called it. Define a function named **`get_number`** that simply returns the integer value **10**.",
        "example": '`def get_five():`\n`    return 5`',
        "challenge": "Challenge: Write a complete function definition for a function named **`get_number`**. The body of the function should be a single line that returns the integer **10**.",
        "answer": "def get_number():\n    return 10",
        "hint": "The `def` line needs a colon. The `return` statement needs 4 spaces of indentation.",
        "type": "function_define_return"
    },
    {
        "concept": "Functions: Using Returned Values ❓",
        "instruction": "To store the value a function returns, assign the function call to a variable. Call the function **`get_number`** (defined in the last lesson) and store its result in a new variable named **`result`**.",
        "example": '`five = get_five()`\n# five is now 5',
        "challenge": "Challenge: Write the command to call the **`get_number`** function and assign the returned value to a variable named **`result`**.",
        "answer": "result = get_number()",
        "hint": "The variable name is followed by the assignment operator, then the function name with parentheses.",
        "type": "exact_match"
    },
    {
        "concept": "Built-in Modules: Random Numbers (`import random`) 🎲",
        "instruction": "To use external functions, you must first import the module. Use the **`import`** keyword to load the **`random`** module. Then, call the **`randint()`** function on the module to get a random integer between two specified numbers (inclusive).",
        "example": '`import random`\n`num = random.randint(1, 6)`',
        "challenge": "Challenge: Write two commands: First, **`import`** the **`random`** module. Second, create a variable named **`rand_val`** and assign it a random integer between **1** and **100** (inclusive).",
        "answer": "import random\nrand_val = random.randint(1, 100)",
        "hint": "The second line uses dot notation: `module.function(min, max)`.",
        "type": "random_import"
    },
    {
        "concept": "Iteration: `for` Loop over a List 💡",
        "instruction": "You can use a `for` loop to iterate directly over the *items* of a list, not just a range of numbers. The loop variable (e.g., `item`) takes the value of each element sequentially.",
        "example": '`items = ["A", "B"]`\n`for item in items:`\n`    print(item)`\n# Output: A, B',
        "challenge": "Challenge: Assuming a list **`names`** exists, write a `for` loop that iterates over each element in **`names`** and prints the value of the element (use **`name`** as the loop variable).",
        "answer": "for name in names:\n    print(name)",
        "hint": "The structure is `for variable in list_name:` followed by an indented action.",
        "type": "for_loop_list_iterate"
    },
    {
        "concept": "Functions: Multiple Arguments (Comma Separated) ✨",
        "instruction": "Functions can accept any number of arguments, separated by commas during definition and when called. Define a function named **`add`** that takes two arguments, **`a`** and **`b`**, and returns their sum.",
        "example": '`def product(x, y):`\n`    return x * y`',
        "challenge": "Challenge: Define a function named **`add`** that accepts two arguments, **`a`** and **`b`**. The function body should contain a single line that returns the result of **`a + b`**.",
        "answer": "def add(a, b):\n    return a + b",
        "hint": "The arguments in the `def` line must be comma-separated, and the return line must be indented.",
        "type": "function_two_args"
    },
    {
        "concept": "Functions: Calling with Keyword Arguments (Named) 🏷️",
        "instruction": "When calling a function, you can optionally specify which parameter a value is assigned to using its name (`param=value`). This is useful for clarity and allows you to pass arguments out of order.",
        "example": '`def power(base, exp):`\n`    return base ** exp`\n`result = power(exp=3, base=2)`\n# result is 8 (2**3)',
        "challenge": "Challenge: Assuming the function **`add`** is defined, call it, passing the value **10** to the **`a`** argument and the value **20** to the **`b`** argument using keyword arguments. Store the returned sum in a variable named **`final_sum`**.",
        "answer": "final_sum = add(a=10, b=20)",
        "hint": "The arguments inside the parentheses must be named with an equals sign.",
        "type": "exact_match"
    },
    {
        "concept": "List Comprehension: Simple Mapping 🚀",
        "instruction": "List comprehension provides a concise way to create lists. Instead of a `for` loop, you define the operation and the loop inside square brackets (`[]`). Example: `[x * 2 for x in [1, 2, 3]]` creates `[2, 4, 6]`.",
        "example": '`numbers = [1, 2, 3]`\n`squared = [n ** 2 for n in numbers]`\n# squared is [1, 4, 9]',
        "challenge": "Challenge: Create a list named **`doubled`** using list comprehension. Iterate over an existing list **`data_points`** and double the value of each element.",
        "answer": "doubled = [x * 2 for x in data_points]",
        "hint": "The format is `new_list = [operation for variable in iterable]`.",
        "type": "list_comprehension_1"
    },
    {
        "concept": "List Comprehension: Conditional Filtering 🧪",
        "instruction": "You can add an `if` condition to the comprehension to filter values. The condition goes after the `for` loop. Example: `[x for x in numbers if x > 5]` includes only numbers greater than 5.",
        "example": '`scores = [80, 65, 90]`\n`passed = [s for s in scores if s >= 70]`\n# passed is [80, 90]',
        "challenge": "Challenge: Create a list named **`filtered`** using list comprehension. Iterate over the list **`data_points`** and only include elements that are **greater than 10**.",
        "answer": "filtered = [x for x in data_points if x > 10]",
        "hint": "The condition (`if x > 10`) comes after the `for` part.",
        "type": "list_comprehension_2"
    },
    {
        "concept": "Data Structures: Tuples (Creation and Immutability) 🧊",
        "instruction": "A Tuple is an ordered collection of items, just like a list, but it is **immutable** (cannot be changed after creation). Tuples use parentheses `()`.",
        "example": '`coordinates = (10, 20)`\n`point = ("x", 5)`',
        "challenge": "Challenge: Create a tuple named **`user_data`** and assign it the values **101** (integer), **'Alice'** (string), and **True** (boolean).",
        "answer": "user_data = (101, 'Alice', True)",
        "hint": "Use parentheses `()` and ensure the string value is in quotes.",
        "type": "tuple_creation"
    },
    {
        "concept": "Tuples: Accessing Elements by Index 🔎",
        "instruction": "Just like lists, items in a tuple are accessed using their **index number** inside square brackets (`[]`). The first item is at index 0.",
        "example": '`point = ("x", 5)`\n`print(point[0])`\n# Output: x',
        "challenge": "Challenge: Assuming the tuple **`user_data`** is **`(101, 'Alice', True)`**, write the command to print the item at **index 1**.",
        "answer": "print(user_data[1])",
        "hint": "Use the `print()` function with the tuple variable name followed by the index in square brackets (`[]`).",
        "type": "tuple_access"
    },
    {
        "concept": "Membership: The `in` Keyword (Lists) ❓",
        "instruction": "The **`in`** keyword is used to test if a specific item is present in a list (or any sequence). It returns a Boolean value (`True` or `False`).",
        "example": '`numbers = [1, 2, 3]`\n`is_present = 2 in numbers`\n# is_present is True',
        "challenge": "Challenge: Assuming a list **`fruits`** exists, check if the string **'banana'** is present in the list. Store the result in a variable named **`found_fruit`**.",
        "answer": "found_fruit = 'banana' in fruits",
        "hint": "The value being searched for comes before the `in` keyword.",
        "type": "membership_in"
    },
    {
        "concept": "Membership: The `not in` Keyword (Dictionaries) ⛔",
        "instruction": "The **`not in`** keyword checks if an item is *not* present. When checking dictionaries, `in` and `not in` test against the **keys** by default.",
        "example": '`user = {"name": "Alex"}`\n`is_missing = "age" not in user`\n# is_missing is True',
        "challenge": "Challenge: Assuming a dictionary **`settings`** exists, check if the key **'theme'** is **not** present in the dictionary. Store the result in a variable named **`theme_missing`**.",
        "answer": "theme_missing = 'theme' not in settings",
        "hint": "Use the keyword combination `not in` to test for absence.",
        "type": "membership_not_in"
    },
    { 
        "concept": "Iteration: Looping over Dictionary Items (`.items()`) 🔄🔑",
        "instruction": "The **`.items()`** method lets you iterate over both the **key** and the **value** in a dictionary simultaneously, which is crucial for structuring data.",
        "example": '`data = {"a": 1, "b": 2}`\n`for key, value in data.items():`\n`    print(f"{key}: {value}")`\n# Output: a: 1, b: 2',
        "challenge": "Challenge: Assuming a dictionary **`scores`** exists, write a `for` loop that iterates over its items. Use **`subject`** for the key and **`score`** for the value. Inside the loop, print the `subject`.",
        "answer": "for subject, score in scores.items():\n    print(subject)",
        "hint": "The `for` line must use two variables, the `in` keyword, the dictionary name, and `.items()`, followed by a colon.",
        "type": "for_loop_dict_items"
    },
    { 
        "concept": "Built-in Functions: `enumerate()` for Indexing 🧭",
        "instruction": "The **`enumerate()`** function is used with `for` loops over sequences (like lists). It returns both the **index** and the **value** for each item, which is helpful for creating a Pandas Index.",
        "example": '`colors = ["R", "G"]`\n`for index, color in enumerate(colors):`\n`    print(f"{index}: {color}")`\n# Output: 0: R, 1: G',
        "challenge": "Challenge: Assuming a list **`countries`** exists, write a `for` loop that uses `enumerate()`. Use **`i`** for the index and **`country`** for the value. Inside the loop, print the `country`.",
        "answer": "for i, country in enumerate(countries):\n    print(country)",
        "hint": "The syntax is `for index_var, value_var in enumerate(list_name):`.",
        "type": "enumerate_loop"
    },
    { 
        "concept": "Data Structures: Sets (Creation and Uniqueness) 🧩",
        "instruction": "A **Set** is an unordered collection of **unique** items. They are defined using curly braces (`{}`) or the `set()` function. Duplicate entries are automatically discarded, which is useful for cleaning data.",
        "example": '`unique = {1, 2, 2, 3}`\n# unique is {1, 2, 3}',
        "challenge": "Challenge: Create a set named **`unique_ids`** and assign it the integer values **1**, **5**, **5**, and **10** using curly braces.",
        "answer": "unique_ids = {1, 5, 10}",
        "hint": "Use curly braces `{}` and only list the unique values you want to be included.",
        "type": "set_creation"
    },
    { 
        "concept": "Set Operations: Union (`|`) 🤝",
        "instruction": "The **Union** operation combines all unique elements from two or more sets. It is performed using the pipe character (`|`) operator or the `.union()` method.",
        "example": '`A = {1, 2}`\n`B = {2, 3}`\n`C = A | B`\n# C is {1, 2, 3}`',
        "challenge": "Challenge: Assume sets **`set1`** and **`set2`** exist. Create a new set named **`combined_set`** using the **`|`** operator to get the union of `set1` and `set2`.",
        "answer": "combined_set = set1 | set2",
        "hint": "The result is assigned to the new variable, using the pipe operator between the two sets.",
        "type": "set_union"
    },
    { 
        "concept": "Set Operations: Intersection (`&`) 🎯",
        "instruction": "The **Intersection** operation returns only the elements that are common to both sets. It is performed using the ampersand character (`&`) operator or the `.intersection()` method.",
        "example": '`A = {1, 2}`\n`B = {2, 3}`\n`C = A & B`\n# C is {2}`',
        "challenge": "Challenge: Assume sets **`set1`** and **`set2`** exist. Create a new set named **`common_set`** using the **`&`** operator to get the intersection of `set1` and `set2`.",
        "answer": "common_set = set1 & set2",
        "hint": "Use the ampersand operator (`&`) between the two sets.",
        "type": "set_intersection"
    },
    { 
        "concept": "Error Handling: The `try...except` Block 🛡️",
        "instruction": "Use a **`try`** block to execute code that might cause an error, and an **`except`** block to handle the error gracefully if it occurs. Both require a colon (`:`).",
        "example": '`try:`\n`    result = 10 / 0  # This raises an error`\n`except:`\n`    print("Cannot divide by zero.")`',
        "challenge": "Challenge: Write a complete `try...except` block. In the `try` block, print the string **'Attempting code...'**. In the `except` block, print the string **'An error occurred.'**",
        "answer": "try:\n    print('Attempting code...')\nexcept:\n    print('An error occurred.')",
        "hint": "Remember the colon on both `try:` and `except:`, and ensure the print statements are indented.",
        "type": "try_except_block"
    },
    { # L52 (Index 51)
        "concept": "Pandas: Importing the Library 🐼",
        "instruction": "The **Pandas** library is the foundation of data analysis in Python. It is almost universally imported using the alias **`pd`** for brevity. This is the first step in any data project.",
        "example": '`import numpy as np`',
        "challenge": "Challenge: Write the single line of code to import the **`pandas`** library using the standard alias **`pd`**.",
        "answer": "import pandas as pd",
        "hint": "Use `import`, the library name, `as`, and the alias `pd`.",
        "type": "exact_match"
    },
    { # L53 (Index 52)
        "concept": "Pandas Series: Creation from a List 📈",
        "instruction": "A Pandas **Series** is a one-dimensional labeled array (like a column in a spreadsheet). You create one by calling the **`pd.Series()`** constructor and passing it a standard Python list.",
        "example": '`data = [10, 20, 30]`\n`s = pd.Series(data)`',
        "challenge": "Challenge: Assume a list named **`temperatures`** exists. Create a Pandas Series named **`temp_series`** by passing the `temperatures` list to the **`pd.Series()`** constructor.",
        "answer": "temp_series = pd.Series(temperatures)",
        "hint": "Remember to use the alias `pd` and ensure the argument is correctly passed in parentheses.",
        "type": "exact_match"
    },
    { # L54 (Index 53)
        "concept": "Pandas DataFrame: Creation from a Dictionary 📊",
        "instruction": "A **DataFrame** is a two-dimensional labeled data structure (like a whole spreadsheet or SQL table). It is usually created by passing a **dictionary** of lists (where keys become column names and values become the column data) to the **`pd.DataFrame()`** constructor.",
        "example": '`data = {"A": [1, 2], "B": [3, 4]}`\n`df = pd.DataFrame(data)`',
        "challenge": "Challenge: Assume a dictionary named **`data_dict`** exists. Create a Pandas DataFrame named **`user_df`** by passing the `data_dict` to the **`pd.DataFrame()`** constructor.",
        "answer": "user_df = pd.DataFrame(data_dict)",
        "hint": "Use the assignment operator (`=`) and the constructor with the alias: `pd.DataFrame()`.",
        "type": "exact_match"
    },
    { # L55 (Index 54)
        "concept": "DataFrame: Checking Column Names (`.columns`) 🏷️",
        "instruction": "The **`.columns`** attribute is used to retrieve an index containing the names of all columns in a Pandas DataFrame. It is read-only and does not require parentheses.",
        "example": '`df.columns`\n# Output: Index([\'Name\', \'Age\'])',
        "challenge": "Challenge: Assuming a DataFrame named **`user_df`** exists, assign its column names (using the `.columns` attribute) to a new variable named **`col_names`**.",
        "answer": "col_names = user_df.columns",
        "hint": "The attribute is called directly on the DataFrame variable, with no parentheses.",
        "type": "exact_match"
    },
    { # L56 (Index 55)
        "concept": "DataFrame: Checking Data Shape (`.shape`) 📐",
        "instruction": "The **`.shape`** attribute returns a **tuple** representing the dimensionality of the DataFrame: `(number_of_rows, number_of_columns)`. It is read-only and does not require parentheses.",
        "example": '`df.shape`\n# Output: (100, 5) # 100 rows, 5 columns',
        "challenge": "Challenge: Assuming a DataFrame named **`user_df`** exists, assign its shape (a tuple of rows and columns) to a new variable named **`df_shape`**.",
        "answer": "df_shape = user_df.shape",
        "hint": "The attribute is called directly on the DataFrame variable, with no parentheses.",
        "type": "exact_match"
    },
    { # L57 (Index 56)
        "concept": "DataFrame: Viewing the First Rows (`.head()`) 👓",
        "instruction": "The **`.head()`** method displays the first 5 rows of the DataFrame by default. This is essential for quickly inspecting the data structure and content after loading.",
        "example": '`df.head()`\n# Displays the first 5 rows',
        "challenge": "Challenge: Assuming a DataFrame named **`user_df`** exists, write the command to print the **first 5 rows** of the DataFrame using the `.head()` method.",
        "answer": "print(user_df.head())",
        "hint": "The method requires parentheses (`()`) and should be wrapped in a `print()` function to display the output.",
        "type": "exact_match_print"
    }
    # --- END LESSONS (57 Total) ---
]

# --- 2. Game State Management & Callbacks (No Change) ---

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

    # --- LOGIC FOR NEW LESSONS 55-57 ---
    
    # LESSON 57 (Index 56): .head() with print
    if match_type == "exact_match_print" and current_lesson["concept"].startswith("DataFrame: Viewing"):
        # Check for print(user_df.head())
        pattern = re.compile(
            r"^print\s*\(\s*user_df\s*\.\s*head\s*\(\s*\)\s*\)$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip()))
    
    # LESSON 56 (Index 55): .shape attribute
    elif match_type == "exact_match" and current_lesson["concept"].startswith("DataFrame: Checking Data Shape"):
        # Check for df_shape = user_df.shape
        pattern = re.compile(
            r"^df_shape\s*=\s*user_df\s*\.\s*shape$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip()))

    # LESSON 55 (Index 54): .columns attribute
    elif match_type == "exact_match" and current_lesson["concept"].startswith("DataFrame: Checking Column Names"):
        # Check for col_names = user_df.columns
        pattern = re.compile(
            r"^col_names\s*=\s*user_df\s*\.\s*columns$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip()))

    # LESSON 54 (Index 53): pd.DataFrame creation
    elif match_type == "exact_match" and current_lesson["concept"].startswith("Pandas DataFrame:"):
        # Check for user_df = pd.DataFrame(data_dict)
        pattern = re.compile(
            r"^user_df\s*=\s*pd\.DataFrame\s*\(\s*data_dict\s*\)$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip()))
    
    # LESSON 53 (Index 52): pd.Series creation
    elif match_type == "exact_match" and current_lesson["concept"].startswith("Pandas Series:"):
        # Check for temp_series = pd.Series(temperatures)
        pattern = re.compile(
            r"^temp_series\s*=\s*pd\.Series\s*\(\s*temperatures\s*\)$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip()))
    
    # LESSON 52 (Index 51): import pandas as pd
    elif match_type == "exact_match" and current_lesson["concept"].startswith("Pandas: Importing"):
        # Check for import pandas as pd
        pattern = re.compile(
            r"^import\s+pandas\s+as\s+pd$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip()))


    # LESSON 51 (Index 50): try_except_block
    elif match_type == "try_except_block":
        # Check for try:\n    print('Attempting code...')\nexcept:\n    print('An error occurred.')
        required_pattern = re.compile(
            r"^try\s*:\s*\n\s*print\s*\(\s*['\"]Attempting\s*code\s*...\s*['\"]\s*\)\s*\nexcept\s*:\s*\n\s*print\s*\(\s*['\"]An\s*error\s*occurred\s*\.\s*['\"]\s*\)$", 
            re.IGNORECASE 
        )
        is_correct = bool(required_pattern.match(user_code_normalized.strip()))
        
    # LESSON 50 (Index 49): set_intersection
    elif match_type == "set_intersection":
        # Check for common_set = set1 & set2
        pattern = re.compile(
            r"^common_set\s*=\s*set1\s*&\s*set2$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip().replace(' ', '')))
        
    # LESSON 49 (Index 48): set_union
    elif match_type == "set_union":
        # Check for combined_set = set1 | set2
        pattern = re.compile(
            r"^combined_set\s*=\s*set1\s*\|\s*set2$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip().replace(' ', '')))

    # LESSON 48 (Index 47): set_creation
    elif match_type == "set_creation":
        # Check for unique_ids = {1, 5, 10} - flexible on spacing
        pattern = re.compile(
            r"^unique_ids\s*=\s*\{\s*1\s*,\s*5\s*,\s*10\s*\}$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip().replace(' ', '')))
        
    # LESSON 47 (Index 46): enumerate_loop
    elif match_type == "enumerate_loop":
        # Check for for i, country in enumerate(countries):\n    print(country)
        required_pattern = re.compile(
            r"^for\s+i\s*,\s*country\s+in\s+enumerate\s*\(\s*countries\s*\)\s*:\s*\n\s*print\s*\(\s*country\s*\)$", 
            re.IGNORECASE 
        )
        is_correct = bool(required_pattern.match(user_code_normalized.strip()))

    # LESSON 46 (Index 45): for_loop_dict_items
    elif match_type == "for_loop_dict_items":
        # Check for for subject, score in scores.items():\n    print(subject)
        required_pattern = re.compile(
            r"^for\s+subject\s*,\s*score\s+in\s+scores\.items\s*\(\s*\)\s*:\s*\n\s*print\s*\(\s*subject\s*\)$", 
            re.IGNORECASE 
        )
        is_correct = bool(required_pattern.match(user_code_normalized.strip()))
        
    # LESSON 45: membership_not_in
    elif match_type == "membership_not_in":
        # Check for theme_missing = 'theme' not in settings
        pattern = re.compile(
            r"^theme_missing\s*=\s*['\"]theme['\"]\s+not\s+in\s+settings$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip().replace('"', "'")))
        
    # LESSON 44: membership_in
    elif match_type == "membership_in":
        # Check for found_fruit = 'banana' in fruits
        pattern = re.compile(
            r"^found_fruit\s*=\s*['\"]banana['\"]\s+in\s+fruits$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip().replace('"', "'")))
        
    # LESSON 43: tuple_access
    elif match_type == "tuple_access":
        # Check for print(user_data[1])
        pattern = re.compile(
            r"^print\s*\(\s*user_data\s*\[\s*1\s*\]\s*\)$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip()))
        
    # LESSON 42: tuple_creation (Robust check)
    elif match_type == "tuple_creation":
        # Check for user_data = (101, 'Alice', True)
        pattern = re.compile(
            r"^user_data\s*=\s*\(\s*101\s*,\s*['\"]Alice['\"]\s*,\s*True\s*\)$", 
            re.IGNORECASE 
        )
        # Check a version that allows for variable spacing and quotes
        is_correct = bool(pattern.match(user_code.strip().replace('"', "'").replace(' ', '')))
        
    # LESSON 41: list_comprehension_2
    elif match_type == "list_comprehension_2":
        # Check for filtered = [x for x in data_points if x > 10]
        pattern = re.compile(
            r"^filtered\s*=\s*\[\s*x\s+for\s+x\s+in\s+data_points\s+if\s+x\s*>\s*10\s*\]$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip()))
        
    # LESSON 40: list_comprehension_1
    elif match_type == "list_comprehension_1":
        # Check for doubled = [x * 2 for x in data_points]
        pattern = re.compile(
            r"^doubled\s*=\s*\[\s*x\s*\*\s*2\s+for\s+x\s+in\s+data_points\s*\]$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code.strip()))

    # LESSON 38: function_two_args
    elif match_type == "function_two_args":
        # Check for def add(a, b):\n    return a + b
        required_pattern = re.compile(
            r"^def\s+add\s*\(\s*a\s*,\s*b\s*\)\s*:\s*\n\s*return\s+a\s*\+\s*b$", 
            re.IGNORECASE 
        )
        is_correct = bool(required_pattern.match(user_code_normalized.strip()))
        
    # LESSON 37: for_loop_list_iterate
    elif match_type == "for_loop_list_iterate":
        # Check for for name in names:\n    print(name)
        required_pattern = re.compile(
            r"^for\s+name\s+in\s+names\s*:\s*\n\s*print\s*\(\s*name\s*\)$", 
            re.IGNORECASE 
        )
        is_correct = bool(required_pattern.match(user_code_normalized.strip()))


    # --- EXISTING LOGIC (Default Fallback) ---
                
    else:
        # Exact Match Logic (Covers all other types: exact_match, quote_flexible, list_creation, etc.)
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
        if match_type in ["if_statement", "if_else_statement", "if_elif_statement", "if_elif_else_statement", "while_loop", "for_loop", "function_define", "function_define_with_arg", "function_define_return", "random_import", "for_loop_list_iterate", "function_two_args", "for_loop_dict_items", "enumerate_loop", "try_except_block"]:
             st.error(
                f"❌ **RETRY.** Attempt **{st.session_state.attempts}**. "
                "Double-check your **COLONS** (`:`) and ensure lines are indented by 4 spaces (or a tab) *only* when they belong to a block (`if`, `elif`, `else`, `while`, `for`, `def`, `try`, or `except`). Also check spacing, parentheses, and keywords for new lessons."
            )
        # Provide a specific warning for list comprehensions
        elif match_type in ["list_comprehension_1", "list_comprehension_2"]:
             st.error(
                f"❌ **RETRY.** Attempt **{st.session_state.attempts}**. "
                "List comprehensions are tricky! Ensure your syntax is `[operation for variable in list if condition]` and check your variable names."
            )
        # Provide a specific warning for membership/set operators
        elif match_type in ["membership_in", "membership_not_in", "set_creation", "set_union", "set_intersection"]:
             st.error(
                f"❌ **RETRY.** Attempt **{st.session_state.attempts}**. "
                "Check your operators (`|`, `&`), brackets (`{}`), quotes, and whether you included only the unique values/correct keywords."
            )
        # Provide a specific warning for Pandas dot-notation
        elif current_lesson["concept"].startswith("Pandas") or current_lesson["concept"].startswith("DataFrame:"):
            st.error(
                f"❌ **RETRY.** Attempt **{st.session_state.attempts}**. "
                "Check your **dot notation** (`df.attribute` or `df.method()`) and ensure you are correctly using a variable assignment (`=`) for attributes, or a `print()` for methods like `.head()`."
            )
        else:
            st.toast("🚨 Try Again! Your syntax didn't match the required command.", icon="❌")


# --- 4. Display Functions (No Change) ---

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
        
        # Determine if it's a loop or function structure needing a block-style placeholder
        block_lessons = {
            14: "if is_rainy == True:\n    ", 
            15: "if is_sunny == True:\n    \nelse:\n    ", 
            16: "if grade > 90:\n    \nelif grade > 80:\n    ", 
            17: "if day == 'Sat':\n    \nelif day == 'Sun':\n    \nelse:\n    ",
            18: "x = 0\nwhile x < 2:\n    \n    ",
            19: "for i in range(3):\n    ",
            30: "def greet():\n    ",
            32: "def show_level(level):\n    ",
            33: "def get_number():\n    ",
            35: "import random\n",
            36: "for name in names:\n    ",
            37: "def add(a, b):\n    ",
            45: "for subject, score in scores.items():\n    ", 
            46: "for i, country in enumerate(countries):\n    ",
            50: "try:\n    \nexcept:\n    " ,
            # Pandas lessons
            51: "import pandas as pd\n",
        }
        
        # Check if the current lesson is a special multi-line structure
        if st.session_state.q_index in block_lessons:
            prefill_value = block_lessons[st.session_state.q_index]
        # For single-line Pandas lessons, check if they need a leading placeholder
        elif st.session_state.q_index >= 52:
            pass # Keep prefill_value as "" unless passed

    # Determine height based on whether it's a block structure
    height_lessons_250 = [17, 18, 50] # Full if/elif/else, while loop, try/except
    height_lessons_200 = [14, 15, 16, 30, 32, 33, 36, 37, 45, 46, 51] # Other conditional/loops/functions, import
    
    if st.session_state.q_index in height_lessons_250:
        height = 250
    elif st.session_state.q_index in height_lessons_200:
        height = 200
    else:
        height = 100

    user_code = st.text_area(
        "Type your Python command(s) below and click 'Submit'. Be precise with indentation!",
        height=height,
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
            
            # Use EMOJI icons for clear status indication
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
