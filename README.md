# Help for validation module


## Project object
For one to create an object of a project, the user must first set the url and the token as environmental variables
to avoid displaying the token in the scripts. 


For example:
```
url=os.getenv("rtss_url_main")
token=os.getenv("rtss_token_main")
```
Thereafter the user can create the object as shown:
```
rtss=Project(url=url, id_var='id', date_var='date_today', token=token, project='rtss')
```

## Fetch data and metadata
To fetch data, one ought to specify the project, date range and variables for which they want to obtain the data e.g.

```
data=get_data(project, start='2018-12-16', stop='2019-06-06',variables=None)
metadata_csv=get_metadata(project)
```

## Metadata class
The metadata class has functions for manipulating the metadata as shown below: 

This is how to create an instance of the metadata class:
```
metadata = Metadata(get_metadata(rtss))
```

### metadata.get_variables(variable)
The function can return two lists of variables:
i)returns all the variables including the ones in the checkboxes
```
metadata.get_variables(expand_checkbox = True)
```
ii)returns all the variables but excludes the variables in the checkboxes
```
metadata.get_variables(expand_checkbox = False)
```

### metadata.get_is_required(variable)
The function takes a variable and returns True or False depending on whether the variable is required or not.

For instance:
```
metadata.get_is_required('id')
out:True
```

where as:
```
metadata.get_is_required('hosp_id')
out:False
```

### metadata.get_branching_logic(variable)
The function takes a variable and returns the branching logic of the variable.

This is how the function is called:
```
metadata.get_branching_logic('random')
out: ([hosp_id] = '51' and  [hosp_id] = '53') and ([leave_period] = '0')
```

### metadata.format_data(row)
The function takes a row and converts its values to its respective types.

e.g.
```
metadata.format(row={'id': 45625545, 'hosp_discharge_summ': '1',
                    'date_today': '2019-05-18', 'age_days': ''})
out: {'id': 45625545,
 'disch_death_summ': '1',
 'date_today': datetime.datetime(2019, 5, 18, 0, 0),
 'age_days': None}
```

### format_missing data
The function takes a row and returns *None* for variables in the row whose values are empty or date variables whose values are less than or equal to '1915-01-01'.

e.g.
```
format_missing(row={'id': 45625545, 'hosp_discharge_summ': '1', 
'date_today': '1913-01-01', 'age_days': ''}) 
```


# Pre-checks
These are conditions that have to be met before validation is done.

### branching logic
This function first evaluates the branching logic, returning True or False. If False, there won't be need to proceed to validation.

For instance:
```
branching_check(row,variable='random',metadata)
out:False
``` 
whereas:
```
branching_check(row,variable='location',metadata)
out:True
```
### hidden
This function checks whether the variable is hidden or not. If hidden, validation will not take place.


```
hidden_check(row,variable='date_today',metadata)
out: True
```
whereas:
```
hidden_check(row,variable='subcounty',metadata)
out: False
```
It is applied while calling the main validation functions as shown.
```
validate_range (row,
        variable='oxygen_sat', 
        metadata=metadata,
        pre_checks=[branching_check, *hidden_check*,
        non_rtss_non_required,hidden_rtss,hidden_cin],
        formater=error_formatter)
```
# Validation
Validation has three functions as shown below:

### *_validate_required()_*
The function returns a list of records whose variables are required but have no values.
```
validate_required(row,
        variable='leave_period',
        metadata=metadata,
        pre_checks=[branching_check, hidden_check],
        formater=error_formatter)
```

### _*validate_range()*_
The function returns a list of records whose data is out of range.

```
validate_range(row,
        variable='oxygen_sat', 
        metadata=metadata,
        pre_checks=[branching_check,
        hidden_check,
        non_rtss_non_required,
        hidden_rtss,hidden_cin],
        formater=error_formatter)
```

### _*date_checks()*_
The function returns a list of records whose date variables are not consistent.

e.g. the function below checks that the date variables that are supposed to be between admission and discharge dates are consistent and therefore returns a list of dates that are out of admission and discharge date range.
```
date_checks (row, 
            variable='date_lp_done',
            d1='date_adm',
            d2='date_discharge',
            pre_checks[branching_check,
            hidden_check,
            non_rtss_non_required,
            hidden_rtss,hidden_cin],
            formater=error_formatter)
```












