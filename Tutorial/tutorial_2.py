from flask import Flask, url_for

app = Flask(__name__)

# Basic routes
@app.route('/')
def home():
    return '<h1>Home Page</h1>'

@app.route('/about')
def about():
    return '<h1>About Page</h1>'

# Dynamic routes with variables
@app.route('/user/<username>')
def user_profile(username):
    return f'<h1>Profile of {username}</h1>'

# With type converters
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'<h1>Post #{post_id}</h1>'


if __name__ == '__main__':
    app.run(debug=True)