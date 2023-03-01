import sqlite3

import flask
from flask import jsonify, request

from data import db_session
from data import jobs
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'team_leader_relation.email', 'job', 'work_size'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/job/<int:news_id>')
def get_one_job(job_id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).get(job_id)
    if not news:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': news.to_dict(only=(
                'id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished',
                'team_leader_relation.id',
                'team_leader_relation.email', 'team_leader_relation.name', 'team_leader_relation.surname'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def add_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if request.json.get('id'):
        job = db_sess.query(Jobs).get(request.json.get('id'))
        if job:
            return jsonify({'error': ' Id already exists'})
    job = Jobs(**request.json)
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})
