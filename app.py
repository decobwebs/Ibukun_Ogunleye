from flask import Flask, render_template, send_from_directory
import os
import threading
import time
import requests

app = Flask(__name__)

# Define the directory where the file is stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Base directory of the app
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'static')  # Directory containing the PDF file

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/download-card")
def download_card():
    # Send the file to the client for download
    filename = "Ibukun_Ogunleye.zip"  # Replace with your actual file name
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

def keep_alive():
    """Periodically visit the website to keep it active."""
    url = "http://127.0.0.1:5001/"  # Replace with your website's public URL in production
    while True:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"Visited {url} successfully at {time.ctime()}")
            else:
                print(f"Failed to visit {url}. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error visiting {url}: {e}")
        time.sleep(720)  # Wait 12 minutes before the next request

if __name__ == "__main__":
    from waitress import serve

    # Start the keep_alive function in a background thread
    threading.Thread(target=keep_alive, daemon=True).start()

    # Uncomment this line for development
    app.run(debug=False, port=5001)
    # Uncomment this line for production
    # serve(app, host='0.0.0.0', port=5001)
