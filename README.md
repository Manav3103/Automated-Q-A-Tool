# Automated-Q-A-Tool
An AI-powered Streamlit web-app that extracts text from PDF, DOCX, or TXT files and generates Short Answer, Long Answer, and Multiple Choice questions using Google Gemini API. Designed for educators and students to create quizzes and study material instantly.


## 🚀 Features
- 📄 Upload PDF, DOCX, or TXT files
- 🤖 Generate Short, Long, and MCQ questions
- 🧠 Uses Google Gemini AI for content generation
- 💾 Download questions as a text file
- 🖥️ Clean and interactive Streamlit UI

---

## 🛠️ Tech Stack
- **Python 3.11+**
- **Streamlit**
- **Google Gemini API**
- **PyPDF2** and **python-docx**

---

## ⚙️ Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/your-username/ai-question-generator.git
   cd ai-question-generator
````

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Gemini API key:**

   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

   *(On Windows PowerShell use `setx GEMINI_API_KEY "your_api_key_here"`)*

4. **Run the app:**

   ```bash
   streamlit run app.py
   ```

---

## 📦 Example Workflow

1. Upload a document (PDF/DOCX/TXT)
2. Choose question types (Short / Long / MCQ)
3. Click **Generate Questions**
4. Download the generated questions file

---

## 📁 File Overview
_____________________________________________________________________________________________
| File                    | Description                                                     |
| ----------------------- | ----------------------------------------------------------------|
| `app.py`                | Main Streamlit interface and app logic                          |
| `document_processor.py` | Handles text extraction from documents and asso creates preview |
| `question_generator.py` | Generates AI-based questions using Gemini API                   |
| `requirements.txt`      | Lists required dependencies                                     |
|___________________________________________________________________________________________|
---

## 🧑‍💻 Author

**Manav Makkar**
📧 Open for collaboration and improvements!

---

## 🪪 License

This project is open-source under the **MIT License**.
