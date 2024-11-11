from dataclasses import Field
from flask import Flask, request
from urllib.parse import unquote_plus
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length, NumberRange
import json
import subprocess

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


def number_length(min, max, message=None):
    if message is None:
        message = f"its lowe than{min} is {max}"

    def _number_length(form: FlaskForm, field: Field):
        number_str=str(field.data)
        if not (min <=len(number_str) <=max):
            raise ValidationError(message)
    
    return _number_length


class NumberLength:
    def __init__(self, min, max, message=None):
        self.min = min
        self.max = max
        self.message = message or f"its lower than {min} and {max}"

    def __call__(self, form: FlaskForm, field: Field):
        number_str=str(field.data)
        if not (self.min <= len(number_str) <=self.max):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    email=StringField()
    # phone=StringField('Phone Number', validators=[DataRequired(message="Phone number is required"),Length(min=10, max=10, message="Phone number should be 10 digits")])
    # phone=IntegerField('Phone Number', validators=[DataRequired(message="Phone number is required"),number_length(min=7, max=10)])
    phone=IntegerField('Phone Number', validators=[DataRequired(message="Phone number is required"),NumberLength(min=7, max=10)])
    
    address = StringField('Delivery Address', validators=[DataRequired(message="Delivery address is required")])
    name = StringField('Recipient Name', validators=[DataRequired(message="Recipient name is required")])
    index=IntegerField()
    comment=StringField()

@app.route("/reg", methods=["POST"])
def reg():
    form=RegistrationForm()

    if form.validate_on_submit():
        email, phone=form.email.data, form.phone.data

        # if len(str(form.phone.data)) <10:
        #     print(len(str(form.phone.data)))
        #     return "Phone number should be 10 digits", 400



        return f"Registration {email} {phone}"

    return f"not ok {form.errors}", 400


@app.route("/trip", methods=["POST"])
def trip():
    name = request.form['name']
    family_name = request.form['family_name']
    ticket_number = request.form['ticket_number']

    # Проверка, что все поля заполнены
    if not name or not family_name or not ticket_number:
        return "Все поля должны быть заполнены"

    # Проверка, что билет состоит из 6 цифр и первая цифра не 0
    if len(ticket_number) != 6 or not ticket_number.isdigit() or ticket_number[0] == '0':
        return "Номер билета должен состоять из 6 цифр, и первая цифра не может быть 0"

    # Проверка счастливого билета
    first_half = sum(int(x) for x in ticket_number[:3])
    second_half = sum(int(x) for x in ticket_number[3:])

    if first_half == second_half:
        return f"Поздравляем вас, {name} {family_name}!"
    else:
        return "Неудача. Попробуйте ещё раз!"



@app.route('/uptime', methods=['GET'])
def get_uptime():
    # Получаем результат выполнения команды uptime
    result = subprocess.run(['uptime', '-p'], capture_output=True, text=True)
    
    # Удаляем лишнюю информацию и передаём строку с временем работы
    uptime_info = result.stdout.strip()
    return f"Current uptime is {uptime_info}"


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"]=False
    app.run(debug=True)

 