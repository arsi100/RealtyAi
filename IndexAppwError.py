from flask import Flask, request, render_template
from openai.error import OpenAIError
import os
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader

os.environ['OPENAI_API_KEY'] = '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'

documents = SimpleDirectoryReader('data').load_data()
index = GPTSimpleVectorIndex.from_documents(documents)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        question = request.form['question']
        try:
            answer = index.query(question)
        except OpenAIError as e:
            error_message = e.error_message
            if "maximum context length" in error_message:
                return render_template('IndexAppDesign.html', answer=f"Error: {error_message}")
            else:
                return render_template('IndexAppDesign.html', answer="An error occurred while processing your request.")
        return render_template('IndexAppDesign.html', answer=answer)
    return render_template('IndexAppDesign.html', answer=None)

if __name__ == '__main__':
    app.run(debug=True)
