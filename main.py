import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Get API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

chat_sessions = {}  # Dictionary to store chat sessions per user

@app.route('/ask', methods=['GET'])
def ask():
    query = request.args.get('q')
    user_id = request.args.get('id')

    if not query or not user_id:
        return jsonify({"error": "Please provide both query and id parameters."}), 400

    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])

    chat_session = chat_sessions[user_id]
    response = chat_session.send_message(query)
    return jsonify({"response": response.text})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the uploaded file to a temporary location
    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)
    
    # Upload the file to Generative AI service
    sample_file = genai.upload_file(path=file_path, display_name=file.filename)
    file_uri = sample_file.uri
    
    # Analyze the uploaded file (assuming there is a function or method for image analysis)
    analysis_result = analyze_image(file_uri)
    
    return jsonify({"file_uri": file_uri, "analysis_result": analysis_result})

def analyze_image(file_uri):
    # This is a placeholder function. Replace it with the actual method to analyze the image.
    # You might need to use another API endpoint or a different function provided by the Generative AI service.
    return "Analysis of the image will be done here."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
