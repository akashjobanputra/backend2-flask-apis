from . import db

machine_tags = db.Table('machine_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('machine_id', db.Integer, db.ForeignKey('machines.id'))
)

class MachineState:
    ON = 1
    OFF = 2

class Cluster(db.Model):
    __tablename__ = 'clusters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    cloud_region = db.Column(db.String(50), nullable=False)
    # machines = db.relationship('Machine', backref='cluster', lazy='dynamic')
    machines = db.relationship('Machine', backref='cluster', lazy=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def to_json(self):
        cluster_details = {
            'id': self.id,
            'name': self.name,
            'cloud_region': self.cloud_region,
            'machines': [machine.to_json() for machine in self.machines]
        }
        return cluster_details

    @staticmethod
    def from_json(json_post):
        return Cluster(**json_post)
        # body = json_post.get('body')
        # if body is None or body == '':
        #     raise ValidationError('post does not have a body')


class Machine(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    instance_type = db.Column(db.String(50), nullable=False)
    cluster_id = db.Column(db.Integer, db.ForeignKey('clusters.id'))
    tags = db.relationship('Tag', backref='machine', lazy=True, secondary=machine_tags)
    state = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, **kwargs):
        super(Machine, self).__init__(**kwargs)
        if self.state is None:
            self.state = MachineState.ON
    
    def to_json(self):
        machine_details = {
            'id': self.id,
            'name': self.name,
            'ip_address': self.ip_address,
            'instance_type': self.instance_type,
            'tags': [str(tag) for tag in self.tags],
            'state': self.state,
            'cluster_id': self.cluster_id
        }
        return machine_details

    @staticmethod
    def from_json(json_post):
        tags = [Tag.get_or_create(tag) for tag in json_post['tags']]
        json_post['tags'] = tags
        json_post['ip_address'] = json_post['ip_address'].lower()
        json_post['instance_type'] = json_post['instance_type'].lower()
        return Machine(**json_post)

    def set_cluster_id(self, cluster_id):
        self.cluster_id = cluster_id
    
    def start(self):
        self.state = MachineState.ON

    def stop(self):
        self.state = MachineState.OFF


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    @classmethod
    def get_or_create(cls, tag_name):
        """Only add tags to the database that don't exist yet. If tag already
        exists return a reference to the tag otherwise a new instance"""
        tag = cls.query.filter(cls.name == tag_name.lower()).first()
        if not tag:
            tag = cls(name=tag_name.lower())
        return tag

    @staticmethod
    def from_json(json_post):
        return Tag(**json_post)

    @property
    def machine_count(self):
        """Return the number of posts with this tag"""
        return len(self.machine)

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'machine_count': self.machine_count}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name})>"