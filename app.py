from flask import Flask, request

from crawling import fetch_all

app = Flask(__name__)


@app.route('/')
def crawling():
	data = fetch_all()
	return dict(data=data)


if __name__ == '__main__':
	app.run()
