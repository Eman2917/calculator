import ast
import html
import math
import operator
import streamlit as st

st.set_page_config(
    page_title="Nova Scientific Calculator",
    page_icon="🧮",
    layout="centered"
)

# ---------- Attractive design ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

.stApp {
    background: linear-gradient(135deg, #101426, #211b46, #101426);
    color: #f8f9ff;
    font-family: Inter, sans-serif;
}
.block-container {
    max-width: 760px;
    padding-top: 2rem;
}
.hero {
    text-align: center;
    margin-bottom: 24px;
}
.hero h1 {
    color: #c4b5fd;
    font-size: 2.25rem;
    font-weight: 800;
}
.hero p { color: #b7bedc; }

.display {
    background: #1c2340;
    border: 1px solid #6155a8;
    border-radius: 20px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 8px 28px #080b1b80;
}
.expression {
    color: #cbd5e1;
    font-size: 1.15rem;
    overflow-wrap: anywhere;
    min-height: 30px;
}
.result {
    color: #6ee7b7;
    font-size: 2.1rem;
    font-weight: 800;
    overflow-wrap: anywhere;
    min-height: 45px;
}
div[data-testid="stTextInput"] input {
    background: #151a30;
    color: white;
    border: 1px solid #8173e6;
    border-radius: 12px;
    padding: 13px;
    font-size: 1.05rem;
}
div.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 12px;
    background: #282e4c;
    color: white;
    border: 1px solid #41496d;
    font-size: 1rem;
    font-weight: 600;
}
div.stButton > button:hover {
    background: #51438d;
    color: white;
    border-color: #b4a5ff;
}
.tip {
    text-align: center;
    color: #aab4d2;
    font-size: 0.85rem;
    margin-top: 18px;
}
</style>
""", unsafe_allow_html=True)


# ---------- Safe scientific calculator ----------
def calculate_expression(expression, angle_mode):
    expression = expression.strip()

    if not expression:
        raise ValueError("Please enter a calculation.")

    expression = (
        expression.replace("×", "*")
        .replace("÷", "/")
        .replace("−", "-")
        .replace("^", "**")
        .replace("π", "pi")
        .replace("√(", "sqrt(")
        .replace("²", "**2")
        .replace("³", "**3")
        .replace("%", "/100")
    )

    def trig(function):
        if angle_mode == "DEG":
            return lambda x: function(math.radians(x))
        return function

    def inverse_trig(function):
        if angle_mode == "DEG":
            return lambda x: math.degrees(function(x))
        return function

    functions = {
        "sin": trig(math.sin),
        "cos": trig(math.cos),
        "tan": trig(math.tan),
        "asin": inverse_trig(math.asin),
        "acos": inverse_trig(math.acos),
        "atan": inverse_trig(math.atan),
        "sqrt": math.sqrt,
        "log": math.log10,
        "ln": math.log,
        "abs": abs,
        "factorial": math.factorial,
        "exp": math.exp,
        "floor": math.floor,
        "ceil": math.ceil,
    }

    constants = {"pi": math.pi, "e": math.e}

    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
    }

    unary_operations = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value
            raise ValueError("Invalid number.")

        if isinstance(node, ast.Name):
            if node.id in constants:
                return constants[node.id]
            raise ValueError("Unknown name.")

        if isinstance(node, ast.BinOp):
            if type(node.op) not in operations:
                raise ValueError("Unsupported operator.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                raise ValueError("Power is too large.")

            return operations[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp):
            if type(node.op) not in unary_operations:
                raise ValueError("Invalid operator.")
            return unary_operations[type(node.op)](
                evaluate(node.operand)
            )

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Invalid function.")

            name = node.func.id
            if name not in functions or node.keywords:
                raise ValueError("Unsupported function.")

            args = [evaluate(arg) for arg in node.args]

            if name == "factorial":
                if (
                    len(args) != 1
                    or args[0] < 0
                    or int(args[0]) != args[0]
                    or args[0] > 170
                ):
                    raise ValueError(
                        "Factorial needs an integer from 0 to 170."
                    )

            return functions[name](*args)

        raise ValueError("Invalid expression.")

    try:
        tree = ast.parse(expression, mode="eval")
        result = evaluate(tree)

        if isinstance(result, complex):
            raise ValueError("Complex results are not supported.")

        if not math.isfinite(float(result)):
            raise ValueError("Result is outside the supported range.")

        return result

    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero.")
    except OverflowError:
        raise ValueError("Result is too large.")
    except (SyntaxError, TypeError, NameError):
        raise ValueError("Invalid expression. Check your input.")
    except ValueError as error:
        if str(error) in (
            "math domain error",
            "math range error",
        ):
            raise ValueError(
                "This function is not defined for that input."
            )
        raise


def format_result(value):
    if isinstance(value, float):
        if value.is_integer() and abs(value) < 1e15:
            return f"{int(value):,}"
        return f"{value:.12g}"
    return f"{value:,}" if isinstance(value, int) else str(value)


# ---------- Session state ----------
if "expression" not in st.session_state:
    st.session_state.expression = ""

if "result" not in st.session_state:
    st.session_state.result = ""

if "error" not in st.session_state:
    st.session_state.error = ""

if "angle" not in st.session_state:
    st.session_state.angle = "DEG"


def add_text(value):
    st.session_state.expression += value
    st.session_state.error = ""


def clear():
    st.session_state.expression = ""
    st.session_state.result = ""
    st.session_state.error = ""


def backspace():
    st.session_state.expression = st.session_state.expression[:-1]
    st.session_state.error = ""


def calculate():
    try:
        answer = calculate_expression(
            st.session_state.expression,
            st.session_state.angle
        )
        st.session_state.result = format_result(answer)
        st.session_state.error = ""
    except Exception as error:
        st.session_state.result = ""
        st.session_state.error = str(error)


def toggle_sign():
    expression = st.session_state.expression
    if expression:
        if expression.startswith("-(") and expression.endswith(")"):
            st.session_state.expression = expression[2:-1]
        else:
            st.session_state.expression = f"-({expression})"


# ---------- Header ----------
st.markdown("""
<div class="hero">
    <h1>✦ NOVA CALCULATOR</h1>
    <p>Your smart scientific calculator</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([2, 1])

with left:
    st.caption("⌨️ Type using your keyboard")

with right:
    st.session_state.angle = st.radio(
        "Angle mode",
        ["DEG", "RAD"],
        horizontal=True,
        label_visibility="collapsed",
        key="angle_choice",
        index=0 if st.session_state.angle == "DEG" else 1
    )

# ---------- Keyboard input ----------
st.text_input(
    "Type expression",
    key="expression",
    placeholder="Example: sin(30) + sqrt(25)",
    on_change=calculate,
    label_visibility="collapsed"
)

# ---------- Display ----------
safe_expression = html.escape(
    st.session_state.expression or "Your expression appears here"
)
safe_result = html.escape(
    st.session_state.result or "—"
)

st.markdown(f"""
<div class="display">
    <div style="color:#a5b4fc;font-size:.8rem;">
        EXPRESSION
    </div>
    <div class="expression">{safe_expression}</div>
    <div style="color:#a5b4fc;font-size:.8rem;margin-top:14px;">
        RESULT
    </div>
    <div class="result">{safe_result}</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.error:
    st.error(st.session_state.error)


# ---------- Scientific buttons ----------
scientific_rows = [
    [("sin", "sin("), ("cos", "cos("), ("tan", "tan("),
     ("√", "sqrt("), ("xʸ", "^")],
    [("asin", "asin("), ("acos", "acos("), ("atan", "atan("),
     ("log", "log("), ("ln", "ln(")],
    [("π", "π"), ("e", "e"), ("(", "("),
     (")", ")"), ("n!", "factorial(")],
]

for row_number, row in enumerate(scientific_rows):
    columns = st.columns(5, gap="small")
    for column, (label, value) in zip(columns, row):
        with column:
            st.button(
                label,
                key=f"scientific_{row_number}_{label}",
                on_click=add_text,
                args=(value,)
            )

st.markdown("---")


# ---------- Main keypad ----------
keypad = [
    [("AC", "clear"), ("⌫", "back"), ("%", "%"), ("÷", "÷")],
    [("7", "7"), ("8", "8"), ("9", "9"), ("×", "×")],
    [("4", "4"), ("5", "5"), ("6", "6"), ("−", "−")],
    [("1", "1"), ("2", "2"), ("3", "3"), ("+", "+")],
    [("±", "sign"), ("0", "0"), (".", "."), ("=", "equal")],
]

for row_number, row in enumerate(keypad):
    columns = st.columns(4, gap="small")

    for column, (label, action) in zip(columns, row):
        with column:
            if action == "clear":
                st.button(
                    label, key=f"key_{row_number}_{label}",
                    on_click=clear
                )
            elif action == "back":
                st.button(
                    label, key=f"key_{row_number}_{label}",
                    on_click=backspace
                )
            elif action == "sign":
                st.button(
                    label, key=f"key_{row_number}_{label}",
                    on_click=toggle_sign
                )
            elif action == "equal":
                st.button(
                    label, key=f"key_{row_number}_{label}",
                    type="primary", on_click=calculate
                )
            else:
                st.button(
                    label, key=f"key_{row_number}_{label}",
                    on_click=add_text, args=(action,)
                )

st.markdown("""
<div class="tip">
    Press Enter to calculate · Backspace to edit · AC to clear<br>
    Supports scientific functions, powers, brackets, π, e and factorial
</div>
""", unsafe_allow_html=True)
