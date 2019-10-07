import requests
import json
import pandas as pd
from datetime import datetime
from settings import Project
import os


# gets data from redcap
def get_data(project, start=None, stop=None,variables=None):
    """
    :param project: A project object
    :param start: start date eg '2009-01-01'. leave None for beginning of study
    :param stop: stop date eg '2009-01-02'. leave None for latest input
    :param variables:
    :return:
    """


    data = {
        'token': project.token,
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'fields[0]': project.id_var,
        'fields[1]': project.date_var,
        #'record[]': outputTwo(),
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }

    request = requests.post(project.url, data=data, verify=False)
    data = json.loads(request.text)
    data2 = pd.DataFrame(data)
    data2[project.date_var] = pd.to_datetime(data2[project.date_var])

    if start is not None:
        data2 = data2.loc[data2[project.date_var] >= pd.to_datetime(start), :]

    if stop is not None:
        data2 = data2.loc[data2[project.date_var] <= pd.to_datetime(stop), :]

    # print(data2)
    if data2.shape[0] == 0:
        return []

    x = {}

    for i, j in enumerate(data2[project.id_var]):
        x["records[{}]".format(i)] = '{}'.format(j)

    data = {
        'token': project.token,
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }

    for k, v in x.items():
        data[k] = v

    if variables is not None:
        for i,v in enumerate(variables):
            data[f'fields[{i}]'] = v

    request = requests. post(project.url, data=data, verify=False)
    data = json.loads(request.text)

    # for u in data:
    #     u.pop("biodata_complete")
    #     u.pop("history_complete")
    #     u.pop("immunization_history_complete")
    #     u.pop("examination_complete")
    #     u.pop("investigations_complete")
    #     u.pop("admission_diagnosis_complete")
    #     u.pop("treatment_complete")
    #     u.pop("supportive_care_complete")
    #     u.pop("monitoring_complete")
    #     u.pop("discharge_information_complete")
    return data


# trial_data = get_data(project=rtss,variables=['ipno','date_today'])

# class Data:
#     def __init__(self, data):
#         self.data = data
#         self.records = {v['record_id']:v for v in self.data}
#
#     def exists(self, record):
#         result = record in self.records.keys()
#         return result
#
#     def get_id(self, record):
#         if not self.exists(record):
#             raise Exception("Variable {} does not exist".format(record))
#         label =self.records[record]['record_id']
#         return label
#
#     def get_valid_date_range(self, record):
#         if not self.exists(record):
#             raise Exception("Variable {} does not exist".format(record))
#         date1 = self.records[record]['date_adm']
#         today_date = self.records[record]['date_today']
#         date1 = None if min == '' else datetime.strptime(date1,'%Y-%m-%d').date()
#         today_date = None if max == '' else datetime.strptime(today_date,'%Y-%m-%d').date()
#         range = None
#         if (date1 is not None) | (today_date is not None): range = (date1, today_date)
#
#         return range

# def check_dates(row,date1,date2,dates_before_adm,dates_after_adm,dates_before_,date_missing="2000-01-01"):

    # checks date adm<other dates
    # :param row:
    # :return:

    # errors=[]

# check_dates(row,"date_adm","date_dsc",["date_pres1","date_pres2"],["date_pres1","date_pres2"])
#
# self1=Data(get_data(rtss))
# o=self1.get_valid_date_range('7600306')
# #print(data2[[]])

# gets metadata from redcap


def get_metadata(project):
    """

    :param project: project object
    :returns: metadata
    """
    data1 = {
        'token': project.token,
        'content': 'metadata',
        'format': 'json',
        'returnFormat': 'json'
    }

    request1 = requests.post(project.url, data=data1, verify=False)
    data1 = json.loads(request1.text)
    return data1



