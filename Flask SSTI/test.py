from flask import Flask,render_template,request
from markupsafe import escape


app=Flask(__name__)

app.secret_key="flag:H4_IT"

@app.route('/info')
def index():
    s=escape(request.values.get('me'))
    return render_template('1.html',arg=s)

app.run()

