
import excel2json

excel2json.convert_from_file('malattie.xlsx') 

import pandas

excel_data_df = pandas.read_excel('malattie.xlsx', sheet_name='malattie')

json_str = excel_data_df.to_json()

print('Excel Sheet to JSON:\n', json_str)