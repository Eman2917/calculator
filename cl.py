import streamlit as st
import math

st.set_page_config(page_title="Scientific Calculator Pro", page_icon="🧮", layout="centered")

# --- ATTRACTIVE COLOR THEME ---
st.markdown("""
<style>
   .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
   .main-card {
        background: white;
        padding: 25px;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    /* Display */
   .display-box {
        background: #1a1d2e;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        text-align: right;
        min-height: 90px;
    }
   .expr { color: #8b90a0; font-size: 18px; min-height: 24px; font-family: monospace; word-break: break-all; }
   .ans { color: #ffffff; font-size: 36px; font-weight: bold; min-height: 45px; word-break: break-all; }

    /* Buttons */
    div.stButton > button {
        height: 55px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 18px;
        border: none;
        transition: 0.2s;
    }
    div.stButton > button:hover { transform: scale(1.03); }

    /* Number buttons */
    button[kind="secondary"] { background: #f1f3f6!important; color: #1a1d2e!important; }
    /* Operator buttons */
   .op-btn button { background: #ff9a3c!important; color: white!important; }
    /* Sci buttons */
   .sci-btn button { background: #667eea!important; color: white!important; }
    /* Equal button */
    div[data-testid="stVerticalBlock"] div:last-child button[kind="primary"] { background: linear-gradient(90deg, #00d2ff, #3a7bd5)!important; }

    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

if "expr" not in st.session_state: st.session_state.expr = ""
if "ans" not in st.session_state: st.session_state.ans = "0"
if "angle" not in st.session_state: st.session_state.angle = "DEG"
if "history" not in st.session_state: st.session_state.history = []

def sin_f(x): return math.sin(math.radians(x)) if st.session_state.angle == "DEG" else math.sin(x)
def cos_f(x): return math.cos(math.radians(x)) if st.session_state.angle == "DEG" else math.cos(x)
def tan_f(x): return math.tan(math.radians(x)) if st.session_state.angle == "DEG" else math.tan(x)

def calculate():
    if not st.session_state.expr: return
    exp = st.session_state.expr.replace("^","**").replace("×","*").replace("÷","/").replace("π","pi")
    funcs = {"sin": sin_f, "cos": cos_f, "tan": tan_f, "sqrt": math.sqrt, "log": math.log10, "ln": math.log, "factorial": math.factorial, "pi": math.pi, "e": math.e}
    try:
        res = eval(exp, {"__builtins__": {}}, funcs)
        if isinstance(res, float): res = round(res, 10)
        st.session_state.ans = str(res)
        st.session_state.history.insert(0, f"{st.session_state.expr} = {res}")
        st.session_state.expr = str(res)
    except ZeroDivisionError: st.session_state.ans = "Math Error"
    except Exception: st.session_state.ans = "Invalid"

def press(v):
    if v == "AC": st.session_state.expr = ""; st.session_state.ans = "0"
    elif v == "DEL": st.session_state.expr = st.session_state.expr[:-1]
    elif v == "=": calculate()
    elif v == "DEG/RAD": st.session_state.angle = "RAD" if st.session_state.angle == "DEG" else "DEG"
    else:
        mapping = {"×":"*","÷":"/","π":"pi","√":"sqrt(","x²":"**2","x³":"**3","!":"factorial("}
        st.session_state.expr += mapping.get(v, v)

# --- UI ---
st.markdown('<div style="text-align:center; color:white; margin-bottom:15px;"><h1 style="color:white; margin:0;">🧮 Scientific Pro</h1><p>Keyboard & Touch Supported</p></div>', unsafe_allow_html=True)

with st.container():
    # DISPLAY
    expr_display = st.session_state.expr if st.session_state.expr else "0"
    ans_display = st.session_state.ans
    st.markdown(f'<div class="display-box"><div class="expr">{expr_display}</div><div class="ans">{ans_display}</div></div>', unsafe_allow_html=True)

    # KEYBOARD INPUT - This is the main feature
    # User can type directly here!
    typed = st.text_input("Type with keyboard and press Enter", value=st.session_state.expr, key="keyboard_input", placeholder="Type: e.g. sin(30)+sqrt(144) and press Enter", label_visibility="collapsed")
    if typed!= st.session_state.expr:
        st.session_state.expr = typed

    col_a, col_b = st.columns([3,1])
    with col_a:
        if st.button("⌨️ Press ENTER to Calculate", type="primary", use_container_width=True):
            calculate()
            st.rerun()
    with col_b:
        if st.button(f"{st.session_state.angle}", use_container_width=True):
            press("DEG/RAD"); st.rerun()

    # BUTTON LAYOUT
    st.markdown("---")
    # Row 1 Scientific
    c = st.columns(5)
    for i, b in enumerate(["sin(", "cos(", "tan(", "log(", "ln("]):
        if c[i].button(b, key=f"s1_{b}", use_container_width=True): press(b); st.rerun()

    c = st.columns(5)
    for i, b in enumerate(["√", "x²", "x³", "^", "!"]):
        if c[i].button(b, key=f"s2_{b}", use_container_width=True): press(b); st.rerun()

    c = st.columns(5)
    for i, b in enumerate(["π", "e", "(", ")", "DEL"]):
        if c[i].button(b, key=f"s3_{b}", use_container_width=True): press(b); st.rerun()

    # Number Pad
    for row in [["7","8","9","÷","AC"], ["4","5","6","×","%"], ["1","2","3","-","+"], ["0",".","=","+",""]]:
        cols = st.columns(5)
        for i, b in enumerate(row):
            if not b: continue
            is_eq = b == "="
            if cols[i].button(b, key=f"n_{row}_{i}", type="primary" if is_eq else "secondary", use_container_width=True):
                press(b); st.rerun()

    with st.expander("📜 History"):
        if st.session_state.history:
            for h in st.session_state.history[:10]: st.code(h)
            if st.button("Clear History"): st.session_state.history = []; st.rerun()
        else: st.write("No history yet")

# Keyboard Shortcuts Help
with st.expander("⌨️ Keyboard Shortcuts"):
    st.markdown("""
    - **Type directly** in the input box above
    - **Enter** = Calculate
    - **Backspace** = Delete
    - Example: `sin(30)`, `sqrt(144)`, `2^8`, `log(100)`, `factorial(5)`
    """)
