from datetime import datetime


def format_missing(row, date_missing=datetime.strptime('1915-01-01', '%Y-%m-%d')):
        new_row = {}
        # for row in data:
        for variable, value in row.items():
            if value is None:
                new_row[variable] = None
            elif (type(value) == float) | (type(value) == int):
                if value == -1:
                    new_row[variable] = None
                else:
                    new_row[variable] = value
            elif type(value) == datetime:
                if value <= date_missing:
                    new_row[variable] = None
                else:
                    new_row[variable] = value
            else:
                new_row[variable] = value

        return new_row

# metadata=Metadata(get_metadata(rtss))
# data = get_data(rtss, variables=metadata.get_variables(expand_checkbox=False))
# data = [metadata.format_data(r) for r in data]
# row=data[162]
# data_formatted = [format_missing(row=r) for r in data]
# data = get_data(rtss)
# row = data[162]
# y = format_missing(row)
