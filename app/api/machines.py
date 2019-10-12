from flask import jsonify, request
from ..models import Cluster, Machine
from .. import db
from . import api

@api.route('/clusters/<int:cluster_id>/machines/')
def get_machines(cluster_id):
    cluster = Cluster.query.filter_by(id=cluster_id).first_or_404()
    return jsonify({
        'machines': [machine.to_json() for machine in cluster.machines]
    })

@api.route('/clusters/<int:cluster_id>/machines/', methods=['POST'])
def new_machine(cluster_id):
    cluster = Cluster.query.filter_by(id=cluster_id).first_or_404()
    machine = Machine.query.filter_by
    # machine_json = request.json
    # tags = [Tag(name=tag) for tag in request.json['tags']]

    machine = Machine.from_json(request.json)
    machine.set_cluster_id(cluster_id)
    db.session.add(machine)
    db.session.commit()
    return jsonify(machine.to_json()), 201
