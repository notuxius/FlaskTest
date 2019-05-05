from flask import Flask, render_template
from flask_redis import Redis
from flask_restful import Resource, Api
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
import json

# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['REDIS_HOST'] = '192.168.99.100'
app.config['REDIS_PORT'] = 6379
app.config['REDIS_DB'] = 0
redis = Redis(app)
redis.flushdb()

api = Api(app)


class AddNewList(Resource):

    def get(self):
        return {'status': 'ok'}


api.add_resource(AddNewList, '/add_new_list')


class ShowLists(Resource):

    def get(self):
        return {'lists': 'xxx'}


api.add_resource(ShowLists, '/show_lists')


# Now create a WTForm Class
# Lots of fields available:
# http://wtforms.readthedocs.io/en/stable/fields.html
class InfoForm(FlaskForm):
    '''
    This general class gets a lot of form about puppies.
    Mainly a way to go through many of the WTForms Fields.
    '''
    listvalue = StringField('Value: ', [validators.DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():

    # return render_template('basic.html')

    # name = redis.get('name') or 'Hello'
    # listvalues = redis.get('listvalues') or 'World'

    #

    # return f"{name} -> {listvalues}"

    # Create instance of the form.
    form = InfoForm()
    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit():
        listdata = {'new_item': form.listvalue.data}

        redis.execute_command('JSON.SET', 'lists', '.', json.dumps(listdata))
        listvalues = json.loads(redis.execute_command('JSON.GET', 'lists'))

        # redis.lpush('lists', "{'new_item': %s }" % (form.listvalue.data))
        # listvalues = redis.lrange('lists', 0, -1)

        return render_template('basic.html', form=form, listvalues=listvalues)
    return render_template('basic.html', form=form)


if __name__ == "main":
    app.run(debug=True)
