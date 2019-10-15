from flask import jsonify, request
from ..models import Cluster
from .. import db
from . import api


@api.route('/clusters/', defaults={'cluster_id': None})
@api.route('/clusters/<int:cluster_id>/')
def get_clusters(cluster_id):
    """Returns all the clusters and their details or the cluster details of the ID provided.
    ---
    parameters:
        - name: cluster_id
          in: path
          type: number
          required: false
          default: None
    definitions:
        clusters:
            id: Clusters
            type: object
            properties:
                clusters:
                    type: array
                    items:
                        $ref: '#/definitions/cluster'
        cluster:
            type: object
            properties:
                id:
                    type: number
                name:
                    type: string
                cloud_region:
                    type: string
                machines:
                    type: array
                    items:
                        $ref: '#/definitions/machine'
        machine:
            type: object
            properties:
                id:
                    type: number
                cluster_id:
                    type: number
                name:
                    type: string
                instance_type:
                    type: string
                ip_address:
                    type: string
                state:
                    type: number
                machines:
                    type: array
                    items:
                        $ref: '#/definitions/tag'
        tag:
            type: string
    responses:
        200:
            description: A list of clusters (may be filtered by cluster_id)
            schema:
                $ref: '#/definitions/clusters'
            examples:
                clusters: [
                        {
                            "id": 1,
                            "name": "DevIN",
                            "cloud_region": "IND_MUM",
                            "machines": [
                                {
                                    "cluster_id": 1,
                                    "id": 1,
                                    "instance_type": "medium",
                                    "ip_address": "abcd:abcd:ce3a:abcd:cccc:abcd",
                                    "name": "DEV_CACHE_OPTIMIZER",
                                    "state": 1,
                                    "tags": [
                                        "dev",
                                        "ind",
                                        "cache"
                                    ]
                                },
                                {
                                    "cluster_id": 1,
                                    "id": 2,
                                    "instance_type": "small",
                                    "ip_address": "abcd:abcd:ce3a:abcd:cccc:73ab",
                                    "name": "DEV_NOTIFICATIONS",
                                    "state": 1,
                                    "tags": [
                                        "dev",
                                        "ind"
                                    ]
                                }
                            ]
                        }
                    ]
    """
    if cluster_id:
        clusters = Cluster.query.filter_by(id=cluster_id).first_or_404()
        response = {
            'cluster': clusters.to_json()
        }
    else:
        clusters = Cluster.query.all()
        response = {
            'clusters': [cluster.to_json() for cluster in clusters]
        }
    return jsonify(response)


@api.route('/clusters/', methods=['POST'])
def new_cluster():
    cluster = Cluster.from_json(request.json)
    db.session.add(cluster)
    db.session.commit()
    return jsonify(cluster.to_json()), 201
