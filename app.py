from flask import Flask, render_template

import bs_logic as bs
from forms import InputForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretsuperstar'


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def hello_world():
    form = InputForm()
    if form.city.data is None:
        return render_template('input.html', title='Input Data for Bikeshare', form=form)
    elif form.submit():
        df = bs.load_data(form.city.data, form.month.data, form.day_of_week.data)
        results = bs.render_result(df)
        return render_template('result.html', title='Results', results=results)
    else:
        return render_template('input.html', title='Input Data for Bikeshare', form=form)


if __name__ == '__main__':
    app.run(debug=True)
