import streamlit as st
import random
import re  # Import the regular expression module

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
        "instruction": "The **`type()`** function is a built-in Python tool used to determine the data type of an object or variable. It takes the variable name inside its parentheses.", 
        "example": '`type(age)`\n# Output: <class \'int\'>',
        "challenge": "Challenge: Type the command to find the data type of the **`count`** variable you created in the last lesson.",
        "answer": "type(count)",
        "hint": "The command is the function name followed by the variable name in parentheses.",
        "type": "exact_match"
    },
    {
        "concept": "Arithmetic: Addition Operator (+) ➕",
        "instruction": "The plus sign (`+`) is used to add numbers or numerical variables together. The result can be assigned to a new variable.",
        "example": '`total = 10 + 5` or `new_age = age + 1`',
        "challenge": "Challenge: Assuming the variable `count` is 42 (from Lesson 3), create a new variable named **`sum`** and assign it the result of **`count` + 8**.",
        "answer": "sum = count + 8",
        "hint": "The answer should only contain the variable assignment. Remember, `count` is treated as the number 42.",
        "type": "exact_match"
    },
    {
        "concept": "Arithmetic: Subtraction (-) and Multiplication (*) ✖️",
        "instruction": "The minus sign (`-`) is used for subtraction, and the asterisk (`*`) is used for multiplication. Both follow standard mathematical rules for assigning results to variables.",
        "example": '`difference = 20 - 7`\n`area = 5 * 6`',
        "challenge": "Challenge: Calculate the total cost of 12 items at $5 each. Create a variable named **`cost`** and assign it the result of **12 * 5**.",
        "answer": "cost = 12 * 5",
        "hint": "The answer should only contain the variable assignment. Remember to use the asterisk (*) for multiplication.",
        "type": "exact_match"
    },
    {
        "concept": "String Concatenation (Joining Text) 🔗", # L7 RESTORED
        "instruction": "The plus sign (`+`) can be used to join two or more strings together (a process called concatenation). You must include a space yourself if you want one between the words.",
        "example": '`first_name = "Jane"`\n`full_name = first_name + " Doe"`\n# Output: "Jane Doe"',
        "challenge": "Challenge: Create a variable named **`full_city`** and assign it the result of joining the variables **`city`** (from Lesson 2) and the string **' Bridge'**.",
        "answer": "full_city = city + ' Bridge'", # The canonical answer
        "hint": "The variable `city` already contains the string value 'London', so the correct syntax is the variable name plus the operator plus the new string in quotes.",
        "type": "concatenation_flexible" # <-- NEW TYPE
    },
    {
        "concept": "Arithmetic: Division (/) and Floor Division (//) ➗", 
        "instruction": "Standard division (`/`) always produces a **float** (a number with a decimal). Floor division (`//`) discards the fractional part, resulting in an **integer**.",
        "example": '`result_float = 7 / 2`\n# Output: 3.5\n`result_int = 7 // 2`\n# Output: 3',
        "challenge": "Challenge: Calculate the floor division of 17 divided by 5 (the whole number result). Create a variable named **`whole_parts`** and assign it the result of **17 // 5**.",
        "answer": "whole_parts = 17 // 5",
        "hint": "Use the double-slash operator (`//`) to perform floor division.",
        "type": "exact_match"
    },
    {
        "concept": "Arithmetic: Modulus Operator (Remainder) %",
        "instruction": "The modulus operator (`%`) returns the **remainder** after performing a division. For example, 7 divided by 3 is 2 with a remainder of 1, so `7 % 3` equals 1.",
        "example": '`remainder_a = 10 % 3`\n# Output: 1\n`is_even = 8 % 2`\n# Output: 0',
        "challenge": "Challenge: Find the remainder when 20 is divided by 6. Create a variable named **`left_over`** and assign it the result of **20 % 6**.",
        "answer": "left_over = 20 % 6",
        "hint": "Divide 20 by 6 (6 goes into 20 three times). What number is left over?",
        "type": "exact_match"
    },
    {
        "concept": "Data Types: Boolean (True/False) 🚦", 
        "instruction": "A Boolean variable can only hold one of two values: **`True`** or **`False`**. Note that these must be capitalized and do not use quotes.",
        "example": '`is_active = True`\n`has_errors = False`',
        "challenge": "Challenge: Create a variable named **`is_valid`** and assign it the Boolean value **`True`**.",
        "answer": "is_valid = True",
        "hint": "Ensure the value is capitalized and has no quotes around it.",
        "type": "exact_match"
    }
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

# --- 3. Core Logic ---

