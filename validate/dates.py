
# 1.dob
# 2.immunization_dates
# 3.rtss_vaccine_dates
# 4.date_last_adm
# 5.date_adm
# 6.treatment_dates
# 7.date_discharge
import pandas as pd


def date_checks(row, variable, d1=None, d2=None, formater=None, metadata=None, error_text="Date out of range", pre_checks=[]):
    errors = []
    for fun in pre_checks:
        if fun(row,variable,metadata)==False:
            return errors
    errors2 = []
    if row[variable] is None:
        return errors

    if (d1 is not None):
        if (row[d1] is not None):
            if row[variable] < row[d1]:
                errors.append(formater(row, variable=variable, error_type=error_text, message="{} should come after {}".format(metadata.get_label(variable), metadata.get_label(d1))))

    if (d2 is not None):
        if (row[d2] is not None):
            if row[variable] > row[d2]:
                errors.append(formater(row, variable=variable, error_type=error_text, message="{} should come before {}".format(metadata.get_label(variable), metadata.get_label(d2))))

    for i in errors:
        if type(i) == list:
            if len(i) > 0:
                errors2.append(i)
        else:
            errors2.append(i)

    return errors2


# metadata = Metadata(get_metadata(rtss))
# data = get_data(project = rtss, variables=metadata.get_variables(expand_checkbox=False), start="2019-08-14", stop="2019-08-14")
# data = [metadata.format_data(r) for r in data]
# formater = Error(metadata)
# data_formatted = [format_missing(r) for r in data]
# g = []
# for r in data_formatted:
#     for v in [date_vars]:
#         g.append(date_checks(r, variable='date_today', d1='date_adm', d2='date_discharge', formater=formater, metadata=metadata, error_text="Dates between admission and discharge"))
# # g = [date_checks(r,variable=v, d1='date_adm', d2='date_discharge',formater=formater, metadata=metadata)for r in data_formatted]
# g2 = [f for f in g if f is not None]
# g2 = reduce(lambda x, y: x+y, g2)
# g3=pd.DataFrame(g2)
# g3.to_csv("date1 errors.csv")

