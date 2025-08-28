import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

# utils
from utils.lcs import lcs_length_words
from utils.edit_distance import edit_distance_words
from utils.rabin_karp import rabin_karp_common_substrings
from utils.kmp import kmp_search
from utils.grammar_checker import check_spelling_and_grammar, rephrase_snippet
from utils.text_extractor import extract_text_from_path  # handles txt, pdf, docx, pptx

app = Flask(__name__)
app.secret_key = '4e09b45fd7be1ab2138e0d9b5b8f7986'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'pptx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ---------------- Helper functions ----------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file_storage):
    filename = secure_filename(file_storage.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_storage.save(filepath)
    return filepath


# ---------------- Routes ----------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    # Get input
    text_input = request.form.get('input_text', '') or ''
    uploaded_file = request.files.get('file')

    # If file uploaded, override text
    if uploaded_file and uploaded_file.filename != '':
        if not allowed_file(uploaded_file.filename):
            flash('Unsupported file type.')
            return redirect(url_for('index'))
        filepath = save_uploaded_file(uploaded_file)
        text_input = extract_text_from_path(filepath)

    if not text_input.strip():
        flash('Please paste text or upload a file.')
        return redirect(url_for('index'))

    # For demo, compare against itself (or you can load reference docs)
    reference_text = text_input  

    # Normalize
    def words(s): return re.findall(r'\w+', s.lower())
    words_input = words(text_input)
    words_ref = words(reference_text)

    # LCS
    lcs = lcs_length_words(text_input, reference_text)
    min_words = max(1, min(len(words_input), len(words_ref)))
    lcs_percent = (lcs / min_words) * 100

    # Edit distance
    ed = edit_distance_words(text_input, reference_text)
    max_w = max(1, max(len(words_input), len(words_ref)))
    edit_similarity_percent = (1 - (ed / max_w)) * 100

    # Overlap
    overlap = len(set(words_input).intersection(set(words_ref)))
    overlap_percent = (overlap / min_words) * 100

    # Rabin-Karp substrings
    matched_blocks = rabin_karp_common_substrings(text_input, reference_text, min_len=30, max_matches=10)
    matched_total_len = sum(len(m) for m in matched_blocks)
    substring_coverage = (matched_total_len / max(1, min(len(text_input), len(reference_text)))) * 100

    # Weighted plagiarism
    plagiarism_percent = (0.40 * substring_coverage) + (0.30 * overlap_percent) + (0.30 * lcs_percent)
    plagiarism_percent = round(max(0.0, min(100.0, plagiarism_percent)), 2)

    # Grammar check
    spelling_issues = check_spelling_and_grammar(text_input, max_suggestions=12)

    # Rephrases
    rephrases = [rephrase_snippet(m) for m in matched_blocks]

    results = {
        'plagiarism_percent': plagiarism_percent,
        'lcs_percent': round(lcs_percent, 2),
        'overlap_percent': round(overlap_percent, 2),
        'edit_similarity_percent': round(edit_similarity_percent, 2),
        'substring_coverage': round(substring_coverage, 2),
        'matched_blocks': matched_blocks,
        'rephrases': rephrases,
        'spelling': spelling_issues,
        'text': text_input
    }

    return render_template('result.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