def check_code_submission(user_code: str):
    """
    Checks the submitted code using either exact match, quote-flexible, or concatenation-flexible logic.
    """
    st.session_state.attempts += 1
    
    current_lesson = LESSONS_DATA[st.session_state.q_index]
    required_answer = current_lesson["answer"].strip()
    user_code_stripped = user_code.strip()
    
    is_correct = False
    
    match_type = current_lesson.get("type")

    if match_type == "concatenation_flexible":
        # Custom logic for Lesson 7: full_city = city + ' Bridge' (flexible quotes allowed)
        # Pattern looks for: full_city = city + (' Bridge' or " Bridge") with optional spaces
        pattern = re.compile(
            r"^full_city\s*=\s*city\s*\+\s*['\"] Bridge['\"]\s*$", 
            re.IGNORECASE 
        )
        is_correct = bool(pattern.match(user_code_stripped))
        
    elif match_type == "quote_flexible":
        # Logic for simple variable assignment (e.g., city = 'London')
        try:
            var_name, var_value_quoted = required_answer.split('=', 1)
            var_value = var_value_quoted.strip().strip("'\"") 
            var_name = var_name.strip()
            # Regex to accept var_name = 'value' or var_name = "value"
            pattern = re.compile(
                rf"^{re.escape(var_name)}\s*=\s*['\"]{re.escape(var_value)}['\"]$", 
                re.IGNORECASE 
            )
            is_correct = bool(pattern.match(user_code_stripped))
        except ValueError:
            is_correct = (user_code_stripped == required_answer)
            
    else:
        # Exact Match Logic (Used for numbers, print(), math, booleans)
        is_correct = (user_code_stripped == required_answer)

    if is_correct:
        st.session_state.passed_lessons += 1
        st.session_state.correct = True
        
        # Success actions
        st.balloons() 
        
    else:
        st.session_state.correct = False
        
        # Failure actions
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
    
    # 2. User Input Area (Code Editor)
    input_key = f"code_input_{st.session_state.q_index}" 
    user_code = st.text_area(
        "Type your Python command below and click 'Submit' (Case and syntax matter for non-string parts!)",
        height=100,
        key=input_key 
    )
    
    # 3. Submission Logic
    submit_disabled = st.session_state.get('correct', False)
    
    if not submit_disabled:
        st.button("Submit Code", 
                  on_click=check_code_submission, 
                  args=(user_code,), 
                  type="primary")
        
    st.markdown("---")
    
    # === DEDICATED FEEDBACK AREA ===
    current_lesson = LESSONS_DATA[st.session_state.q_index]

    if st.session_state.get('correct', False):
        # Display congratulations message
        st.success("🎉 **PASS! Congratulations!** Excellent syntax. Click 'Next Lesson' to continue.")
        st.button("Next Lesson >>", on_click=next_lesson)

    elif st.session_state.attempts > 0:
        # Display retry/error message
        st.error(
            f"❌ **RETRY.** Attempt **{st.session_state.attempts}**. "
            "Please check your capitalization, quotes, and spacing, and type the command again."
        )
        if st.session_state.attempts >= 2:
            with st.expander("💡 Show Hint"):
                st.info(current_lesson["hint"])


def display_completion_screen():
    """Renders the final score and completion message."""
    st.balloons()
    st.title("✅ Congratulations! All Lessons Complete!")
    
    total_lessons = len(LESSONS_DATA)
    st.markdown(f"## You completed **{st.session_state.passed_lessons}** out of **{total_lessons}** lessons.")
    
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
    passed = st.session_state.passed_lessons
    
    # --- SIDEBAR: Progress and Navigation ---
    with st.sidebar:
        st.title("Progress & Navigation")
        
        # 1. Overall Progress
        st.write(f"**Passed Lessons:** {passed} of {total_lessons}")
        st.progress(passed / total_lessons if total_lessons > 0 else 0)
        st.markdown("---")
        
        # 2. Lesson Navigation Buttons
        st.markdown("### Jump to Lesson:")
        for i, lesson in enumerate(LESSONS_DATA):
            # Check if the user is currently on this lesson or has passed it
            is_unlocked = i <= passed or (i == passed and current_lesson_num == passed)
            is_current = i == current_lesson_num
            
            # Determine the label and icon
            icon = "➡️" if is_current else ("✅" if i < passed else "🔒")
            label = f"L{i+1}: {lesson['concept']}"
            
            st.button(
                f"{icon} {label}", 
                key=f"nav_btn_{i}",
                on_click=set_lesson, 
                args=(i,),
                disabled=not is_unlocked,
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
