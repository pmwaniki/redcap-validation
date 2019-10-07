
from projects.sample_project1.variables import non_rtss_exclussion,rtss_hospitals

def non_rtss_non_required(row,variable,metadata):
    if (variable in non_rtss_exclussion) & (row['hosp_id'] not in rtss_hospitals):
        return False
    return True

def hidden_rtss(row,variable,metadata):
    if (row['hosp_id'] in rtss_hospitals) & (variable in ['acidotic__breathing','acidotic_breathing','leave_period', 'ref_hosp']):
        return False
    return True

def hidden_cin(row,variable,metadata):
    if (row['hosp_id'] not in rtss_hospitals) & (variable in ['hb1_test', 'gluc1_test', 'hb_units']):
        return False
    return True