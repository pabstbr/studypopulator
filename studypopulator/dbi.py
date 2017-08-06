import sqlite3
from flask import g

DATABASE = './participant.db'

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = dict_factory
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db

def close_connection(exception):
    """Closes the database again at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Creates the database from the schema file"""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def dict_factory(cursor, row):
    """Factory to translate sqlite query results into dicts for mustache"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def insert_participant(participant_name, participant_age, participant_siblings, participant_environment, participant_genetic):
    """Adds a new participant to the database

    Keyword Arguments:
    participant_name -- name of the new participant
    participant_age -- age of the new participant
    participant_siblings -- whether the new participant has siblings
    participant_environment -- Environment exposure notes of the new participant
    participant_genetic -- Known genetic mutations of the new participant
    """
    db = get_db()

    db.cursor().execute('''
        INSERT INTO
        participant (name, age, hasSibling, environmentalExposure, geneticMutation)
        VALUES (?, ?, ?, ?, ?)
        ''', (participant_name, participant_age, participant_siblings, participant_environment, participant_genetic))
    db.commit()

def update_review_status(participant_review_status, participant_id):
    """Set a participant's review status

    Keyword Arguments:
    participant_review_status -- Description of the participant's new review status
    participant_id -- database table id for the participant
    """
    db = get_db()

    db.cursor().execute('''
        UPDATE
            participant
        SET
            reviewStatus = ?
        WHERE
            id = ?
        ''', (participant_review_status, participant_id))
    db.commit()

def get_participants(participant_id=None):
    """Return a list of participants, or a single participant if their ID is specified

    Keyword Arguments:
    participant_id -- database table id for the participant (default None)
    """
    db = get_db()
    cursor = db.cursor()
    if participant_id is None:
        cursor.execute('''
            SELECT
                id, name, age, reviewStatus
            FROM 
                participant
            ORDER BY
                name ASC
            ''')
        return cursor.fetchall()
    else:
        cursor.execute('''
            SELECT
                id, name, age, hasSibling, environmentalExposure, geneticMutation, reviewStatus
            FROM 
                participant
            WHERE
                id = ?
            ''', (participant_id))
        return cursor.fetchone()