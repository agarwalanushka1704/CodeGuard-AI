# CodeGuard AI 🛡️

### AI-Powered Code Quality Analysis & Bug Risk Prediction

CodeGuard AI is a machine learning-based web application that analyzes Python code, evaluates its quality, estimates potential bug risk, and provides intelligent recommendations to improve code structure and maintainability.

🌐 **Live Demo:** https://codeguard-ai-k3pr.onrender.com

📂 **GitHub Repository:** https://github.com/agarwalanushka1704/CodeGuard-AI

---

## 🚀 Features

- **Code Quality Score:** Evaluates code quality on a scale of 0–100.
- **Bug Risk Prediction:** Estimates the potential risk of bugs in submitted Python code.
- **Code Metrics:** Analyzes functions, loops, branches, complexity, nesting depth, and other code characteristics.
- **Code Findings:** Identifies potential code quality issues.
- **Smart Recommendations:** Provides suggestions to improve code quality.
- **Interactive Code Editor:** Allows users to paste Python code for analysis.
- **Machine Learning Integration:** Uses trained regression models to generate predictions.

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, Flask |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Code Analysis | Python AST |
| Deployment | Render |
| Version Control | Git & GitHub |

## 🧠 Machine Learning Models

CodeGuard AI uses three regression algorithms:

1. Linear Regression
2. Random Forest Regressor
3. Gradient Boosting Regressor

These models are trained using a structured code dataset containing software complexity and code quality-related features.

The application uses the trained models to estimate code quality and potential bug risk.

## 📊 Analysis Parameters

The application extracts several code characteristics, including:

- Lines of Code
- Number of Functions
- Branches and Loops
- Exception Handlers
- Boolean Operations
- Cyclomatic Complexity
- Nesting Depth
- Long Lines
- Duplicate Lines
- Comments and Comment Ratio
- Risky Function Calls

## 📁 Project Structure

```text
CodeGuard-AI/
│
├── app.py
├── create_dataset.py
├── feature_extractor.py
├── predictor.py
├── train_model.py
├── test_features.py
├── requirements.txt
│
├── dataset/
│   ├── code_dataset.csv
│   └── code_dataset_backup.csv
│
├── model/
│   ├── bug_risk_model.pkl
│   ├── quality_model.pkl
│   ├── features.pkl
│   └── evaluation.json
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   └── index.html
│
└── .gitignore
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/agarwalanushka1704/CodeGuard-AI.git
```

### 2. Navigate to the Project Directory

```bash
cd CodeGuard-AI
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

### 7. Open in Browser

```text
http://127.0.0.1:5000
```

## 🌐 Live Deployment

The application is deployed using Render.

**Live URL:** https://codeguard-ai-k3pr.onrender.com

## 🔮 Future Enhancements

- Syntax error line highlighting
- Support for additional programming languages
- More advanced static code analysis
- Improved machine learning predictions
- Downloadable code analysis reports
- Enhanced code quality recommendations

## ⚠️ Disclaimer

Bug risk is an estimated machine learning prediction based on extracted code features. It does not guarantee detection of actual software bugs.

## 👩‍💻 Contributors

**Anushka Agarwal** — Developer & Project Contributor

**Aditi** — Developer & Project Contributor

---

⭐ If you find this project interesting, consider starring the repository!

**Built with Python, Machine Learning & Flask.**
