from flask import Flask, request

app = Flask(__name__)

@app.route('/callback')
def callback():
	code = request.args.get('code')
	if code:
		return f"Authorization code: {code}"
	else:
		return "Authorization code not found!"

if __name__ == '__main__':
	app.run(port=8080)