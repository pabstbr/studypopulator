import os
import pystache
from flask import Flask, redirect, request, url_for
from . import dbi

app = Flask(__name__)

#Specifies the potential review statuses and allows mustache to handle specifiying what's selected in the dropdown
REVIEW_STATUSES = [
        {'value': 'not_review','text': 'Not Reviewed', 'selected': None},
        {'value': 'not_accepted','text': 'Reviewed - Not Accepted', 'selected': None},
        {'value': 'accepted','text': 'Reviewed - Accepted', 'selected': None}
    ]

@app.route('/new_participant')
def new_participant():
    """View for populating new participant information"""
    renderer = pystache.Renderer(search_dirs=os.path.join(app.root_path, 'templates/'))
    return renderer.render_path(os.path.join(app.root_path, 'templates/input_form.mustache'))

@app.route('/display/<participant_id>')
def display_participant(participant_id):
    """Query database for specific information on one participant

    Keyword Arguments:
    particpant_id -- the id of the participant
    """
    results = dbi.get_participants(participant_id)
    statuses = REVIEW_STATUSES

    for status in statuses:
        if status['value'] == results['reviewStatus']:
            status['selected'] = 'selected'

    renderer = pystache.Renderer(search_dirs=os.path.join(app.root_path, 'templates/'))
    return renderer.render_path(os.path.join(app.root_path, 'templates/participant.mustache'), {'participant': results, 'statuses': statuses})

@app.route('/')
@app.route('/display_all')
def display_all_participants():
    """Query the database for all participant info and display their base information
    If no participants are found go to the new_participant page
    """
    participants = dbi.get_participants()
    renderer = pystache.Renderer(search_dirs=os.path.join(app.root_path, 'templates/'))

    if participants is None:
        return redirect(url_for('new_participant'))

    return renderer.render_path(os.path.join(app.root_path, 'templates/all_participants.mustache'), participants = participants)

@app.route('/insert_participant', methods=['POST'])
def insert_participant():
    """Add a new participant into the participant table

    Keyword Arguments:
    name -- name of the new participant
    age -- age of the new participant
    HasSiblings -- whether the new participant has siblings
    EnvironmentExposure -- Environment exposure notes of the new participant
    GeneticMutation -- Known genetic mutations of the new participant
    """
    participant_name = request.form['name']
    participant_age = request.form['age']
    participant_siblings = 1 if request.form['HasSiblings'] == 'on' else 0
    participant_environment = request.form['EnvironmentalExposure']
    participant_genetic = request.form['GeneticMutation']

    dbi.insert_participant(participant_name, participant_age, participant_siblings, participant_environment, participant_genetic)

    return redirect(url_for('display_all_participants'))

@app.route('/update_review_status', methods=['POST'])
def update_review_status():
    """Update the review status of the participant

    Request Arguments:
    ReviewStatus -- Description of the participant's new review status
    id -- database table id for the participant
    """
    participant_id = request.form['id']
    participant_review_status = request.form['ReviewStatus']

    dbi.update_review_status(participant_review_status, participant_id)

    return redirect(request.referrer)

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database again at the end of the request."""
    dbi.close_connection(exception)

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    dbi.init_db()
    print('Initialized the database.')