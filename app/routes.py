from app import app, tasks
from flask import flash, redirect, render_template, request

from app.forms import SearchTermForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        form = SearchTermForm()
        return render_template('index.html', title='Twitter Sentiment Analysis on Raspberry', form=form)

    search_term = request.form['search_term']
    tasks.twitter_search.apply_async(args=[search_term], countdown=0)
    return redirect('/index')
