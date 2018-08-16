#! /usr/bin/env python

""" Put docstring here. """  # TODO

from flask import Flask, render_template, request, flash
from wtforms import Form, TextField
from elasticsearch_dsl.connections import connections

from vimeo_challenge.index import get_similar_clips, load_model, get_clip_by_id


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '12345'


class ReusableForm(Form):
    clip_id = TextField('Clip ID:')


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def prompt():
    """ Display page prompting for clip ID. """
    form = ReusableForm(request.form)
    connections.create_connection(hosts=['elasticsearch:9200'])

    if request.method == 'POST':
        clip_id = form.clip_id.data
        clip = get_clip_by_id(clip_id)
        if clip is not None:
            similar_clips = get_similar_clips(clip_id)
            return render_template('index.html', form=form, clips=similar_clips)
        else:
            flash('Clip ID not found. Please enter a new clip ID.')

    return render_template('index.html', form=form, clips=[])


def setup():
    """ Restore ES snapshot before using web app. """
    load_model(host='elasticsearch')


app.before_first_request(setup)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
