from flask import Flask, render_template, redirect, url_for, flash
from flask_redis import Redis
# from flask_restful import Resource, Api
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
import json

# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
# app.config['REDIS_HOST'] = '192.168.99.100'
# app.config['REDIS_PORT'] = 6379
# app.config['REDIS_DB'] = 0
redis = Redis(app)
redis.flushdb()


# api = Api(app)
#
#
# class AddNewList(Resource):
#
#     def get(self):
#         return {'status': 'ok'}
#
#
# api.add_resource(AddNewList, '/add_new_list')


# class ShowLists(Resource):
#
#     def get(self):
#         return {'lists': 'xxx'}
#
#
# api.add_resource(ShowLists, '/show_lists')


# Now create a WTForm Class
class InfoForm(FlaskForm):
    '''
    This general class gets a lot of form about puppies.
    Mainly a way to go through many of the WTForms Fields.
    '''
    add_list = StringField('Add new list: ', [validators.DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    # return render_template('base.html')

    # name = redis.get('name') or 'Hello'
    # listvalues = redis.get('listvalues') or 'World'

    #

    # return f"{name} -> {listvalues}"

    # Create instance of the form.

    # If the form is valid on submission (we'll talk about validation next)
    return render_template('base.html')


@app.route('/add_new_list', methods=['GET', 'POST'])
def add_new_list():
    status = ''

    form = InfoForm()

    if form.validate_on_submit():
        # listdata = {'new_item': form.add_list.data}

        # redis.execute_command('JSON.SET', 'lists', '.', json.dumps(listdata))
        # listvalues = json.loads(redis.execute_command('JSON.GET', 'lists'))

        try:
            redis.lpush('lists', form.add_list.data)
            status = json.dumps({'status': 'ok'})
            # return redirect(url_for('add_new_list'))
        except Exception:
            status = json.dumps({'status': 'error'})
            # return redirect(url_for('add_new_list'), code=500)

    form.add_list.data = ''
    return render_template('add_new_list.html', form=form, status=status)


@app.route('/show_lists')
def show_lists():
    try:
        lists = redis.lrange('lists', 0, -1)
        lists_strings = []
        for lst in lists:
            # lists_strings.append([lst.decode('utf-8')])
            lists_strings.append(lst.decode('utf-8'))

        if lists_strings:
            lists_json = json.dumps({'lists': lists_strings})
        else:
            lists_json = 'No lists to show'
    except Exception:
        lists_json = 'Error communicating with DB'

    return render_template('show_lists.html', lists_json=lists_json)


if __name__ == "main":
    app.run(debug=True)
