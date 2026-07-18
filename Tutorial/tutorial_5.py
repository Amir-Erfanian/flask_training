from flask import Flask, request
from flask_login import current_user
from datetime import datetime
import random

app = Flask(__name__)

@app.route('/')
def home():
    return 'Home Page. Testing API...'


@app.route("/api/hello")
def api_hello():

    return {
        "message": "Hello World!"
    }
    
@app.route("/api/status")
def api_status():

    return {
        "status": "online",
        "version": "1.0",
        "framework": "Flask"
    }

# @app.route("/api/me")
# def api_me():

#     if current_user.is_authenticated:

#         return {

#             "logged_in": True,

#             "id": current_user.id,

#             "username": current_user.username,

#             "email": current_user.email

#         }

#     return {

#         "logged_in": False

#     }


@app.route("/api/time")
def api_time():

    now = datetime.now()

    return {

        "year": now.year,

        "month": now.month,

        "day": now.day,

        "hour": now.hour,

        "minute": now.minute,

        "second": now.second

    }
  
@app.route("/api/random")
def api_random():

    return {
        "number": random.randint(1, 100)
    }  
  
@app.route("/api/add")
def api_add():

    a = int(request.args.get("a", 0))

    b = int(request.args.get("b", 0))

    return {

        "a": a,

        "b": b,

        "result": a + b

    }
  
@app.route("/api/greet/<name>")
def greet(name):
    return {
        "message": f"Hello {name}!"
    }
  
  
    
if __name__ == '__main__':
    app.run(debug=True)
