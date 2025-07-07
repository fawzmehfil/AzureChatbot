from flask import Flask, request, jsonify, send_from_directory
from openai import AzureOpenAI
import os
import pyodbc
from datetime import datetime

app = Flask(__name__, static_folder="static", static_url_path="")

# Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_ENDPOINT")
)
deployment = os.getenv("AZURE_DEPLOYMENT_NAME")

# SQL connection setup
server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
username = os.getenv("SQL_USERNAME")
password = os.getenv("SQL_PASSWORD")
driver = '{ODBC Driver 17 for SQL Server}'

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def get_history(session_id):
    try:
        conn = pyodbc.connect(conn_str, timeout=5)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT role, message FROM chat_history
            WHERE session_id = ?
            ORDER BY timestamp ASC
        """, (session_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{"role": row[0], "content": row[1]} for row in rows]
    except Exception as e:
        print("History Error:", e)
        return []

def save_message(session_id, role, content):
    try:
        conn = pyodbc.connect(conn_str, timeout=5)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chat_history (session_id, role, message, timestamp)
            VALUES (?, ?, ?, ?)
        """, (session_id, role, content, datetime.utcnow()))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Save Error:", e)

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")
        session_id = request.json.get("session_id", "default")

        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages += get_history(session_id)
        messages.append({"role": "user", "content": user_input})

        save_message(session_id, "user", user_input)

        response = client.chat.completions.create(
            model=deployment,
            messages=messages
        )
        reply = response.choices[0].message.content
        save_message(session_id, "assistant", reply)

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
