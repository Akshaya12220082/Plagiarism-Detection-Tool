# Plagiarism-Detection-Tool

A lightweight plagiarism checker built using **classical string matching algorithms** (KMP, LCS, Rabin-Karp, Edit Distance) and modern UI with **Streamlit**.  
This project is fully rooted in **Data Structures and Algorithms (DSA)** logic.

---

## 🔍 Features

- ✅ **Text Comparison** using:
  - KMP (Knuth-Morris-Pratt)
  - Rabin-Karp
  - Longest Common Subsequence (LCS)
  - Edit Distance
- 📄 Upload support: `.txt`, `.pdf`, `.docx`
- 📊 **Visual Reports**: Plagiarism %, Spell Check, Grammar Issues
- 📈 Real-time **Charts**: Bar, Pie, Progress
- ✨ **Rephrasing Suggestions** (DSA + WordNet-based)
- 🧾 Exportable **PDF Report**
- 💡 Fully modular for adding new algorithms

---

## 🏗️ Tech Stack

### 💻 Frontend
- [Streamlit](https://streamlit.io/) – Fast, clean UI like Grammarly
- `Matplotlib` / `Plotly` – For dynamic chart visualizations
- `streamlit-aggrid` – Tabular displays for matched phrases

### 🧠 Backend
- **Python** – Core programming language
- DSA Algorithms:
  - `KMP`, `Rabin-Karp`, `LCS`, `Edit Distance`
  - `Trie`, `Suffix Array`, `Heap`, `Priority Queue`
- `python-docx` / `PyMuPDF` – File reading (DOCX, PDF)
- `fpdf` / `reportlab` – Generate downloadable PDF reports

### 🔤 NLP Tools
- `TextBlob` or `PySpellChecker` – Spelling and grammar checks
- `WordNet` from `NLTK` – Synonym-based rephrasing (non-ML)

---

## 🚀 How to Run

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/plagiarism-detector-dsa.git
   cd plagiarism-detector-dsa
