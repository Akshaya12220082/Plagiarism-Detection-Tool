import os
import re
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from io import BytesIO

# utils
from utils.lcs import lcs_length_words
from utils.edit_distance import edit_distance_words
from utils.rabin_karp import rabin_karp_common_substrings
from utils.kmp import kmp_search
from utils.grammar_checker import check_spelling_and_grammar, rephrase_snippet
from utils.text_extractor import extract_text_from_path

# PDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Config
UPLOAD_FOLDER = "uploads"
ALLOWED_EXT = {"txt", "pdf", "docx", "pptx"}

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "replace-with-a-secure-random-key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


def save_uploaded_file(file_storage):
    filename = secure_filename(file_storage.filename)
    unique = f"{uuid.uuid4().hex}_{filename}"
    path = os.path.join(app.config["UPLOAD_FOLDER"], unique)
    file_storage.save(path)
    return path


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    # get text input or uploaded file
    text_input = (request.form.get("input_text") or "").strip()
    uploaded_file = request.files.get("file")

    if uploaded_file and uploaded_file.filename:
        if not allowed_file(uploaded_file.filename):
            flash("Unsupported file type. Allowed: " + ", ".join(sorted(ALLOWED_EXT)))
            return redirect(url_for("index"))
        path = save_uploaded_file(uploaded_file)
        text_input = extract_text_from_path(path) or text_input

    if not text_input or not text_input.strip():
        flash("Please paste text or upload a file to analyze.")
        return redirect(url_for("index"))

    # Normalize helper
    def words(s): return re.findall(r"\w+", s.lower())

    words_input = words(text_input)

    # For demonstration, reference_text is the same as input OR you can load multiple references
    # If you want to compare against a reference corpus, change this logic.
    reference_text = text_input

    # 1) LCS at word-level
    lcs_len = lcs_length_words(text_input, reference_text)
    min_words = max(1, min(len(words_input), len(words(reference_text))))
    lcs_percent = (lcs_len / min_words) * 100

    # 2) Edit distance (word-level) -> produce similarity %
    ed = edit_distance_words(text_input, reference_text)
    max_w = max(1, max(len(words_input), len(words(reference_text))))
    edit_similarity_percent = (1 - (ed / max_w)) * 100

    # 3) Overlap (unique word intersection)
    overlap = len(set(words_input).intersection(set(words(reference_text))))
    overlap_percent = (overlap / min_words) * 100

    # 4) Rabin-Karp common substrings (character-level, returns substrings)
    matched_blocks = rabin_karp_common_substrings(text_input, reference_text, min_len=30, max_matches=12)
    matched_total_len = sum(len(m) for m in matched_blocks)
    substring_coverage = (matched_total_len / max(1, min(len(text_input), len(reference_text)))) * 100

    # 5) Weighted plagiarism score
    plagiarism_percent = (0.40 * substring_coverage) + (0.30 * overlap_percent) + (0.30 * lcs_percent)
    plagiarism_percent = round(max(0.0, min(100.0, plagiarism_percent)), 2)

    # Spell & grammar
    spelling = check_spelling_and_grammar(text_input, max_suggestions=15)

    # Rephrases for matched blocks
    rephrases = [rephrase_snippet(b, max_changes=3) for b in matched_blocks]

    results = {
        "plagiarism_percent": plagiarism_percent,
        "lcs_percent": round(lcs_percent, 2),
        "overlap_percent": round(overlap_percent, 2),
        "edit_similarity_percent": round(edit_similarity_percent, 2),
        "substring_coverage": round(substring_coverage, 2),
        "matched_blocks": matched_blocks,
        "rephrases": rephrases,
        "spelling": spelling,
        "text": text_input,
    }

    return render_template("result.html", results=results)


@app.route("/download_report", methods=["POST"])
def download_report():
    # expects form field 'text' and results derived client-side or server-side
    text = request.form.get("text", "")
    plagiarism = request.form.get("plagiarism", "N/A")
    matched = request.form.get("matched", "")
    spelling = request.form.get("spelling", "")

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "Plagiarism Detection Report")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(40, y, f"Plagiarism percentage: {plagiarism}")
    y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Matched blocks:")
    y -= 18
    c.setFont("Helvetica", 10)
    for line in (matched.splitlines()[:20] if matched else []):
        if y < 60:
            c.showPage()
            y = height - 40
        c.drawString(48, y, line[:100])
        y -= 14

    if y < 120:
        c.showPage()
        y = height - 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Spelling / grammar issues:")
    y -= 18
    c.setFont("Helvetica", 10)
    for line in (spelling.splitlines()[:60] if spelling else []):
        if y < 60:
            c.showPage()
            y = height - 40
        c.drawString(48, y, line[:100])
        y -= 14

    c.showPage()
    c.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="plagiarism_report.pdf", mimetype="application/pdf")


if __name__ == "__main__":
    app.run(debug=True)
