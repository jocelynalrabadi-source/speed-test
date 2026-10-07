import streamlit as st
import random
import time


class Question:
    def __init__(self, text, option, answer):
        self.text = text
        self.option = option
        self.answer = answer


class player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def addition(self):
        self.score += 1


class qgame:
    def __init__(self, questions):
        self.questions = questions
        self.current_question_idx = 0

    def get_current_question(self):
        if self.current_question_idx < len(self.questions):
            return self.questions[self.current_question_idx]
        return None

    def next_question(self):
        self.current_question_idx += 1


questions = [
    Question("What does len() do?", ["Adds numbers", "Counts items", "Prints text", "Stops program"], "Counts items"),
    Question("Which data type uses square brackets []?", ["Tuple", "String", "List", "Set"], "List"),
    Question("What keyword is used to define a function?", ["func", "define", "def", "function"], "def"),
    Question("Which symbol is used for comments in Python?", ["//", "#", "/*", "--"], "#"),
    Question("What is the output type of input()?", ["int", "string", "float", "boolean"], "string"),
    Question("Which keyword is used for loops?", ["repeat", "loop", "for", "iterate"], "for"),
    Question("What does print() do?", ["Takes input", "Displays output", "Stores data", "Loops code"], "Displays output"),
    Question("Which data type is immutable?", ["List", "Dictionary", "Tuple", "Set"], "Tuple"),
    Question("What symbol is used for assignment?", ["=", "==", "!=", ":"], "="),
    Question("Which operator means 'equal to'?", ["=", "==", "!=", "<>"], "=="),
    Question("What does int() do?", ["Converts to integer", "Converts to string", "Prints value", "Stops program"], "Converts to integer"),
    Question("Which keyword is used for conditions?", ["if", "loop", "check", "when"], "if"),
    Question("What is a list?", ["Single value", "Collection of items", "Loop", "Function"], "Collection of items"),
    Question("Which function gives the type of a variable?", ["type()", "kind()", "var()", "check()"], "type()"),
    Question("Which keyword is used to exit a loop?", ["exit", "stop", "break", "end"], "break"),
    Question("What does range() do?", ["Stores values", "Generates sequence", "Prints output", "Takes input"], "Generates sequence"),
    Question("Which data type uses {}?", ["List", "Tuple", "Dictionary", "String"], "Dictionary"),
    Question("What is True or False called?", ["String", "Boolean", "Integer", "List"], "Boolean"),
    Question("Which keyword is used to handle errors?", ["try", "check", "error", "handle"], "try"),
    Question("What does append() do?", ["Removes item", "Adds item", "Sorts list", "Prints list"], "Adds item"),
]


def get_rank(score, total):
    percent = (score / total) * 100
    if percent >= 90:
        return "Excellent"
    elif percent >= 75:
        return "Very Good"
    elif percent >= 50:
        return "Good"
    else:
        return "Needs Improvement"


st.set_page_config(page_title="Speed game")

st.title("Speed Quiz Game")

# Session state
if "started" not in st.session_state:
    st.session_state.started = False
if "finished" not in st.session_state:
    st.session_state.finished = False
if "p" not in st.session_state:
    st.session_state.p = None
if "game" not in st.session_state:
    st.session_state.game = None
if "answers" not in st.session_state:
    st.session_state.answers = []
if "start_time" not in st.session_state:
    st.session_state.start_time = None

TIME_LIMIT = 35


# Start screen
if not st.session_state.started:
    name = st.text_input("Enter your name")

    if st.button("Start Quiz"):
        if name.strip() == "":
            st.warning("Please enter your name")
        else:
            random.shuffle(questions)
            selected = questions[:20]

            st.session_state.p = player(name)
            st.session_state.game = qgame(selected)
            st.session_state.answers = [None] * len(selected)
            st.session_state.start_time = time.time()
            st.session_state.started = True
            st.session_state.finished = False
            st.rerun()


else:
    game = st.session_state.game
    p = st.session_state.p

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = TIME_LIMIT - elapsed

    if remaining <= 0:
        st.session_state.finished = True

    if not st.session_state.finished:

        st.write(f"Player: {p.name}")
        st.write(f"Time left: {max(0, remaining)} seconds")
        st.progress(max(0, remaining) / TIME_LIMIT)

        q = game.get_current_question()

        if q:
            st.subheader(q.text)

            choice = st.radio(
                "Choose your answer:",
                [None] + q.option,
                format_func=lambda x: "Select answer" if x is None else x,
                key=f"q_{game.current_question_idx}"
            )

            if st.button("Next Question"):
                st.session_state.answers[game.current_question_idx] = choice
                game.next_question()

                if game.current_question_idx >= len(game.questions):
                    st.session_state.finished = True

                st.rerun()

    else:
        score = 0
        for i in range(len(game.questions)):
            if st.session_state.answers[i] == game.questions[i].answer:
                score += 1

        p.score = score

        st.success(f"Final Score: {p.score}/{len(game.questions)}")
        st.subheader(get_rank(p.score, len(game.questions)))

        st.write("Review:")

        for i in range(len(game.questions)):
            q = game.questions[i]
            user = st.session_state.answers[i]

            st.write(f"Question {i+1}: {q.text}")
            st.write(f"Your answer: {user if user else 'No answer'}")
            st.write(f"Correct answer: {q.answer}")

            if user == q.answer:
                st.success("Correct")
            else:
                st.error("Wrong")

            st.write("---")

        if st.button("Restart Quiz"):
            st.session_state.clear()
            st.rerun()