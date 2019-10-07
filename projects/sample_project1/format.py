class Error:
    def __init__(self, metadata, date_today='date_today', id_var='id', ip_var='ipno', hosp_var='hosp_id'):
        self.metadata = metadata
        self.date_today = date_today
        self.id_var = id_var
        self.hosp_var = hosp_var
        self.ip_var = ip_var

    def __call__(self, row, variable, error_type, message):

        return {'RecordID': int(row[self.id_var]),
                'Identifier': row[self.ip_var],
                'DateOfEntry':  row[self.date_today],
                'Hospital': row[self.hosp_var],
                'Form': self.metadata.metadata_expanded[variable]['form_name'],
                'Section': self.metadata.metadata_expanded[variable]['section_header'],
                'Variable': variable,
                'Error_Type': error_type,
                'Entry': row[variable],
                'Message': message
                }
# self.metadata.get_variables()
# self=Error(metadata)
# y=[self(r,variable='diarrhoea_bloody',error_type="required",message="Hospital ID required")for r in data]
