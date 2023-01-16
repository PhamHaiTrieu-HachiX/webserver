from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)
# Index page
@app.route('/', methods=['POST', 'GET'])
def index():
  return render_template("index.html")

if __name__ == "__main__":
  # Only run debug=True in developement mode, not for Production
#   app.run(port=5000, host="0.0.0.0",debug=True)
  app.run()
