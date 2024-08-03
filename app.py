from flask import Flask, request
from urllib.parse import unquote_plus
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/search/', methods=['GET'])
def search():
    arr= request.args.getlist("cell")
    if not arr:
        return "No input provided", 400

    return arr


@app.route('/array', methods=['POST'])
def show_arr():
    arr= request.form.getlist("arr")
    if not arr:
        return "No input provided", 400
    arr=[int(x) for x in arr]
    print(arr)
    return f"this is {arr}"


@app.route('/array2', methods=['POST'])
def show_arr2():
    arr= request.get_data(as_text=True)
    if not arr:
        return "No input provided", 400
    # arr=[int(x) for x in arr]
    arr=unquote_plus(arr)
    print(arr)
    return f"this is {arr}"


@app.route('/array3', methods=['POST'])
def show_arr3():
    arr=request.get_data(as_text=True)

    arr = json.loads(arr)
    result = arr["arr"]

    return f"this is {result}"


class RegistrationForm(FlaskForm):
    email=StringField()
    phone=StringField('Phone Number', validators=[DataRequired(message="Phone number is required"),Length(min=10, max=10, message="Phone number should be 10 digits")])
    address = StringField('Delivery Address', validators=[DataRequired(message="Delivery address is required")])
    name = StringField('Recipient Name', validators=[DataRequired(message="Recipient name is required")])
    index=IntegerField()
    comment=StringField()

@app.route("/reg", methods=["POST"])
def reg():
    form=RegistrationForm()

    if form.validate_on_submit():
        email, phone=form.email.data, form.phone.data

        if len(str(form.phone.data)) <10:
            return "Phone number should be 10 digits", 400



        return f"Registration {email} {phone}"

    return f"not ok {form.errors}", 400


@app.route("/trip", methods=["POST"])
def trip():
    return "f"



if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"]=False
    app.run(debug=True)

