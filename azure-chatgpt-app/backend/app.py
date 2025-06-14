from flask import Flask, request, jsonify, send_from_directory, session
from openai import AzureOpenAI
import os

app = Flask(__name__, static_folder="static", static_url_path="")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-key")  # Required for session handling

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_ENDPOINT")
)

deployment = os.getenv("AZURE_DEPLOYMENT_NAME")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")
        if "history" not in session:
            session["history"] = [{"role": "system", "content": "You are a helpful assistant."}]
        
        # Append user message
        session["history"].append({"role": "user", "content": user_input})

        # Send full conversation
        response = client.chat.completions.create(
            model=deployment,
            messages=session["history"]
        )

        reply = response.choices[0].message.content
        session["history"].append({"role": "assistant", "content": reply})

        return jsonify({"reply": reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/api/reset", methods=["POST"])
def reset_history():
    session.pop("history", None)
    return jsonify({"message": "Conversation reset."})

@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)


"""
from flask import Flask, request, jsonify, send_from_directory
from openai import AzureOpenAI
import os

app = Flask(__name__, static_folder="static", static_url_path="")

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_ENDPOINT")
)

deployment = os.getenv("AZURE_DEPLOYMENT_NAME")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
"""