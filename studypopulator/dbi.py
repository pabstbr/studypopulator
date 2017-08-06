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
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def insert_participant(participant_name, participant_age, participant_siblings, participant_environment, participant_genetic):
    db = get_db()

    db.cursor().execute('''
        INSERT INTO
        participant (name, age, hasSibling, environmentalExposure, geneticMutation)
        VALUES (?, ?, ?, ?, ?)
        ''', (participant_name, participant_age, participant_siblings, participant_environment, participant_genetic))
    db.commit()

def update_review_status(participant_review_status, participant_id):
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
    db = get_db()
    cursor = db.cursor()
    if participant_id is None:
        cursor.execute('''
            SELECT
                *
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

def tester():
    print('test test')