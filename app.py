import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import sys
import traceback
import os

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Python Сургалт",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Nunito:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #334155;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stRadio label { 
    font-size: 0.9rem;
    padding: 4px 0;
}

/* Main background */
.main { background-color: #f8fafc; }

/* Cards */
.lesson-card {
    background: white;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 16px rgba(0,0,0,0.04);
    border-left: 5px solid #6366f1;
}
.info-box {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 12px;
    padding: 16px 20px;
    margin: 12px 0;
    font-size: 0.95rem;
    color: #1e40af;
}
.success-box {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 12px;
    padding: 16px 20px;
    margin: 12px 0;
    color: #166534;
}
.warning-box {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 12px;
    padding: 16px 20px;
    margin: 12px 0;
    color: #92400e;
}
.exercise-box {
    background: linear-gradient(135deg, #fdf4ff 0%, #fce7f3 100%);
    border: 2px dashed #d946ef;
    border-radius: 16px;
    padding: 20px 24px;
    margin: 16px 0;
}
.chapter-header {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    padding: 20px 28px;
    border-radius: 16px;
    margin-bottom: 24px;
}
.chapter-header h1 { color: white; margin: 0; font-size: 1.8rem; }
.chapter-header p { color: #e0e7ff; margin: 6px 0 0 0; font-size: 1rem; }

/* Code blocks */
code {
    font-family: 'JetBrains Mono', monospace !important;
    background: #1e293b;
    color: #e2e8f0;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.88rem;
}
pre {
    background: #1e293b !important;
    border-radius: 12px !important;
    padding: 20px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
    color: #e2e8f0 !important;
    overflow-x: auto;
}

/* Stremlit code area override */
.stCodeBlock { border-radius: 12px; overflow: hidden; }

/* Progress bar */
.progress-wrap {
    display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap;
}
.prog-dot {
    width: 12px; height: 12px; border-radius: 50%;
    background: #e2e8f0; display: inline-block;
}
.prog-dot.done { background: #22c55e; }
.prog-dot.current { background: #6366f1; }

/* Tables */
.stDataFrame { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar Navigation ──────────────────────────────────────────────────────
LESSONS = {
    "🏠 Нүүр хуудас": "home",
    "── PYTHON ҮНДЭС ──": None,
    "6. Анхны Python код": "l6",
    "7. Илэрхийлэл & Хувьсагч": "l7",
    "8. Датаны төрлүүд": "l8",
    "9. Давталт & Функц": "l9",
    "── ДАТА ШИНЖИЛГЭЭ ──": None,
    "10. Дата унших & бичих": "l10",
    "11. Pandas шинжилгээ": "l11",
    "12. Дата визуалчлал": "l12",
    "13. Статистик шинжилгээ": "l13",
}

with st.sidebar:
    st.markdown("### 🐍 Python Сургалт")
    st.markdown("---")
    
    lesson_key = st.radio(
        "Хичээл сонгох",
        options=[k for k in LESSONS if LESSONS[k] is not None or k.startswith("──")],
        format_func=lambda x: x,
        label_visibility="collapsed"
    )
    
    if LESSONS.get(lesson_key) is None and lesson_key.startswith("──"):
        lesson_key = "🏠 Нүүр хуудас"
    
    selected = LESSONS.get(lesson_key, "home")
    
    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.8rem; color:#94a3b8; padding:8px 0;'>
    💡 <b>Зөвлөгөө:</b> Код гүйлгэхийн тулд<br>
    <code style='background:#334155; color:#7dd3fc'>Shift + Enter</code> дарна уу
    </div>
    """, unsafe_allow_html=True)

# ─── Helper: Interactive Code Runner ────────────────────────────────────────
def code_runner(key, default_code="", height=200):
    code = st.text_area("📝 Кодоо энд бичнэ үү:", value=default_code, height=height, key=f"code_{key}")
    col1, col2 = st.columns([1, 5])
    with col1:
        run = st.button("▶ Ажиллуулах", key=f"run_{key}", use_container_width=True)
    if run:
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            exec(compile(code, "<string>", "exec"), {"__builtins__": __builtins__})
            sys.stdout = old_stdout
            output = buf.getvalue()
            if output:
                st.code(output, language=None)
                st.success("✅ Амжилттай!")
            else:
                st.info("ℹ️ Гаралт алга (зөв ажилласан)")
        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"❌ Алдаа: {type(e).__name__}: {e}")

def show_code(code, lang="python"):
    st.code(code, language=lang)

# ─── HOME PAGE ───────────────────────────────────────────────────────────────
if selected == "home":
    st.markdown("""
    <div class='chapter-header'>
        <h1>🐍 Python Сургалтын Платформ</h1>
        <p>Дата шинжилгээний Python сургалт — Монгол хэлээр</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 Нийт хичээл", "8")
    with col2:
        st.metric("🐍 Python үндэс", "4 хичээл")
    with col3:
        st.metric("📊 Дата шинжилгээ", "4 хичээл")
    with col4:
        st.metric("⏱️ Нийт хугацаа", "~12 цаг")

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='lesson-card'>
            <h3>🐍 Python Үндэс</h3>
            <p>Python програмчлалын хэлний суурь ойлголтууд:</p>
            <ul>
                <li>✅ Анхны Python код</li>
                <li>✅ Илэрхийлэл & хувьсагч</li>
                <li>✅ Датаны төрлүүд (int, float, str, list, dict)</li>
                <li>✅ For loop & Функц бичих</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='lesson-card' style='border-left-color: #06b6d4'>
            <h3>📊 Дата Шинжилгээ</h3>
            <p>Pandas, Matplotlib, Seaborn ашиглан дата боловсруулах:</p>
            <ul>
                <li>✅ CSV, Excel, Web-с дата унших</li>
                <li>✅ Pandas DataFrame шинжилгээ</li>
                <li>✅ Дата визуалчлал</li>
                <li>✅ Статистик шинжилгээ</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box'>
        💡 <b>Хэрхэн эхлэх вэ?</b> Зүүн талын цэснээс хичээлээ сонгоно уу. 
        Код бичих хэсэгт кодоо бичиж <b>▶ Ажиллуулах</b> товчийг дарна уу.
    </div>
    """, unsafe_allow_html=True)


# ─── LESSON 6: First Python code ─────────────────────────────────────────────
elif selected == "l6":
    st.markdown("""
    <div class='chapter-header'>
        <h1>📌 Хичээл 6: Анхны Python Код</h1>
        <p>print() функц, коммент бичих, алдааг ойлгох</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 1. Код ажиллуулах")
    st.markdown("""
    <div class='info-box'>
    💡 Jupyter дээр <code>Shift + Enter</code> дарж кодыг ажиллуулна. 
    Энэхүү платформ дээр <b>▶ Ажиллуулах</b> товчийг ашиглана.
    </div>
    """, unsafe_allow_html=True)

    show_code('print("Hello World!")')
    st.markdown("**Гаралт:**")
    st.code("Hello World!", language=None)

    st.markdown("## 2. Коммент бичих")
    st.markdown("`#` тэмдэгтээр эхэлсэн мөрийг Python тайлбар (коммент) гэж үздэг ба ажиллуулдаггүй.")
    show_code('# Принт хийх код\nprint("Hello Python")')

    st.markdown("## 3. Алдаа гарах")
    st.markdown("""
    <div class='warning-box'>
    ⚠️ Алдаа гарах нь програмчлалын байнгын нэг хэсэг! <code>NameError</code> нь тухайн нэр тодорхойлогдоогүй гэсэн үг.
    </div>
    """, unsafe_allow_html=True)
    show_code('frint("Hello Python")  # frint гэж функц байхгүй → NameError')

    st.markdown("---")
    st.markdown("""
    <div class='exercise-box'>
    <h3>🎯 Дасгал ажил</h3>
    <p><code>print()</code> функц ашиглан <b>"My Python Code"</b> гэж хэвлэнэ үү.</p>
    </div>
    """, unsafe_allow_html=True)
    code_runner("l6_ex1", '# Кодоо доор бичнэ үү\n')


# ─── LESSON 7: Expressions & Variables ───────────────────────────────────────
elif selected == "l7":
    st.markdown("""
    <div class='chapter-header'>
        <h1>📌 Хичээл 7: Илэрхийлэл & Хувьсагч</h1>
        <p>Арифметик үйлдлүүд болон хувьсагч ашиглах</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 1. Expressions (Илэрхийлэлүүд)")
    st.markdown("Python дээр хийгдэх үйлдлийг **expression** гэнэ. Жишээ нь арифметик үйлдлүүд:")

    ops = {
        "➕ Нэмэх": ("43 + 60 + 16 + 41", "160"),
        "➖ Хасах": ("50 - 60", "-10"),
        "✖️ Үржих": ("5 * 5", "25"),
        "➗ Хуваах": ("25 / 5", "5.0"),
        "🔢 Бүхэлчлэн хуваах": ("25 // 6", "4"),
        "🔣 Үлдэгдэл": ("25 % 6", "1"),
        "💪 Зэрэг": ("2 ** 8", "256"),
    }

    cols = st.columns(3)
    for i, (name, (code, result)) in enumerate(ops.items()):
        with cols[i % 3]:
            st.markdown(f"**{name}**")
            st.code(f"{code}  # → {result}", language="python")

    st.markdown("## 2. Хувьсагч (Variables)")
    st.markdown("Хувьсагч нь утгыг санах ойд хадгалж, дараа нь ашиглах боломжийг олгоно.")

    show_code("""# Хувьсагч үүсгэж утга оноох
total_min = 43 + 42 + 57   # нийт минут
total_hr = total_min / 60   # цаг руу хөрвүүлэх
print("Нийт минут:", total_min)
print("Нийт цаг:", total_hr)""")

    st.markdown("""
    <div class='info-box'>
    💡 <b>Зөвлөгөө:</b> Хувьсагчийн нэрийг утгатай нь уялдуулан өгөх нь кодыг ойлгомжтой болгодог. 
    Жишээ: <code>x</code> гэхээр <code>total_minutes</code> илүү дүрслэлтэй.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class='exercise-box'>
    <h3>🎯 Дасгал ажлууд</h3>
    <b>Даалгавар 1:</b> 150 минутыг цаг руу хөрвүүлэх хувьсагч үүсгэ.
    </div>
    """, unsafe_allow_html=True)
    code_runner("l7_ex1", "minutes = 150\nhours = minutes / 60\nprint(hours)")

    st.markdown("""
    <div class='exercise-box'>
    <b>Даалгавар 2:</b> x = 3 + 2 * 2, y = (3 + 2) * 2, z = x + y утгуудыг тооцоол.
    </div>
    """, unsafe_allow_html=True)
    code_runner("l7_ex2", "x = 3 + 2 * 2\ny = (3 + 2) * 2\nz = x + y\nprint('x =', x)\nprint('y =', y)\nprint('z =', z)")


# ─── LESSON 8: Data Types ─────────────────────────────────────────────────────
elif selected == "l8":
    st.markdown("""
    <div class='chapter-header'>
        <h1>📌 Хичээл 8: Python Датаны Төрлүүд</h1>
        <p>int, float, str, bool, list, dict — Датаны үндсэн төрлүүд</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 1. Үндсэн датаны төрлүүд")

    col1, col2 = st.columns(2)
    with col1:
        types_info = [
            ("int", "Бүхэл тоо", "-1, 0, 42", "#6366f1"),
            ("float", "Бодит тоо", "1.73, -3.14", "#06b6d4"),
            ("str", "Тэмдэгт мөр", "'Hello', \"Python\"", "#f59e0b"),
            ("bool", "Логик утга", "True, False", "#10b981"),
        ]
        for dtype, desc, ex, color in types_info:
            st.markdown(f"""
            <div style='background:white; border-left:4px solid {color}; border-radius:8px; 
                        padding:10px 14px; margin:8px 0; box-shadow:0 1px 3px rgba(0,0,0,0.06)'>
                <b style='color:{color}'>{dtype}</b> — {desc}<br>
                <code style='font-size:0.82rem'>{ex}</code>
            </div>""", unsafe_allow_html=True)

    with col2:
        types_info2 = [
            ("list", "Жагсаалт", "[1, 'a', True]", "#ec4899"),
            ("dict", "Толь бичиг", "{'name': 'User'}", "#8b5cf6"),
            ("tuple", "Хувиршгүй жагсаалт", "(1, 2, 3)", "#64748b"),
            ("NoneType", "Утгагүй", "None", "#94a3b8"),
        ]
        for dtype, desc, ex, color in types_info2:
            st.markdown(f"""
            <div style='background:white; border-left:4px solid {color}; border-radius:8px; 
                        padding:10px 14px; margin:8px 0; box-shadow:0 1px 3px rgba(0,0,0,0.06)'>
                <b style='color:{color}'>{dtype}</b> — {desc}<br>
                <code style='font-size:0.82rem'>{ex}</code>
            </div>""", unsafe_allow_html=True)

    st.markdown("## 2. type() функцоор төрлийг шалгах")
    show_code("""print(type(1.73))      # float
print(type(-1))        # int
print(type('Hello'))   # str
print(type(True))      # bool
print(type([1,2,3]))   # list
print(type({'a': 1}))  # dict""")

    st.markdown("## 3. Датаны төрлийг хөрвүүлэх")
    show_code("""print(float(2))    # 2 → 2.0
print(int(1.9))    # 1.9 → 1 (бүхэлчлэгдэнэ)
print(str(42))     # 42 → '42'
print(int('10'))   # '10' → 10""")

    st.markdown("## 4. List дээр ажиллах")

    tab1, tab2 = st.tabs(["📋 Үндсэн үйлдлүүд", "🔧 Аргууд"])
    with tab1:
        show_code("""lst = ['Element1', 'Element2', 'Element3', 'Element4', 'Element5']

print(lst[0])       # Анхны элемент → 'Element1'
print(lst[-1])      # Сүүлийн элемент → 'Element5'
print(lst[1:3])     # Slice → ['Element2', 'Element3']
print(len(lst))     # Урт → 5""")
    with tab2:
        show_code("""lst = ['red', 'yellow', 'green']

lst.append('blue')   # Нэмэх
print(lst)

lst.remove('red')    # Устгах
print(lst)

lst.sort()           # Эрэмбэлэх
print(lst)""")

    st.markdown("---")
    st.markdown("""
    <div class='exercise-box'>
    <h3>🎯 Дасгал: Кодыг ажиллуулж, үр дүнг харна уу</h3>
    </div>
    """, unsafe_allow_html=True)
    code_runner("l8_ex", """height = 1.73
Age = 25
tall = True
Name = 'Монгол'
info = [height, Age, tall, Name]

print("Өндөр:", height, "→ төрөл:", type(height).__name__)
print("Нас:", Age, "→ төрөл:", type(Age).__name__)
print("Өндөр эсэх:", tall, "→ төрөл:", type(tall).__name__)
print("Нэр:", Name, "→ төрөл:", type(Name).__name__)
print("Мэдээлэл:", info)""")


# ─── LESSON 9: Loops & Functions ─────────────────────────────────────────────
elif selected == "l9":
    st.markdown("""
    <div class='chapter-header'>
        <h1>📌 Хичээл 9: Давталт & Функц</h1>
        <p>For loop болон функц бичих арга</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔄 For Loop", "⚙️ Функц"])

    with tab1:
        st.markdown("## For Loop — Давталт")
        st.markdown("Нэг үйлдлийг олон дахин давтах шаардлагатай үед `for loop` ашигладаг.")

        st.markdown("### Жишээ 1: List-ийн элементүүдийг хэвлэх")
        show_code("""dates = [1982, 1980, 1973]
for year in dates:
    print(year)""")

        st.markdown("### Жишээ 2: range() ашиглах")
        show_code("""for i in range(0, 5):
    print(i)""")

        st.markdown("### Жишээ 3: enumerate() — Индекстэй давталт")
        show_code("""colors = ['улаан', 'шар', 'ногоон', 'хөх']
for i, color in enumerate(colors):
    print(f"{i}: {color}")""")

        st.markdown("---")
        st.markdown("""
        <div class='exercise-box'>
        <h3>🎯 Дасгал</h3>
        <p>Доорх жагсаалтыг үүсгэж, элемент болгоныг хэвлэх loop бич:</p>
        <code>genres = ['rock', 'R&B', 'Soundtrack', 'soul', 'pop']</code>
        </div>
        """, unsafe_allow_html=True)
        code_runner("l9_loop", "genres = ['rock', 'R&B', 'Soundtrack', 'soul', 'pop']\n# for loop бич\n")

    with tab2:
        st.markdown("## Функц (Function)")
        st.markdown("""
        <div class='info-box'>
        Функц нь кодыг <b>хялбаршуулах</b>, <b>олон дахин ашиглах</b> зорилготой.<br>
        Python-д 2 төрлийн функц байдаг: <b>Pre-defined</b> (суурилагдсан) ба <b>User-defined</b> (хэрэглэгчийн)
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Pre-defined функцүүд")
        show_code("""ratings = [10.0, 8.5, 9.5, 7.0, 9.0]
print(sum(ratings))   # Нийлбэр → 44.0
print(len(ratings))   # Тоо → 5
print(max(ratings))   # Хамгийн их → 10.0
print(min(ratings))   # Хамгийн бага → 7.0""")

        st.markdown("### User-defined функцүүд")
        show_code("""def нэмэх(a, b):
    \"\"\"Хоёр тоог нэмэх функц\"\"\"
    return a + b

def album_type(artist, album, year):
    if year > 1980:
        return f"{artist} - {album}: Орчин үеийн"
    else:
        return f"{artist} - {album}: Хуучин"

print(нэмэх(5, 3))
print(album_type("Michael Jackson", "Thriller", 1982))""")

        st.markdown("---")
        st.markdown("""
        <div class='exercise-box'>
        <h3>🎯 Дасгал</h3>
        <p>Тойргийн талбайг тооцоолох функц бич: <code>def circle_area(radius):</code></p>
        <p>Томьёо: π × r²  (pi = 3.14159)</p>
        </div>
        """, unsafe_allow_html=True)
        code_runner("l9_func", """def circle_area(radius):
    pi = 3.14159
    # area тооцоол
    pass

print(circle_area(5))   # 78.53975 гарах ёстой
print(circle_area(10))  # 314.159 гарах ёстой""")


# ─── LESSON 10: Read & Write Data ────────────────────────────────────────────
elif selected == "l10":
    st.markdown("""
    <div class='chapter-header'>
        <h1>📌 Хичээл 10: Дата Унших & Бичих</h1>
        <p>CSV, Excel файлаас pandas ашиглан дата оруулах</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📄 CSV", "📊 Excel", "💾 Экспорт"])

    with tab1:
        st.markdown("## CSV Дата Оруулах")
        show_code("""import pandas as pd

# CSV уншиж DataFrame үүсгэх
df = pd.read_csv('cars.csv')

print(df.shape)      # Мөр, баганы тоо
print(df.head())     # Эхний 5 мөр
print(df.dtypes)     # Датаны төрлүүд""")

        st.markdown("### 🔴 Амьд жишээ — cars.csv")
        try:
            df_cars = pd.read_csv('/mnt/user-data/uploads/cars.csv')
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Нийт мөр", df_cars.shape[0])
            with col2: st.metric("Нийт багана", df_cars.shape[1])
            with col3: st.metric("Тоон баганы тоо", len(df_cars.select_dtypes(include='number').columns))
            st.dataframe(df_cars.head(8), use_container_width=True)
        except Exception as e:
            st.error(f"Файл олдсонгүй: {e}")

        st.markdown("### Тусгай параметрүүд")
        show_code("""# Тусгай хязгаарлагчтай CSV
df = pd.read_csv('data.csv', sep=';')

# Толгойгүй CSV
df = pd.read_csv('data.csv', header=None)

# Тодорхой баганыг унших
df = pd.read_csv('data.csv', usecols=['name', 'price'])

# Мөрийн тоог хязгаарлах
df = pd.read_csv('data.csv', nrows=100)""")

    with tab2:
        st.markdown("## Excel Дата Оруулах")
        show_code("""import pandas as pd

# Excel уншиж DataFrame үүсгэх
df = pd.read_excel('cities.xlsx')
print(df.head())

# Тодорхой хуудас унших
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')""")

        st.markdown("### 🔴 Амьд жишээ — cities.xlsx")
        try:
            df_cities = pd.read_excel('/mnt/user-data/uploads/cities.xlsx')
            st.dataframe(df_cities.head(10), use_container_width=True)
        except Exception as e:
            st.warning(f"Excel файл: {e}")

    with tab3:
        st.markdown("## DataFrame-г Экспортлох")
        show_code("""import pandas as pd

df = pd.read_csv('cars.csv')

# CSV-рүү хадгалах
df.to_csv('export.csv', index=False)

# Excel-рүү хадгалах
df.to_excel('export.xlsx', index=False, sheet_name='Data')

# JSON-рүү хадгалах
df.to_json('export.json', orient='records')

print("Амжилттай хадгаллаа!")""")

        st.markdown("""
        <div class='success-box'>
        ✅ <b>index=False</b> параметр ашиглан индексийг хадгалахаас зайлсхийж болно.
        </div>
        """, unsafe_allow_html=True)


# ─── LESSON 11: Pandas Analysis ──────────────────────────────────────────────
elif selected == "l11":
    st.markdown("""
    <div class='chapter-header'>
        <h1>📌 Хичээл 11: Pandas Дата Шинжилгээ</h1>
        <p>DataFrame-тэй ажиллах, эрэмбэлэх, филтэрлэх, групплэх</p>
    </div>
    """, unsafe_allow_html=True)

    @st.cache_data
    def load_cars():
        return pd.read_csv('/mnt/user-data/uploads/cars.csv')

    df = load_cars()

    tabs = st.tabs(["🔍 Шинжих", "📊 Эрэмбэлэх", "🔧 Филтэр", "📈 Групп", "🔄 Хувиргалт"])

    with tabs[0]:
        st.markdown("## Data Exploration — Датаг шинжих")
        show_code("""df.head()          # Эхний 5 мөр
df.tail()          # Сүүлийн 5 мөр
df.shape           # (мөр, багана)
df.info()          # Датаны төрлүүд, null утгууд
df.describe()      # Статистик хураангуй
df.columns         # Баганын нэрс
df.dtypes          # Датаны төрлүүд""")

        st.markdown("### 🔴 Амьд үр дүн")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**head()**")
            st.dataframe(df.head(), use_container_width=True)
        with col2:
            st.markdown("**describe()**")
            st.dataframe(df.describe().round(2), use_container_width=True)

    with tabs[1]:
        st.markdown("## Sorting — Эрэмбэлэх")
        show_code("""# Нэг баганаар эрэмбэлэх
df.sort_values('price', ascending=True)    # Өсөх
df.sort_values('price', ascending=False)   # Буурах

# Олон баганаар эрэмбэлэх
df.sort_values(['make', 'price'], ascending=[True, False])""")

        st.markdown("### Жишээ: Үнэгээр эрэмбэлэх")
        sort_col = st.selectbox("Эрэмбэлэх багана:", df.select_dtypes(include='number').columns[:5])
        asc = st.checkbox("Өсөх дарааллаар", value=False)
        st.dataframe(df.sort_values(sort_col, ascending=asc)[['make', sort_col]].head(10), use_container_width=True)

    with tabs[2]:
        st.markdown("## Indexing & Filtering — Филтэр")
        show_code("""# Нэг баганыг сонгох
df['make']
df[['make', 'price', 'horsepower']]

# Нөхцөлт филтэр
df[df['price'] > 20000]
df[df['make'] == 'toyota']

# Олон нөхцөл
df[(df['price'] > 15000) & (df['horsepower'] > 100)]

# isin() — Олон утгын дотор байгааг шалгах
df[df['make'].isin(['toyota', 'honda', 'mazda'])]""")

        st.markdown("### Жишээ: Интерактив филтэр")
        makes = sorted(df['make'].dropna().unique())
        selected_make = st.multiselect("Загварыг сонгох:", makes, default=makes[:3])
        if selected_make:
            filtered = df[df['make'].isin(selected_make)][['make', 'price', 'horsepower', 'body-style']].dropna()
            st.dataframe(filtered, use_container_width=True)

    with tabs[3]:
        st.markdown("## Grouping — Групплэх")
        show_code("""# Групплэх
df.groupby('make')['price'].mean()
df.groupby('make')['price'].agg(['mean', 'min', 'max', 'count'])

# Pivot table
df.pivot_table(values='price', index='make', columns='body-style', aggfunc='mean')""")

        st.markdown("### Жишээ: Загвараар дундаж үнэ")
        grp = df.groupby('make')['price'].mean().dropna().sort_values(ascending=False).head(10).reset_index()
        grp.columns = ['Загвар', 'Дундаж үнэ ($)']
        grp['Дундаж үнэ ($)'] = grp['Дундаж үнэ ($)'].round(0).astype(int)
        st.dataframe(grp, use_container_width=True)

    with tabs[4]:
        st.markdown("## DataFrame Хувиргалтууд")
        show_code("""# Шинэ багана нэмэх
df['price_euro'] = df['price'] * 0.92

# Багана устгах
df.drop(columns=['column_name'], inplace=True)

# Null утгуудыг дүүргэх
df['price'].fillna(df['price'].mean(), inplace=True)

# Дахин нэрлэх
df.rename(columns={'price': 'Price_USD'}, inplace=True)

# apply() — функц хэрэглэх
df['price_level'] = df['price'].apply(lambda x: 'Өндөр' if x > 20000 else 'Бага')""")

        st.markdown("### Жишээ: Үнийн түвшин нэмэх")
        df_sample = df[['make', 'price']].dropna().head(10).copy()
        df_sample['Үнийн түвшин'] = df_sample['price'].apply(lambda x: '🔴 Өндөр' if x > 20000 else ('🟡 Дунд' if x > 12000 else '🟢 Бага'))
        st.dataframe(df_sample, use_container_width=True)


# ─── LESSON 12: Data Visualization ──────────────────────────────────────────
elif selected == "l12":
    st.markdown("""
    <div class='chapter-header'>
        <h1>📌 Хичээл 12: Дата Визуалчлал</h1>
        <p>Matplotlib & Seaborn ашиглан график байгуулах</p>
    </div>
    """, unsafe_allow_html=True)

    @st.cache_data
    def load_churn():
        return pd.read_csv('/mnt/user-data/uploads/telecom_churn.csv')

    df = load_churn()

    tabs = st.tabs(["📊 Histogram", "📦 Box Plot", "🎻 Violin", "📈 Scatter", "🔥 Heatmap"])

    with tabs[0]:
        st.markdown("## Histogram — Тархалт")
        show_code("""import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(10, 5))
df['Total day minutes'].hist(bins=30, color='steelblue', edgecolor='white', ax=ax)
ax.set_title('Өдрийн дуудлагын минутын тархалт')
ax.set_xlabel('Минут')
ax.set_ylabel('Тоо')
plt.show()""")

        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        df['Total day minutes'].hist(bins=30, color='#6366f1', edgecolor='white', ax=axes[0])
        axes[0].set_title('Өдрийн дуудлагын минут', fontsize=12)
        axes[0].set_xlabel('Минут'); axes[0].set_ylabel('Тоо')

        df['Customer service calls'].hist(bins=10, color='#06b6d4', edgecolor='white', ax=axes[1])
        axes[1].set_title('Үйлчилгээний дуудлагын тоо', fontsize=12)
        axes[1].set_xlabel('Дуудлага'); axes[1].set_ylabel('Тоо')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with tabs[1]:
        st.markdown("## Box Plot — Хайрцган диаграм")
        show_code("""fig, ax = plt.subplots()
df.boxplot(column='Total day minutes', by='Churn', ax=ax)
plt.suptitle('')
ax.set_title('Churn-аар хуваасан өдрийн дуудлага')
plt.show()""")

        fig, ax = plt.subplots(figsize=(8, 5))
        df.boxplot(column='Total day minutes', by='Churn', ax=ax,
                   boxprops=dict(color='#6366f1'), medianprops=dict(color='#ef4444', linewidth=2))
        plt.suptitle('')
        ax.set_title('Churn-аар өдрийн дуудлагын минут', fontsize=12)
        ax.set_xlabel('Churn (Явсан эсэх)'); ax.set_ylabel('Минут')
        st.pyplot(fig)
        plt.close()

    with tabs[2]:
        st.markdown("## Violin Plot — Хийл диаграм")
        show_code("""fig, ax = plt.subplots()
sns.violinplot(data=df, x='Churn', y='Total day minutes', ax=ax)
plt.show()""")

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.violinplot(data=df, x='Churn', y='Total day minutes',
                       palette=['#6366f1', '#ef4444'], ax=ax)
        ax.set_title('Violin Plot: Churn vs Өдрийн минут', fontsize=12)
        st.pyplot(fig)
        plt.close()

    with tabs[3]:
        st.markdown("## Scatter Plot — Цэгэн диаграм")
        show_code("""fig, ax = plt.subplots()
ax.scatter(df['Total day minutes'], df['Total day charge'],
           alpha=0.3, color='steelblue')
ax.set_xlabel('Өдрийн минут')
ax.set_ylabel('Өдрийн төлбөр ($)')
plt.show()""")

        fig, ax = plt.subplots(figsize=(8, 5))
        colors = df['Churn'].map({True: '#ef4444', False: '#6366f1'})
        ax.scatter(df['Total day minutes'], df['Total day charge'],
                   alpha=0.2, c=colors, s=10)
        ax.set_xlabel('Өдрийн минут'); ax.set_ylabel('Өдрийн төлбөр ($)')
        ax.set_title('Минут vs Төлбөр (Улаан=Явсан, Цэнхэр=Байгаа)', fontsize=11)
        st.pyplot(fig)
        plt.close()

    with tabs[4]:
        st.markdown("## Heatmap — Корреляцийн зураглал")
        show_code("""import seaborn as sns

corr = df.select_dtypes(include='number').corr()
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
plt.show()""")

        num_cols = df.select_dtypes(include='number').columns[:8]
        corr = df[num_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r',
                    center=0, ax=ax, annot_kws={'size': 8})
        ax.set_title('Корреляцийн Heatmap', fontsize=12)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()


# ─── LESSON 13: Statistical Analysis ─────────────────────────────────────────
elif selected == "l13":
    st.markdown("""
    <div class='chapter-header'>
        <h1>📌 Хичээл 13: Статистик Шинжилгээ</h1>
        <p>Дескриптив статистик, корреляци, ANOVA, регрессийн шинжилгээ</p>
    </div>
    """, unsafe_allow_html=True)

    @st.cache_data
    def load_house():
        return pd.read_csv('/mnt/user-data/uploads/kc_house_data.csv')

    df = load_house()

    tabs = st.tabs(["📋 Дескриптив", "🔗 Корреляци", "📊 ANOVA", "📉 Регресс"])

    with tabs[0]:
        st.markdown("## Descriptive Analysis — Дискрептив статистик")
        show_code("""import pandas as pd

df = pd.read_csv('kc_house_data.csv')

# Үндсэн статистик
print(df.describe())

# Тусгай тооцоолол
print("Дундаж үнэ:", df['price'].mean())
print("Медиан:", df['price'].median())
print("Стандарт хазайлт:", df['price'].std())
print("Хамгийн их:", df['price'].max())
print("Хамгийн бага:", df['price'].min())""")

        st.markdown("### Үр дүн")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Дундаж үнэ", f"${df['price'].mean():,.0f}")
        with col2: st.metric("Медиан", f"${df['price'].median():,.0f}")
        with col3: st.metric("Хамгийн их", f"${df['price'].max():,.0f}")
        with col4: st.metric("Нийт өмч", f"{len(df):,}")

        st.dataframe(df[['price', 'bedrooms', 'bathrooms', 'sqft_living', 'grade']].describe().round(2), use_container_width=True)

    with tabs[1]:
        st.markdown("## Correlation Analysis — Корреляцийн шинжилгээ")
        show_code("""# Корреляцийн матриц
corr_matrix = df.corr()

# Үнэтэй хамгийн их корреляцтай баганууд
price_corr = df.corr()['price'].sort_values(ascending=False)
print(price_corr)""")

        num_df = df.select_dtypes(include='number').drop(columns=['id'], errors='ignore')
        price_corr = num_df.corr()['price'].drop('price').sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 5))
        colors = ['#22c55e' if v > 0 else '#ef4444' for v in price_corr.values]
        ax.barh(price_corr.index, price_corr.values, color=colors, edgecolor='white')
        ax.set_title('Үнэтэй (price) корреляц', fontsize=12)
        ax.set_xlabel('Корреляцийн коэффициент'); ax.axvline(0, color='black', linewidth=0.5)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        st.markdown("""
        <div class='info-box'>
        💡 <b>Корреляцийн утгын тайлбар:</b><br>
        • +1.0 ойртох тусам эерэг хамааралтай (нэг нь нэмэгдэхэд нөгөө нь нэмэгдэнэ)<br>
        • -1.0 ойртох тусам сөрөг хамааралтай<br>
        • 0 ойртох тусам хамааралгүй
        </div>
        """, unsafe_allow_html=True)

    with tabs[2]:
        st.markdown("## ANOVA — Вариацын шинжилгээ")
        show_code("""from scipy import stats

# Өрөөний тоогоор ангилж ANOVA шалгах
groups = [df[df['bedrooms']==i]['price'] for i in [2,3,4,5]]
f_stat, p_value = stats.f_oneway(*groups)
print(f"F-статистик: {f_stat:.2f}")
print(f"P-утга: {p_value:.4f}")
if p_value < 0.05:
    print("✅ Ялгаа статистикийн хувьд чухал!")""")

        from scipy import stats
        groups = [df[df['bedrooms']==i]['price'].dropna() for i in [2,3,4,5] if len(df[df['bedrooms']==i]) > 0]
        f_stat, p_value = stats.f_oneway(*groups)
        col1, col2 = st.columns(2)
        with col1: st.metric("F-статистик", f"{f_stat:.2f}")
        with col2: st.metric("P-утга", f"{p_value:.6f}")

        if p_value < 0.05:
            st.success("✅ p < 0.05: Өрөөний тоо үнэд статистикийн хувьд мэдэгдэхүйц нөлөөтэй!")

        fig, ax = plt.subplots(figsize=(10, 5))
        bed_price = df[df['bedrooms'].between(1, 6)].groupby('bedrooms')['price'].mean()
        ax.bar(bed_price.index, bed_price.values, color='#6366f1', edgecolor='white')
        ax.set_title('Өрөөний тооны дундаж үнэ', fontsize=12)
        ax.set_xlabel('Өрөөний тоо'); ax.set_ylabel('Дундаж үнэ ($)')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with tabs[3]:
        st.markdown("## Regression Analysis — Регрессийн шинжилгээ")
        show_code("""from sklearn.linear_model import LinearRegression
import numpy as np

# Энгийн шугаман регресс
X = df[['sqft_living']]
y = df['price']

model = LinearRegression()
model.fit(X, y)

print(f"R² оноо: {model.score(X, y):.4f}")
print(f"Коэффициент: {model.coef_[0]:.2f}")
print(f"Хугарлын цэг: {model.intercept_:.2f}")

# Урьдчилсан таамаглал
pred = model.predict([[2000]])  # 2000 кв.фут
print(f"2000 кв.фут байрны таамагласан үнэ: ${pred[0]:,.0f}")""")

        try:
            from sklearn.linear_model import LinearRegression

            sample = df[['sqft_living', 'price']].dropna().sample(2000, random_state=42)
            X = sample[['sqft_living']]
            y = sample['price']
            model = LinearRegression()
            model.fit(X, y)
            r2 = model.score(X, y)

            col1, col2, col3 = st.columns(3)
            with col1: st.metric("R² оноо", f"{r2:.4f}")
            with col2: st.metric("Коэффициент", f"{model.coef_[0]:.2f}")
            with col3: st.metric("2000 sqft таамаглал", f"${model.predict([[2000]])[0]:,.0f}")

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.scatter(sample['sqft_living'], sample['price'], alpha=0.2, color='#6366f1', s=8, label='Бодит')
            x_line = np.linspace(sample['sqft_living'].min(), sample['sqft_living'].max(), 100)
            ax.plot(x_line, model.predict(x_line.reshape(-1, 1)), color='#ef4444', linewidth=2, label='Регрессийн шугам')
            ax.set_xlabel('Байрны хэмжээ (кв.фут)'); ax.set_ylabel('Үнэ ($)')
            ax.set_title('Шугаман регресс: Хэмжээ vs Үнэ', fontsize=12)
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        except ImportError:
            st.warning("sklearn суулгаагүй байна. `pip install scikit-learn` ажиллуулна уу.")


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#94a3b8; font-size:0.82rem; padding:12px 0'>
    🐍 Python Сургалтын Платформ • Монгол хэлний сургалт
</div>
""", unsafe_allow_html=True)
