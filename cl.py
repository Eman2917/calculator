import streamlit as st
import streamlit.components.v1 as components

st.title('Eman')

st.set_page_config(page_title="Scientific Calculator", page_icon="🧮", layout="centered")

# Hide Streamlit default UI
st.markdown("<style>#MainMenu, footer, header {visibility:hidden;} .stApp{background: linear-gradient(135deg, #667eea, #764ba2);}</style>", unsafe_allow_html=True)

calculator_code = """
<div id="wrapper">
<style>
  *{margin:0; padding:0; box-sizing:border-box; font-family: 'Segoe UI', system-ui;}
  #wrapper{display:flex; justify-content:center; padding:10px;}
  .calc{
    width:380px; background:#ffffff; border-radius:28px; padding:22px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.35);
  }
  /* 2. Proper Display */
  .display{
    background:#0f172a; border-radius:18px; padding:20px 18px; min-height:115px;
    text-align:right; margin-bottom:18px; border: 2px solid #1e293b;
  }
  .expr{color:#94a3b8; font-size:19px; min-height:24px; word-break:break-all; letter-spacing:0.5px;}
  .res{color:#ffffff; font-size:42px; font-weight:800; min-height:48px; word-break:break-all; margin-top:6px;}
  .hint{color:#64748b; font-size:11px; text-align:center; margin-bottom:12px; letter-spacing:1px; font-weight:600;}
  
  .grid{display:grid; grid-template-columns:repeat(5, 1fr); gap:10px;}
  button{
    height:58px; border:none; border-radius:14px; font-size:18px; font-weight:700;
    cursor:pointer; transition:all 0.15s; outline:none;
  }
  button:active{transform:scale(0.92); filter: brightness(0.9);}

  /* 3. Attractive Colors */
  .num{background:#f1f5f9; color:#0f172a;} .num:hover{background:#e2e8f0;}
  .op{background:#fb923c; color:white; font-size:22px;} .op:hover{background:#f97316;}
  .sci{background:#818cf8; color:white; font-size:15px;} .sci:hover{background:#6366f1;}
  .eq{background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%); color:white; grid-column: span 2; font-size:26px;}
  .ac{background:#ef4444; color:white;} .ac:hover{background:#dc2626;}
  .mode-btn{
    width:100%; height:38px; background:#0f172a; color:#38bdf8; 
    border:1.5px solid #334155; border-radius:10px; font-size:13px; margin-bottom:14px; font-weight:700;
  }
</style>

<div class="calc">
  <div class="display">
    <div class="expr" id="expr"></div>
    <div class="res" id="res">0</div>
  </div>
  <div class="hint" id="mode">DEG MODE • KEYBOARD ACTIVE ⌨️</div>
  <button class="mode-btn" onclick="toggleMode()">SWITCH TO RAD / DEG</button>
  
  <div class="grid">
    <button class="sci" onclick="add('sin(')">sin</button>
    <button class="sci" onclick="add('cos(')">cos</button>
    <button class="sci" onclick="add('tan(')">tan</button>
    <button class="sci" onclick="add('log(')">log</button>
    <button class="sci" onclick="add('ln(')">ln</button>

    <button class="sci" onclick="add('sqrt(')">√</button>
    <button class="sci" onclick="add('**2')">x²</button>
    <button class="sci" onclick="add('**3')">x³</button>
    <button class="sci" onclick="add('^')">xʸ</button>
    <button class="sci" onclick="add('!')">x!</button>

    <button class="sci" onclick="add('π')">π</button>
    <button class="sci" onclick="add('e')">e</button>
    <button class="num" onclick="add('(')">(</button>
    <button class="num" onclick="add(')')">)</button>
    <button class="ac" onclick="del()">DEL</button>

    <button class="num" onclick="add('7')">7</button>
    <button class="num" onclick="add('8')">8</button>
    <button class="num" onclick="add('9')">9</button>
    <button class="op" onclick="add('/')">÷</button>
    <button class="ac" onclick="clearAll()">AC</button>

    <button class="num" onclick="add('4')">4</button>
    <button class="num" onclick="add('5')">5</button>
    <button class="num" onclick="add('6')">6</button>
    <button class="op" onclick="add('*')">×</button>
    <button class="num" onclick="add('%')">%</button>

    <button class="num" onclick="add('1')">1</button>
    <button class="num" onclick="add('2')">2</button>
    <button class="num" onclick="add('3')">3</button>
    <button class="op" onclick="add('-')">−</button>
    <button class="op" onclick="add('+')">+</button>

    <button class="num" onclick="add('0')">0</button>
    <button class="num" onclick="add('.')">.</button>
    <button class="eq" onclick="calc()">=</button>
  </div>
</div>

<script>
let expr = "";
let isDeg = true;
const exprEl = document.getElementById('expr');
const resEl = document.getElementById('res');
const modeEl = document.getElementById('mode');

function update(){ exprEl.innerText = expr || ""; if(expr==="") resEl.innerText="0"; }
function add(v){ 
  if(v==='π') expr+='Math.PI'; 
  else if(v==='e') expr+='Math.E'; 
  else expr+=v; 
  update(); 
}
function clearAll(){ expr=""; resEl.innerText="0"; update(); }
function del(){ expr=expr.slice(0,-1); update(); }
function toggleMode(){ isDeg=!isDeg; modeEl.innerText=(isDeg?"DEG":"RAD")+" MODE • KEYBOARD ACTIVE ⌨️"; }
function factorial(n){ if(n<0) return NaN; let r=1; for(let i=2;i<=n;i++) r*=i; return r; }

function calc(){
  try{
    let e = expr.replace(/\\^/g,'**');
    e = e.replace(/sqrt\\(/g,'Math.sqrt(').replace(/log\\(/g,'Math.log10(').replace(/ln\\(/g,'Math.log(');
    e = e.replace(/sin\\(/g, isDeg?'(Math.sin(Math.PI/180*':'(Math.sin(');
    e = e.replace(/cos\\(/g, isDeg?'(Math.cos(Math.PI/180*':'(Math.cos(');
    e = e.replace(/tan\\(/g, isDeg?'(Math.tan(Math.PI/180*':'(Math.tan(');
    e = e.replace(/(\\d+)!/g,'factorial($1)').replace(/factorial\\(/g,'factorial(');
    let result = eval(e);
    if(typeof result==='number') result = parseFloat(result.toFixed(10));
    resEl.innerText=result; expr=String(result); exprEl.innerText="";
  }catch{ resEl.innerText="Error"; }
}

// 1. Proper Keyboard Working
document.addEventListener('keydown', (ev)=>{
  const k = ev.key;
  if((k>='0' && k<='9') || ['+','-','*','/','(',')','.','%','^'].includes(k)){ add(k); ev.preventDefault(); }
  else if(k==='Enter' || k==='='){ calc(); ev.preventDefault(); }
  else if(k==='Backspace'){ del(); ev.preventDefault(); }
  else if(k==='Escape'){ clearAll(); }
});
update();
</script>
</div>
"""

components.html(calculator_code, height=780)


