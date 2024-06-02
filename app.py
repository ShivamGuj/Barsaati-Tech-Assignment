from flask import Flask, render_template, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run_script')
def run_script():
    # Run the Selenium script
    result = subprocess.run(['python', 'selenium_script.py'], capture_output=True, text=True)
    return jsonify(result.stdout)

if __name__ == "__main__":
    app.run(debug=True)
