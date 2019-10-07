import json
import os
with open(os.path.join(os.environ['HOMEPATH'],"settings.json")) as f:
    tokens = json.load(f)


class Project:
    def __init__(self, url, id_var, date_var, token, project):
        self.url = url
        self.date_var = date_var
        self.id_var = id_var
        self.token = token
        self.project = project






cin = Project(url = "https://hsuweb.kemri-wellcome.org/redcap/api/", id_var = 'id', date_var = 'date_today', token = tokens['cin_token'], project = 'cin')