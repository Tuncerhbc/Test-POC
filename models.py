from app import db
from app import login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.apptime import get_time as get_ntp_time


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    admin = db.Column(db.Boolean())
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    auth_level = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_auth_level(self):
        return self.auth_level

    def set_auth_level(self, auth_level):
        self.auth_level = auth_level


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    controlDomain = db.Column(db.String(64), index=True, unique=False)
    hbcStandard = db.Column(db.String(128), index=True, unique=False)
    question = db.Column(db.String(256), index=True, unique=True)

    def __repr__(self):
        return '<Question {}>'.format(self.question)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    project_name = db.Column(db.String(64), unique=True, index=True)
    project_manager = db.Column(db.String(64))
    project_description = db.Column(db.String(140))

    def __repr__(self):
        return '{}'.format(self.project_name)


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    assessment_id = db.Column(db.Integer, index=True, unique=False)
    questionNumber = db.Column(db.Integer, index=True)
    questionText = db.Column(db.String(512), index=True)
    questionResponse = db.Column(db.String(512))
    controlID = db.Column(db.String(32))
    control_satisfied = db.Column(db.Boolean())
    security_risk = db.Column(db.String(128))
    impact = db.Column(db.Integer)
    likelihood = db.Column(db.Integer)
    riskscore = db.Column(db.Integer)
    risklevel = db.Column(db.String(64))
    comment = db.Column(db.String(140))

    def set_impact(self, impact):
        self.impact = impact

    def set_likelihood(self, likelihood):
        self.likelihood = likelihood

    def calculate_risk(self):
        if self.riskscore >= 6:
            self.risklevel = "HIGH"
        elif self.riskscore >= 3:
            self.risklevel = "MEDIUM"
        else:
            self.risklevel = "LOW"

    def __repr__(self):
        return '<Response: - {} - {} - {}> \n'.format(self.questionNumber, self.questionText, self.questionResponse)


class Assessments(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    appname = db.Column(db.String(128), index=True, unique=True)
    timestamp = db.Column(db.String(128), index=True, default=get_ntp_time(0))
    implementation_date = db.Column(db.String(64))
    project_name = db.Column(db.String(64), db.ForeignKey('project.project_name'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    application_type = db.Column(db.String(64),index=True)
    externally_developed = db.Column(db.String(64))
    external_facing = db.Column(db.String(64))
    data_sensitivity = db.Column(db.String(64))
    is_submitted = db.Column(db.Boolean(), default=False)

    risk_level = db.Column(db.String(64))
    criticality = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Assessment {}>'.format(self.appname)


class Evaluation(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    appname = db.Column(db.String(128), index=True, unique=True)
    app_id = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.String(128), index=True, default=get_ntp_time(0))
    username = db.Column(db.String(64), index=True)


class DataSensitivity(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), index=True)
    data_type = db.Column(db.String(64), index=True)
    data_details = db.Column(db.String(64))
# PCI
# Customer PII
# Employee PII
# Financial
# Other


class Banners(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('assessments.id'))
    appname = db.Column(db.String(128), index=True)
    banner = db.Column(db.String(128), index=True)



class Access(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    appname = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Dashboard(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
