#!/usr/bin/python


from validate.from_redcap_meta import validate_required, validate_range, validate_no_entry
from data.fetch_data_metadata import get_data, get_metadata, Metadata
from validate.dates import date_checks
from settings import Project
import argparse
from functools import reduce
from datetime import datetime
import pandas as pd
from projects.sample_project1.format import Error
from projects.sample_project1.conditions import non_rtss_non_required, hidden_rtss, hidden_cin
from projects.sample_project1.variables import ignore_records, dates_after_adm_before_discharge
from utils import format_missing
from conditions.metadata import branching_check, hidden_check
from projects.sample_project1.custom_checks import convulsions_range, fever_duration, history_illn, prior_treatment, vaccination_reactions, hiv_test, hiv_instay
import os
import multiprocessing as mp


''''import conditions'''
url = os.getenv("rtss_url_main")
token = os.getenv("rtss_token_main")
rtss = Project(url=url, id_var='id', date_var='date_today', token=token, project='rtss')


parser = argparse.ArgumentParser()
# group = parser.add_mutually_exclusive_group()
# group.add_argument("--verbose", action="store_true")
# group.add_argument("--quiet", action="store_true")
parser.add_argument("-sta", "--start",  help="this is the start date")
parser.add_argument("-sto", "--stop", help="this is the stop date")
# parser.add_argument("-ho","--hosp",  help=" this is the hospital id")
parser.add_argument("-o","--out",help=" this is where errors will be contained")
# args = parser.parse_args().__dict__
args = parser.parse_args(['--start=2019-05-07', '--stop=2019-07-02','--out=errors.csv']).__dict__

start = args.get('start', None)
stop = args.get('stop', None)
out = args.get("out", "Errors.csv")

'''get metadata'''
metadata = Metadata(get_metadata(rtss))

# metadata1 = Metadata(get_metadata(rtss))
# metadata2 = Metadata(get_metadata(rtss))
# metadata3 = Metadata(get_metadata(rtss))
# metadata4 = Metadata(get_metadata(rtss))
# metadata5 = Metadata(get_metadata(rtss))

'''get data'''
data = get_data(rtss, variables=metadata.get_variables(expand_checkbox=False), start="2019-09-20", stop="2019-09-20")
data = [row for row in data if row['id'] not in ignore_records]
data = [metadata.format_data(r) for r in data]
data_formatted = [format_missing(r) for r in data]


vars = [i for i in metadata.get_variables_without_description()]

required_vars = [i for i in metadata.get_variables(expand_checkbox=True)if metadata.get_is_required(i) is True]
# required_vars1 = [i for i in metadata1.get_variables(expand_checkbox=True)if metadata1.get_is_required(i)is True]
# required_vars2 = [i for i in metadata2.get_variables(expand_checkbox=True)if metadata2.get_is_required(i)is True]
# required_vars3 = [i for i in metadata3.get_variables(expand_checkbox=True)if metadata3.get_is_required(i)is True]
# required_vars4 = [i for i in metadata4.get_variables(expand_checkbox=True)if metadata4.get_is_required(i)is True]
# required_vars5 = [i for i in metadata5.get_variables(expand_checkbox=True)if metadata.get_is_required(i)is True]

range_vars = [i for i in metadata.get_variables(expand_checkbox=True) if metadata.get_valid_range(i) is not None]
# range_vars1 = [i for i in metadata1.get_variables(expand_checkbox=True) if metadata1.get_valid_range(i) is not None]
# range_vars2 = [i for i in metadata2.get_variables(expand_checkbox=True) if metadata2.get_valid_range(i) is not None]
# range_vars3 = [i for i in metadata3.get_variables(expand_checkbox=True) if metadata3.get_valid_range(i) is not None]
# range_vars4 = [i for i in metadata4.get_variables(expand_checkbox=True) if metadata4.get_valid_range(i) is not None]
# range_vars5 = [i for i in metadata5.get_variables(expand_checkbox=True) if metadata5.get_valid_range(i) is not None]

date_vars = [i for i in metadata.get_variables(expand_checkbox=True) if metadata.get_type(i) == 'date']

'''Run checks'''
error_formatter = Error(metadata=metadata)
general_errors = []

''' redcap's is_required'''
required_errors = []
for r in data:
    for v in required_vars:
        required_errors.append(validate_required(r, variable=v, metadata=metadata, formater=error_formatter, pre_checks=[branching_check, hidden_check,non_rtss_non_required, hidden_rtss, hidden_cin]))
general_errors.append(required_errors)



