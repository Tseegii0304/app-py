# 🐍 Python Сургалтын Платформ

Монгол хэлний Python & Дата Шинжилгээний интерактив сургалтын вэб апп.

## 📚 Хичээлийн агуулга

| # | Хичээл | Агуулга |
|---|--------|---------|
| 6 | Анхны Python код | print(), коммент, алдаа |
| 7 | Илэрхийлэл & Хувьсагч | Арифметик, хувьсагч |
| 8 | Датаны төрлүүд | int, float, str, bool, list, dict |
| 9 | Давталт & Функц | For loop, функц |
| 10 | Дата унших & бичих | CSV, Excel, JSON |
| 11 | Pandas шинжилгээ | DataFrame, filter, group |
| 12 | Дата визуалчлал | Histogram, Box, Scatter, Heatmap |
| 13 | Статистик шинжилгээ | Descriptive, Correlation, ANOVA, Regression |

## 🚀 Локал дээр ажиллуулах

### 1. Python суулгагдсан эсэхийг шалгах
```bash
python --version  # Python 3.8+ байх ёстой
```

### 2. Virtual environment үүсгэх (санал болгодог)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Хэрэгцээт сангуудыг суулгах
```bash
pip install -r requirements.txt
```

### 4. Датаны файлуудыг зөв байршилд тавих
Дараах файлуудыг `python_course/` хавтасруу хуулна:
- `cars.csv`
- `telecom_churn.csv`
- `kc_house_data.csv`
- `cities.xlsx`

### 5. Апп ажиллуулах
```bash
cd python_course
streamlit run app.py
```

Браузер автоматаар нээгдэж `http://localhost:8501` хаягаар орно.

---

## ☁️ Streamlit Cloud дээр деплой хийх

### 1. GitHub repository үүсгэх
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/python-course.git
git push -u origin main
```

### 2. Streamlit Cloud-д холбох
1. [share.streamlit.io](https://share.streamlit.io) руу орно
2. GitHub-ээрээ нэвтэрнэ
3. **"New app"** дарна
4. Repository, branch (`main`), файл (`app.py`) сонгоно
5. **"Deploy!"** дарна

### 3. Датаны файлуудыг GitHub-д оруулах
CSV болон xlsx файлуудыг repository-д оруулаагүй бол `requirements.txt`-ийн хажуугаар нэмнэ.

---

## 📁 Хавтасны бүтэц
```
python_course/
├── app.py              # Үндсэн Streamlit апп
├── requirements.txt    # Python сангийн жагсаалт
├── README.md           # Энэхүү файл
├── cars.csv
├── telecom_churn.csv
├── kc_house_data.csv
├── cities.xlsx
└── ...
```

## 🛠️ Техникийн тодорхойлолт

- **Frontend:** Streamlit 1.28+
- **Дата боловсруулалт:** Pandas, NumPy
- **Визуалчлал:** Matplotlib, Seaborn
- **Статистик:** SciPy, Scikit-learn
- **Python хувилбар:** 3.8+
