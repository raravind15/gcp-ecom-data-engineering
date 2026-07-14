from flask import Flask
from flask import request
from flask import jsonify

app=Flask(__name__)

# request_json=request.get_json(silent=True) or {}


@app.route("/")
def home():
    return {
        "Message":"App is running"
    }

@app.post("/student")

def add_student():
    request_json = request.get_json(silent=True) or {}
    Name=request_json.get("name")
    Age=request_json.get("age")
    
    return (jsonify(
        {
        "status":"Success",
        "message":"Student Added",
        "name":Name,
        "age":Age
        }
        ),200)



if __name__=="__main__":
    app.run(
        host="0.0.0.0",port=8080,debug=True
    )