'''redcap range_validation'''
errors_range = []
for r in data_formatted:
    for v in range_vars:
        errors_range.append(validate_range(r, variable=v, metadata=metadata, formater=error_formatter, pre_checks=[branching_check, hidden_check]))
general_errors.append(errors_range)


# no_entry_errors = []
# for r in data:
#     for v in vars:
#         no_entry_errors.append(validate_no_entry(r, variable=v, metadata=metadata, formater=error_formatter, pre_checks=[branching_check, hidden_check]))
#         no_entry_errors = [s for s in no_entry_errors if s is not None]


'''check dates'''
'''dates that should come between admission and discharge'''
date1_errors = []
for r in data_formatted:
    for v in dates_after_adm_before_discharge:
        date1_errors.append(date_checks(r, variable=v, d1='date_adm', d2='date_discharge', formater=error_formatter, metadata=metadata))
general_errors.append(date1_errors)


'''dates after discharge'''
date2_errors = []
for r in data_formatted:
    for v in ['date_today']:
        date2_errors.append(date_checks(r, variable=v, d1='date_discharge', d2=None, formater=error_formatter, metadata=metadata))
general_errors.append(date2_errors)

'''dates that should come before admission:'''
date3_errors = []
for r in data_formatted:
    for v in ['dob','date_last_adm',]:
        date3_errors.append(date_checks(r, variable=v, d2='date_adm', metadata=metadata, formater=error_formatter, pre_checks=[branching_check, hidden_check]))
general_errors.append(date3_errors)


'''dates that come after discharge'''
date4_errors = []
for r in data_formatted:
    for v in ['date_today', ]:
        date4_errors.append(date_checks(r, variable=v, d1='date_discharge', metadata=metadata, formater=error_formatter))
general_errors.append(date4_errors)

'''custom checks'''
'''convulsion number'''
errors_convulsion_no = []
for r in data_formatted:
    for v in vars:
        errors_convulsion_no.append(convulsions_range(row=r, variable=v, metadata=metadata, formater=error_formatter, pre_checks=[branching_check, hidden_check,non_rtss_non_required, hidden_rtss, hidden_cin]))
general_errors.append(errors_convulsion_no)

'''fever duration'''
errors_fever_duration = []
for r in data_formatted:
    for v in vars:
        errors_fever_duration.append(fever_duration(row=r, variable=v, metadata=metadata, formater=error_formatter, pre_checks=[branching_check,hidden_check, non_rtss_non_required, hidden_rtss, hidden_cin]))
general_errors.append(errors_fever_duration)

'''History of illness'''
errors_history_illn = []
for r in data_formatted:
    for v in vars:
        errors_history_illn.append(history_illn(row=r, variable=v, metadata=metadata, formater=error_formatter, pre_checks=[branching_check, hidden_check, non_rtss_non_required, hidden_rtss,hidden_cin]))
general_errors.append(errors_history_illn)

'''History of treatment'''
errors_prior_treatment = []
for r in data_formatted:
    for v in vars:
        errors_prior_treatment.append(prior_treatment(row=r, variable=v, metadata=metadata, formater= error_formatter, pre_checks=[branching_check, hidden_check, non_rtss_non_required, hidden_cin, hidden_rtss]))
general_errors.append(errors_prior_treatment)

'''Vaccination reactions'''
errors_vaccination_reactions = []
for r in data_formatted:
    for v in vars:
        errors_vaccination_reactions.append(vaccination_reactions(row=r, variable=v, metadata=metadata, formater=error_formatter, pre_checks=[branching_check, hidden_check, hidden_cin, hidden_rtss, non_rtss_non_required]))
general_errors.append(errors_vaccination_reactions)

'''HIV Test'''
errors_hiv_test = []
for r in data_formatted:
    for v in vars:
        errors_hiv_test.append(hiv_test(row=r, variable=v, metadata=metadata, formater=error_formatter, pre_checks=[branching_check, hidden_check, hidden_rtss, hidden_cin, non_rtss_non_required]))
general_errors.append(errors_hiv_test)

'''HIV ordered during in stay'''
errors_hiv_instay = []
for r in data_formatted:
    for v in vars:
        errors_hiv_instay.append(hiv_instay(row=r, variable=v, metadata=metadata, formater=error_formatter, pre_checks=[branching_check, hidden_check,hidden_cin, hidden_rtss, non_rtss_non_required]))
general_errors.append(errors_hiv_instay)

general_errors = reduce(lambda x, y: x+y, general_errors)

general_errors = [x for x in general_errors if x != []]

general_errors = [ge for ge in general_errors if ge is not None]

general_errors = reduce(lambda x,y: x+y, general_errors)

ans = pd.DataFrame(general_errors)
ans.to_csv("Verification App (New).csv")




