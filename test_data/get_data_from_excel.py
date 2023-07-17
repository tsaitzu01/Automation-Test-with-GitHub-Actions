import pandas as pd
import logging

class GetDataFromExcel:
    
    def read_check_with_invalid_value(sheet_name):

        def replace_chars_with_asterisks(value):
            if isinstance(value, str) and value.endswith(' chars'):
                number = int(value.split(' ')[0])
                asterisks = '*' * number
                return asterisks
            return value

        df = pd.read_excel('test_data/Stylish_TestCase.xlsx', sheet_name = sheet_name
                           , dtype={'Mobile': str, 'Security Code': str})
        
        df.fillna('', inplace = True)
        df = df.applymap(replace_chars_with_asterisks)
        data_list = df.to_dict('records')

        logging.info(data_list)

        return data_list