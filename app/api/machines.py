from flask import jsonify, request, flash
from ..models import Cluster, Machine, Tag
from .. import db
from . import api


@api.route('/clusters/<int:cluster_id>/machines')
def get_machines(cluster_id):
    cluster = Cluster.query.filter_by(id=cluster_id).first_or_404()
    return jsonify({
        'machines': [machine.to_json() for machine in cluster.machines]
    })


@api.route('/clusters/<int:cluster_id>/machines', methods=['POST'])
def new_machine(cluster_id):
    cluster = Cluster.query.filter_by(id=cluster_id).first_or_404()
    machine = Machine.from_json(request.json)
    machine.set_cluster_id(cluster_id)
    db.session.add(machine)
    db.session.commit()
    return jsonify(machine.to_json()), 201


@api.route('/machines/<string:tag>')
def get_machines_by_tag(tag):
    tag = Tag.query.filter_by(name=tag.lower()).first_or_404()
    result = {
        'machines': [machine.to_json() for machine in tag.machine]
    }
    return jsonify(result)


@api.route('/machines/<string:tag>/start', methods=['POST'])
def start_machines(tag):
    tag = Tag.query.filter_by(name=tag.lower()).first_or_404()
    for machine in tag.machine:
        machine.start()
    db.session.commit()
    return {'message': 'Operation Successful.'}


@api.route('/machines/<string:tag>/stop', methods=['POST'])
def stop_machines(tag):
    tag = Tag.query.filter_by(name=tag.lower()).first_or_404()
    for machine in tag.machine:
        machine.stop()
    db.session.commit()
    return {'message': 'Operation Successful.'}


@api.route('/machines/<string:tag>/restart', methods=['POST'])
def restart_machines(tag):
    tag = Tag.query.filter_by(name=tag.lower()).first_or_404()
    for machine in tag.machine:
        machine.stop()
    db.session.commit()
    for machine in tag.machine:
        machine.start()
    db.session.commit()
    return {'message': 'Operation Successful.'}


@api.route('/machines/<string:tag>/delete', methods=['POST'])
def delete_machines(tag):
    tag = Tag.query.filter_by(name=tag.lower()).first_or_404()
    for machine in tag.machine:
        mach = db.session.query(Machine).filter(
            Machine.id == machine.id).first()
        db.session.delete(mach)
    db.session.commit()
    return {'message': 'Operation Successful.'}
