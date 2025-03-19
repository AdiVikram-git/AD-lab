from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import ollama
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins



# Function to scrape data from a URL
def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract relevant data (e.g., paragraphs)
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])
        return text
    except Exception as e:
        return str(e)

# Function to summarize text using LLM (Ollama)
def summarize_text(text):
    try:
        # Use Ollama for summarization
        response = ollama.generate(
            model="llama2",  # Use the Llama 2 model
            prompt=f"Summarize the following text:\n\n{text}"
        )
        return response["response"]
    except Exception as e:
        return str(e)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scrape", methods=["POST"])  # Ensure this is a list of strings
def scrape():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Step 1: Scrape the website
    scraped_text = scrape_website(url)

    # Step 2: Summarize the scraped text using LLM
    summary = summarize_text(scraped_text)

    return jsonify({
        "scraped_text": scraped_text,
        "summary": summary
    })
if __name__ == "__main__":
    app.run(debug=True , port=5000)