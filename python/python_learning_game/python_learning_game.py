import streamlit as st
import random
import re

# --- 1. Question/Lesson Data (The Content) ---
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
    # --- LESSON 13 ---
    {
        "concept": "Comparison Operators: Greater Than/Less Than (<, >) ⬆️⬇️",
        "instruction": "The **Greater Than** (`>`) and **Less Than** (`<`) operators are used to check the size relationship between two numbers. They form the basis of most conditional checks in programming.",
        "example": '`is_small = 5 < 10`\n# Output: True\n`is_large = 20 > 50`\n# Output: False',
        "challenge": "Challenge: Create a variable named **`is_valid_score`** and assign it the result of checking if the number **75** is greater than the number **50**.",
        "answer": "is_valid_score = 75 > 50",
        "hint": "Use the correct operator to compare the two numbers. The resulting Boolean should reflect the truth of the statement.",
        "type": "exact_match"
    }
    # --- END LESSON 13 ---
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

def check_code_submission(user_code: str):
    """Checks the submitted code."""
    st.session_state.attempts += 1
    
    current_lesson = LESSONS_DATA[st.session_state.q_index]
    required_answer = current_lesson["answer"].strip()
    user_code_stripped = user_code.strip()
    
    is_correct = False
    match_type = current_lesson.get("type")

    if match_type == "concatenation_flexible":
        pattern = re.compile(
            r"^full_city\s*=\s*city\s*\+\s*['\"] Bridge['\"]\s*$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code_stripped))
        
    elif match_type == "quote_flexible":
        # Check for Lesson 11 (index 10) comparison: result_match = 'Python' == 'python'
        if st.session_state.q_index == 10:
            p = re.compile(
                r"^result_match\s*=\s*['\"]Python['\"]\s*==\s*['\"]python['\"]\s*$", 
                re.IGNORECASE 
            )
            is_correct = bool(p.match(user_code_stripped))
        
        # Check for Lesson 2 (index 1) assignment: city = 'London'
        elif st.session_state.q_index == 1: 
             var_name, var_value_quoted = required_answer.split('=', 1)
             var_value = var_value_quoted.strip().strip("'\"") 
             var_name = var_name.strip()
             pattern = re.compile(
                rf"^{re.escape(var_name)}\s*=\s*['\"]{re.escape(var_value)}['\"]$", 
                re.IGNORECASE 
             )
             is_correct = bool(pattern.match(user_code_stripped))
        else:
             is_correct = (user_code_stripped == required_answer)
                
    else:
        # Exact Match Logic (L12 and L13 fall here)
        is_correct = (user_code_stripped == required_answer)

    if is_correct:
        current_index = st.session_state.q_index
        
        if current_index not in st.session_state.passed_indices:
            st.session_state.passed_lessons += 1
            st.session_state.passed_indices.add(current_index)
        
        st.session_state.correct = True 
        st.balloons() 
        
    else:
        st.session_state.correct = False
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
    
    st.markdown(f"### 📝 Your Challenge")
    st.warning(lesson_data['challenge'])
    
    is_permanently_passed = st.session_state.q_index in st.session_state.passed_indices
    
    # 2. User Input Area (Code Editor)
    input_key = f"code_input_{st.session_state.q_index}" 
    user_code = st.text_area(
        "Type your Python command below and click 'Submit' (Case and syntax matter for non-string parts!)",
        height=100,
        key=input_key,
        value=lesson_data["answer"] if is_permanently_passed else ""
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
        st.error(
            f"❌ **RETRY.** Attempt **{st.session_state.attempts}**. "
            "Please check your capitalization, quotes, and spacing, and type the command again."
        )
        if st.session_state.attempts >= 2:
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
