import flask
from flask import render_template, Flask

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='заготовка')


@app.route('/training/<prof>')
def training(prof):
    return render_template('training.html', title=prof)


@app.route('/list_prof/<list>')
def list_prof(list):
    prof = (
        'инженер-исследователь', 'пилот', "строитель", 'экзобиолог', 'врач', 'инженер по терраформированию',
        'климатолог',
        'пециалист по радиационной защите', 'астрогеолог', 'гляциолог', 'инженер жизнеобеспечения', 'метеоролог',
        'оператор марсохода', 'киберинженер', 'штурман', 'пилот дронов')
    return render_template('list_prof.html', list=list, prof=prof)


@app.route('/answer')
@app.route('/auto_answer')
def auto_answer():
    pasrams = {'title': 'Анкета',
               "surname": "Сусвнин",
               "name": "Иван",
               "education": "4 класса",
               "profession": "экскурсовод",
               "sex": "м",
               "motivation": "всегда мечтал застрять на Марсе",
               'ready': 'всегда ready'}
    return render_template('auto_answer.html', **pasrams)


if __name__ == "__main__":
    app.run()
