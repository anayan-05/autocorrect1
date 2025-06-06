from flask import Flask, render_template, request
from autocorrect import load_words, build_vocab, build_frequency_from_corpus, autocorrect

app = Flask(__name__)

# Load dictionary and corpus once when app starts
dictionary_words = load_words('dictionary.txt')
dictionary_set = set(dictionary_words)
word_counts = build_frequency_from_corpus('corpus.txt')

@app.route("/", methods=["GET", "POST"])
def index():
    original_text = ""
    corrected_text = ""

    if request.method == "POST":
        original_text = request.form["input_text"]  # Match 'input_text' from textarea name
        corrected_text = ' '.join([
            autocorrect(word, dictionary_set, word_counts) for word in original_text.split()
        ])

    return render_template("index.html", original=original_text, corrected=corrected_text)

if __name__ == "__main__":
    app.run(debug=True)
