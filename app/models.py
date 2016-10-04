from app import db
from app import app
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    fname = db.Column(db.String(128), index = True, unique = False)
    lname = db.Column(db.String(128), index = True, unique = False)

    username = db.Column(db.String(128), index = True, unique = True)
    password = db.Column(db.String(1024), index = True, unique = False)

    email = db.Column(db.String(128), index = True, unique = False)

    school = db.Column(db.String(128), index = True, unique = False)

    permissions = db.Column(db.String(1024), index = True, unique = False)

    registrations = db.relationship('Registration', backref='user', lazy = 'dynamic')

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)
        db.session.commit()

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def add_permission(self, permission):
        if not self.permissions[:-1] == ',':
            self.permissions += ','
        if not self.check_permission(permission):
            self.permissions += permission + ','
        db.session.commit()

    def remove_permission(self, permission):
        self.permissions = self.permissions.replace(permission + ',', ',')
        db.session.commit()

    def check_permission(self, permission):
        contains_permission = False
        for p in self.permissions.split(','):
            contains_permission = contains_permission or (p == permission)
        return contains_permission

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    num_teams = db.Column(db.String(2048), index = True, unique = False)
    teams = db.Column(db.String(2048), index = True, unique = False)
    judges = db.Column(db.String(2048), index = True, unique = False)

    tournament = db.Column(db.String(128), index = True, unique = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def add_team(self, team):
        if not self.teams[:-1] == ',':
            self.teams += ','
        self.teams += team + ','
        db.session.commit()

    def remove_team(self, team):
        self.teams = self.teams.replace(team + ',', '')
        db.session.commit()

    def add_judge(self, judge):
        if not self.judges[:-1] == ',':
            self.judges += ','
        self.judges += judge + ','
        db.session.commit()

    def remove_judge(self, judge):
        self.judges = self.judges.replace(judge + ',', '')
        db.session.commit()    
