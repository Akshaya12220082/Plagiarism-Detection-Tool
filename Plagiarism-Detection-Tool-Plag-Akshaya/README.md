# 🧠 Plagiarism Detection Tool

## 📘 Plagiarism Detection

Plagiarism is the act of copying someone else's content without proper acknowledgment, which is unethical and unacceptable in academics and content creation.  
This tool aims to detect plagiarism in textual content using efficient string matching algorithms instead of relying on machine learning or AI.

---

## 🎯 Project Description

This web application allows users to **paste or upload text files** and check them for plagiarism using classical DSA techniques.  
After analysis, the user is provided with:
- Plagiarism percentage
- Matching content blocks
- Grammar/spelling issues
- Optional rephrasing suggestions

It provides a visual summary using charts and allows downloading of results as a PDF report.

---

## 🔍 Features

- ✅ **Text Comparison** using:
  - Knuth-Morris-Pratt (KMP)
  - Rabin-Karp
  - Longest Common Subsequence (LCS)
  - Edit Distance
- 📄 **Supports file uploads**: `.txt`, `.pdf`, `.docx`
- 📊 **Visual feedback**: plagiarism %, spelling issues, grammar highlights
- 📈 **Charts**: bar, pie, progress indicators (Chart.js)
- ✨ **Rephrasing suggestions** using synonym replacement (WordNet logic)
- 🧾 **PDF report generation**
- 💡 **Modular and scalable** for new algorithms

---

## 🏗️ Tech Stack

### 💻 Frontend
| Technology | Purpose |
|------------|---------|
| **HTML** | Structure of the web page |
| **CSS** | Styling of UI components |
| **JavaScript** | Event handling, data exchange with backend |
| **Chart.js** | For plagiarism and grammar result visualizations |
| **Bootstrap** | For responsive and clean layout |

### 🧠 Backend
| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **Flask** | Backend web framework to handle routing and logic |
| **DSA Algorithms** | KMP, LCS, Rabin-Karp, Edit Distance |
| `python-docx` / `PyMuPDF` | For reading `.docx` and `.pdf` file uploads |
| `fpdf` / `reportlab` | Generate downloadable plagiarism report in PDF format |
| `pyspellchecker` / `TextBlob` | Spelling and grammar checks |
| `NLTK - WordNet` | Synonym lookup for rephrasing suggestions |

----------

