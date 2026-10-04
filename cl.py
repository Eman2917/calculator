import streamlit as st
import math

st.set_page_config(page_title="Scientific Calculator", page_icon="🧮", layout="centered")

st.markdown("""
<style>
   .stApp { background-color: #f5f5f5; }
    #MainMenu, footer { visibility: hidden; }
    div[data-testid="stVerticalBlock"] { background: white; padding: 25px; border-radius: 20px; box-shadow: 0px 5px 25px rgba(0,0,0,0.15); }
</style>
""", unsafe_allow_html=True)

if "expression" not in st.session_state: st.session_state.expression = ""
if "answer" not in st.session_state: st.session_state.answer = ""
if "angle" not in st.session_state: st.session_state.angle = "DEG"
if "history" not in st.session_state: st.session_state.history = []

def sin_function(x): return math.sin(math.radians(x)) if st.session_state.angle == "DEG" else math.sin(x)
def cos_function(x): return math.cos(math.radians(x)) if st.session_state.angle == "DEG" else math.cos(x)
def tan_function(x): return math.tan(math.radians(x)) if st.session_state.angle == "DEG" else math.tan(x)

def calculate(expression):
    expression = expression.replace("^", "**")
    functions = {"sin": sin_function, "cos": cos_function, "tan": tan_function, "sqrt": math.sqrt, "log": math.log10, "ln": math.log, "factorial": math.factorial, "abs": abs, "pi": math.pi, "e": math.e}
    try:
        result = eval(expression, {"__builtins__": {}}, functions)
        if isinstance(result, float): result = round(result, 10)
        return result
    except ZeroDivisionError: return "Math Error"
    except: return "Invalid Expression"

def button_click(value):
    if value == "AC": st.session_state.expression = ""; st.session_state.answer = ""
    elif value == "DEL": st.session_state.expression = st.session_state.expression[:-1]
    elif value == "=":
        if st.session_state.expression:
            result = calculate(st.session_state.expression)
            st.session_state.answer = str(result)
            if result not in ["Math Error", "Invalid Expression"]:
                st.session_state.history.append(f"{st.session_state.expression} = {result}")
    elif value == "DEG/RAD": st.session_state.angle = "RAD" if st.session_state.angle == "DEG" else "DEG"
    elif value in ["sin","cos","tan","log","ln","sqrt"]: st.session_state.expression += f"{value}("
    elif value == "x²": st.session_state.expression += "**2"
    elif value == "x³": st.session_state.expression += "**3"
    elif value == "π": st.session_state.expression += "pi"
    elif value == "√": st.session_state.expression += "sqrt("
    elif value == "!": st.session_state.expression += "factorial("
    elif value == "×": st.session_state.expression += "*"
    elif value == "÷": st.session_state.expression += "/"
    else: st.session_state.expression += value

st.title("Scientific Calculator")
st.caption(f"Angle Mode: {st.session_state.angle}")

# --- FIXED DISPLAY - NO div bug ---
st.text_input("Expression", value=st.session_state.expression, disabled=True, label_visibility="collapsed", placeholder="0")
if st.session_state.answer:
    st.markdown(f"### = {st.session_state.answer}")

if st.button("DEG / RAD", use_container_width=True):
    button_click("DEG/RAD"); st.rerun()

st.markdown("**Scientific Functions**")
for row in [["sin","cos","tan","log","ln"], ["√","x²","x³","^","!"], ["π","e","(",")","DEL"]]:
    cols = st.columns(5)
    for i, b in enumerate(row):
        if cols[i].button(b, key=f"s_{b}_{i}_{row[0]}", use_container_width=True):
            button_click(b); st.rerun()

st.markdown("**Keypad**")
for r, row in enumerate([["7","8","9","÷","AC"], ["4","5","6","×","("], ["1","2","3","-",")"], ["0",".","%","+","="]]):
    cols = st.columns(5)
    for i, b in enumerate(row):
        if cols[i].button(b, key=f"n_{r}_{i}", use_container_width=True):
            button_click(b); st.rerun()

st.markdown("---")
with st.expander("📜 Calculation History"):
    if st.session_state.history:
        for item in reversed(st.session_state.history): st.write(item)
        if st.button("Clear History"): st.session_state.history = []; st.rerun()
    else: st.write("No calculations yet.")