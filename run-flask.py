#! /usr/bin/env python

""" Put docstring here. """  # TODO

from flask import Flask, render_template, request, flash  # TODO - remove unused imports
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from elasticsearch_dsl.connections import connections

from vimeo_challenge.index import get_similar_clips, load_model


app = Flask(__name__)


class ReusableForm(Form):
    clip_id = TextField('Clip ID:')


@app.route('/', methods=['GET', 'POST'])
@app.route('/prompt', methods=['GET', 'POST'])
def prompt():
    form = ReusableForm(request.form)

    if request.method == 'POST':
        clip_id = form.clip_id.data
        return display(clip_id)

    return render_template('prompt.html', form=form)


@app.route('/display')
def display(clip_id):
    load_model(host='elasticsearch')
    connections.create_connection(hosts=['elasticsearch:9200'])
    similar_clips = get_similar_clips(clip_id)
    return render_template('display.html', clips=similar_clips)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
