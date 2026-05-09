from flask import Flask, render_template, request
import os

app = Flask(__name__)


def load_chunks(file, chunk_size=1024):
    """Reads a file and splits it into chunks."""
    chunks = []
    leftover = ''
    while True:
        chunk = file.read(chunk_size)

        if not chunk:
            break

        chunk = leftover + chunk

        lines = chunk.splitlines(keepends=True)

        if not chunk.endswith('\n'):
            leftover = lines.pop()
        else:
            leftover = ''

        chunks.extend(lines)

        if leftover:
            chunks.append(leftover)

        return chunks


def find_best_chunk(chunks, query):
    """Finds the chunk that matches the query best."""
    best_score = -1
    best_chunk = "No match found."

    query_words = set(query.lower().split())

    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        score = len(query_words.intersection(chunk_words))  # simple overlap

        if score > best_score:
            best_score = score
            best_chunk = chunk

    return best_chunk

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    query = ""

    if request.method == "POST":
        uploaded_file = request.files["file"]
        query = request.form["query"]

        if uploaded_file:
            text = uploaded_file.read().decode("utf-8")

            from io import StringIO
            file_like = StringIO(text)

            chunks = load_chunks(file_like)

            result = find_best_chunk(chunks, query)

    return render_template(
        "index.html",
        result=result,
        query=query
    )

if __name__ == "__main__":
    app.run(debug=True)