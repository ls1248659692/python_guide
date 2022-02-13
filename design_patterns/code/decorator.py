from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello, World'

@app.route('/home')
def home():
	return 'Welcome Home'


from functools import wraps


def debug(f):
	@wraps(f)
	def debug_function(*args, **kwargs):
		print('call: ', f.__name__, args, kwargs)
		ret = f(*args, **kwargs)
		print('return: ', ret)
	return debug_function


@debug
def foo(a, b, c=None):
	print(a, b, c)
	return True


if __name__ == '__main__':
	foo(1, 2, 3)
	app.run()
