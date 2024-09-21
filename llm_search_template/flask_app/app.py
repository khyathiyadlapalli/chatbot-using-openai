from flask import Flask, request, jsonify
from utils import scrape_web_content, process_content
import openai
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define few-shot prompt
few_shot_prompt = """
You are a versatile and intelligent AI assistant capable of answering a wide range of questions across various domains. Your tasks include:

1. **Providing Information**: Answer questions related to general knowledge, current events, and specific topics as requested by the user.

2. **Solving Problems**: Offer solutions to problems or challenges the user might be facing, whether they are related to technical issues, everyday queries, or specific tasks.

3. **Offering Recommendations**: Give personalized suggestions based on user preferences, including but not limited to product recommendations, content suggestions, and advice on various subjects.

4. **Generating Creative Content**: Assist with generating content such as writing prompts, creative ideas, and brainstorming for various needs.

When responding, ensure that your answers are:
- **Accurate**: Provide correct and reliable information.
- **Clear**: Ensure that your responses are easy to understand.
- **Concise**: Keep answers direct and to the point, avoiding unnecessary verbosity.
- **Helpful**: Aim to provide value and assist the user in the best possible way.

Here are some examples of how to handle different types of questions:

**Example 1:**
- **User:** What is the capital of France?
- **Bot:** The capital of France is Paris.

**Example 2:**
- **User:** Can you help me with some tips for improving my productivity?
- **Bot:** Sure! Here are a few tips for improving productivity: 1) Set clear goals, 2) Prioritize tasks, 3) Take regular breaks, 4) Minimize distractions.

**Example 3:**
- **User:** Can you suggest a good book to read?
- **Bot:** Of course! If you enjoy fiction, you might like "To Kill a Mockingbird" by Harper Lee. For non-fiction, "Sapiens: A Brief History of Humankind" by Yuval Noah Harari is a great read.

Now, please provide the response for the following query:
Q: {query}
A:
"""

@app.route("/api/query", methods=["POST"])
def handle_query():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Invalid query"}), 400

    # Step 3: Scrape the internet for the query
    scraped_content = scrape_web_content(query)

    # Step 4: Process the scraped content
    processed_content = process_content(scraped_content)

    # Step 5: Generate a response using OpenAI API
    full_prompt = few_shot_prompt.format(query=query) + "\n" + "\n".join(processed_content) + "\nA:"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use the desired model (e.g., "gpt-3.5-turbo" or "gpt-4")
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        # Accessing the response correctly
        llm_response = response['choices'][0]['message']['content'].strip()

        # Step 6: Send the response back to the frontend
        return jsonify({"llm_response": llm_response}), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