class Metadata:

    def __init__(self, metadata):
        self.metadata = metadata
        self.vars_expanded = []
        self.vars_non_expanded = []
        self.metadata_expanded = {}
        self.metadata_non_expanded = {}
        for v in metadata:
            self.vars_non_expanded.append(v['field_name'])
            self.metadata_non_expanded[v['field_name']] = v
            if v['field_type'] == 'checkbox':
                t = v['select_choices_or_calculations']
                t2 = t.split("|")
                t3 = list(map(lambda x: x.split(",")[0], t2))
                t3b=[str.strip(i) for i in t3]
                t4 = [v['field_name'] + "___" + i for i in t3b]
                t5 = [i.replace("-", "_") for i in t4]
                self.vars_expanded = self.vars_expanded+t5
                for v2 in t5:
                    self.metadata_expanded[v2] = v

            else:
                self.vars_expanded.append(v['field_name'])
                self.metadata_expanded[v['field_name']] = v

            # self.variables={v['field_name']: v for v in self.metadata}
            # self.vars_non_expanded=list(self.variables.keys())


    def exists(self, variable):
        """

        :param variable: variable
        :return: True or False depending on whether the variable exists in the metadata
        """
        result = variable in (self.vars_expanded + self.vars_non_expanded)
        return result

    def get_variables(self, expand_checkbox=True):
        """
        :param expand_checkbox: if true the function returns expanded variables and vice versa
        :return:
        """
        if expand_checkbox:
            return self.vars_expanded
        else:
            return self.vars_non_expanded

    def get_variables_without_description(self):
        """
        :return: variables which
        """
        variables = self.get_variables(expand_checkbox=True)
        for variable in variables:
            if self.metadata_expanded[variable]['field_type'] == 'descriptive':
                variables.remove(variable)
        return variables

    def get_label(self, variable):
        """
               :param variable: variable
               :return: the label of the variable
        """
        if not self.exists(variable):
            raise Exception("Variable {} does not exist".format(variable))
        label=self.metadata_expanded[variable]['field_label']
        return label

    def get_type(self, variable):
        """
               :param variable: variable
               :return: the type of the data in the variable
        """
        if not self.exists(variable):
            raise Exception("Variable {} does not exist".format(variable))
        type_=self.metadata_expanded[variable]['text_validation_type_or_show_slider_number']
        v_type='str'
        if type_ == '':
            v_type = 'str'
        elif 'date' in type_:
            v_type = 'date'
        elif type_ == "number":
            v_type = 'float'
        elif type_ == 'integer':
            v_type = 'int'

        return v_type

    def get_valid_range(self, variable):

        """
               :param variable: variable
               :return: the range of the given variable
        """
        if not self.exists(variable):
            raise Exception("Variable {} does not exist".format(variable))
        min = self.metadata_expanded[variable]['text_validation_min']
        if min == '':
            min=None
        else:
            type_=self.get_type(variable)
            if type_ == 'float':
                min=float(min)
            elif type_ == 'date':
                min=datetime.strptime(min,'%Y-%m-%d')
            elif type_ == 'int':
                min = int(min)

        max = self.metadata_expanded[variable]['text_validation_max']
        if max == '':
            max=None
        else:
            type_ = self.get_type(variable)
            if type_ == 'float':
                max = float(max)
            elif type_ == 'date':
                max = datetime.strptime(max, '%Y-%m-%d')
            elif type_ == 'int':
                max = int(max)

        range=None
        if (min is not None) | (max is not None): range = (min, max)
        return range

    def get_is_required(self,variable):
        """
               :param variable: variable
               :return: true or false depending on whether a variable is required or not
        """
        if not self.exists(variable):
            raise Exception("Variable {} does not exist".format(variable))
        required = self.metadata_expanded[variable]['required_field']
        if required == '': required = False
        else: required = True
        return required

    def get_choices(self, variable):
        if not self.exists(variable):
            raise Exception("Variable {} does not exist".format(variable))
        choice = self.metadata_expanded[variable]['select_choices_or_calculations']
        choices = dict(item.split(",") for item in choice.split("|"))

        return choices

    def get_branching_logic(self, variable):
        """
        :param variable: variable
        :return: the branching logic of the variable
        """
        if not self.exists(variable):
            raise Exception("Variable {} does not exist".format(variable))
        logic = self.metadata_expanded[variable]['branching_logic']
        if logic == '':
            logic2 = None
        else:
            logic2 = logic
        return logic2

    def get_hidden(self, variable):
        """
               :param variable: variable
               :returns: true or false whether the variable is hidden or not
        """
        if not self.exists(variable):
            raise Exception("Variable {} does not exist".format(variable))
        hidden = self.metadata_expanded[variable]['field_annotation']
        if hidden == '':
            return False
        elif '@HIDDEN' in hidden:
            return True
        else:
            return False

    def format_data(self, row=None, labels=False):
        # for key, value in row.items():
        #     if not self.exists(key):
        #         raise Exception("Variable {} does not exist".format(key))
        """
               :param variable: row
               :return: a row whose values have been converted to their respective types
        """
        new_row = {}
        for variable, value in row.items():
            if value == '':
                new_row[variable] = None
                continue
            type_ = self.get_type(variable=variable)
            if type_ == 'str':
                new_row[variable] = value
            elif type_ == 'float':
                new_row[variable] = float(value)
            elif type_ == 'int':
                new_row[variable] = int(value)
            elif type_ == 'date':
                new_row[variable] = datetime.strptime(value, '%Y-%m-%d')
        return new_row








        # formatted_data = row[variable]
        # if self.get_type(variable) is not None:
        #     if row[variable] == '':
        #         formatted_data = None
        #     else:
        #         formatted_data = row[variable]
        #     if self.get_type(variable) == "integer":
        #         if formatted_data is not None:
        #             formatted_data = int(row[variable])
        #             # formatted_data2 = [s for s in formatted_data if s is not None]
        #     if self.get_type(variable) == "date_ymd":
        #         if formatted_data is not None:
        #             formatted_data = datetime.strptime(row[variable], '%Y-%m-%d')
        #             # formatted_data2 = [s for s in formatted_data if s is not None]
        #     if self.get_type(variable) == "number":
        #         if formatted_data is not None:
        #             formatted_data = float(row[variable])
        #             # formatted_data2 = [s for s in formatted_data if s is not None]
        # return formatted_data




if __name__=='__main__':
    self = Metadata(get_metadata(rtss))
    self.get_label('id')
    self.get_valid_range('w_cell_count')
    self.get_is_required('w_cell_count')
    self.get_branching_logic('random')
    self.get_choices('subcounty_county')
    self.get_valid_range('w_cell_count')
    [self.get_hidden(f) for f in self.get_variables(expand_checkbox=True)]
    [self.format_data(r,'age_days')for r in trial_data]


