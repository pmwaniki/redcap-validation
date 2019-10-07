
def convulsions_range(row, variable, metadata, formater, pre_checks=[]):
    errors = []
    for fun in pre_checks:
        if fun(row, variable, metadata)== False:
            return errors
    if row['convulsions'] == 1:
        if row['convulsions_no'] <= 0:
            errors.append(formater(row, 'convulsions_no', error_type="Range check", message= "Number of convulsions is invalid!"))
    return errors


def fever_duration(row, variable, metadata, formater, pre_checks=[]):
    errors = []
    for fun in pre_checks:
        if fun(row, variable, metadata)==False:
            return errors
    if row['fever'] == 1:
        if row['fever_dur'] <= 0:
            errors.append(formater(row, 'fever_dur', error_type="Range check", message="Duration of fever is invalid!"))
        return errors

def history_illn(row, variable, metadata, formater, pre_checks=[]):
    errors=[]
    for fun in pre_checks:
        if fun(row, variable, metadata) == False:
            return errors
        if row['p_exist_illness']==1:
            if row['exist_illn_list'] is None:
                errors.append(formater(row,'exist_illn_list', error_type="Illness history", message="Existing illnesses is not specified!"))
            return errors

def prior_treatment(row, variable, metadata, formater, pre_checks=[]):
    errors=[]
    for fun in pre_checks:
        if fun(row, variable, metadata) == False:
            return errors
        if row['any_treat']==1:
            if row['exist_illn_list'] is None:
                errors.append(formater(row, 'exist_illn_list', error_type="Treatment history", message="List of drugs taken is missing!"))
            return errors

def vaccination_reactions(row, variable, metadata, formater, pre_checks=[]):
    errors=[]
    for fun in pre_checks:
        if fun(row, variable, metadata) == False:
            return errors
        if row['react_vaccn']==1:
            if row['recent_vaccn'] is None:
                errors.append(formater(row, 'recent_vaccn', error_type="Vaccine Reactions", message="Vaccines with reaction is not specified!"))
            return errors

def hiv_test(row, variable, metadata, formater, pre_checks=[]):
    errors=[]
    for fun in pre_checks:
        if fun(row, variable, metadata) == False:
            return errors
        if row['hiv1_order']==1:
            if row['hiv1_test'] is None:
                errors.append(formater(row, 'hiv1_test', error_type="HIV test", message="HIV test ordered is not specified!"))
            return errors

def hiv_instay(row, variable, metadata, formater, pre_checks=[]):
    errors=[]
    for fun in pre_checks:
        if fun(row, variable, metadata) == False:
            return errors
        if row['hiv_inpt_order']==1 and row['hiv1_order']==0:
            if row['hiv_inpt_test'] is None and row['hiv_inpt_result'] is None:
                errors.append(formater(row, 'hiv_inpt_order', error_type="HIV test instay", message="Other HIV test resutls orderd during inpatient stay is not specified!"))
            return errors





