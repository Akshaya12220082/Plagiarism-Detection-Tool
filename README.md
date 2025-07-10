# Plagiarism-Detection-Tool

## 📘 Plagiarism Detection

Plagiarism refers to the act of copying or closely imitating the language, ideas, or work of another author without proper acknowledgment. It is a major concern in academics, publishing, and content creation. Detecting plagiarism is essential to uphold originality, intellectual integrity, and fairness in evaluation systems.

---

## 🎯 Project Description

This tool is a lightweight plagiarism checker built entirely on **classical string matching algorithms** such as **KMP**, **Rabin-Karp**, **LCS**, and **Edit Distance** — showcasing the real-world power of **Data Structures and Algorithms (DSA)** without relying on AI/ML models.

Users can input text manually or upload `.txt`, `.pdf`, or `.docx` files. The tool scans for exact and near-duplicate matches, provides a plagiarism score, detects grammar and spelling errors, and even suggests rephrased alternatives using logic-based synonym replacement.

The clean UI is powered by **Streamlit**, and results are visualized through charts and downloadable reports — delivering an intuitive experience backed by solid algorithmic foundations.


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

