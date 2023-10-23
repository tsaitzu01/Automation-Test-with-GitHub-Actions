import pandas as pd
import logging
import os

class GetDataFromExcel:
    
    def read_checkout_value(sheet_name):

        def replace_chars(value):
            if isinstance(value, str) and value.endswith(' chars'):
                number = int(value.split(' ')[0])
                asterisks = 'h' * number
                return asterisks
            return value

        df = pd.read_excel('test_data/Stylish_TestCase.xlsx', sheet_name = sheet_name
                           , dtype={'Mobile': str, 'Security Code': str})
        
        df.fillna('', inplace = True)
        df = df.applymap(replace_chars)
        data_list = df.to_dict('records')

        return data_list
    
    def read_create_product(sheet_name):

        def replace_chars(value):
            if isinstance(value, str) and value.endswith(' chars'):
                number = int(value.split(' ')[0])
                asterisks = 'h' * number
                return asterisks
            return value
        
        def split_column_value(value):
            return [item.strip() for item in value.split(',')]
        
        def update_select_all_value(value, all_list):
            if value == ['全選']:
                logging.info(value)
                return all_list
            else:
                logging.info(value)
                return value

        def update_image_value(value, image_path):
            if value == 'sample image':
                return image_path
            else:
                return value
    
        # Read Excel
        if 'API' in sheet_name:
            df = pd.read_excel('test_data/Stylish_TestCase.xlsx', sheet_name = sheet_name
                               , dtype={'ColorIDs': str})
        else:     
            df = pd.read_excel('test_data/Stylish_TestCase.xlsx', sheet_name = sheet_name)

        # Fill na with ''
        df.fillna('', inplace = True)

        # Replace '* chars' to numbers of characters
        df = df.applymap(replace_chars)

        # Replace '全選' to a list with all colors
        if 'API' in sheet_name:
            df['ColorIDs'] = df['ColorIDs'].apply(split_column_value)
        else:
            df['Colors'] = df['Colors'].apply(split_column_value)
            df['Colors'] = df['Colors'].apply(update_select_all_value, args=[['白色', '亮綠', '淺灰', '淺棕', '淺藍', '深藍', '粉紅']])

        # Replace '全選' to a list with all sizes
        df['Sizes'] = df['Sizes'].apply(split_column_value)
        df['Sizes'] = df['Sizes'].apply(update_select_all_value, args=[['S', 'M', 'L', 'XL', 'F']])
        
        # Replace image to expected path
        if 'API' in sheet_name:
            df['Main Image'] = df['Main Image'].apply(update_image_value, args=[("mainImage.jpg")])
            df['Other Image 1'] = df['Other Image 1'].apply(update_image_value, args=[("otherImage0.jpg")])
            df['Other Image 2'] = df['Other Image 2'].apply(update_image_value, args=[("otherImage1.jpg")])    
        else:
            df['Main Image'] = df['Main Image'].apply(update_image_value, args=[(os.getcwd() + "/test_data/mainImage.jpg")])
            df['Other Image 1'] = df['Other Image 1'].apply(update_image_value, args=[(os.getcwd() + "/test_data/otherImage0.jpg")])
            df['Other Image 2'] = df['Other Image 2'].apply(update_image_value, args=[(os.getcwd() + "/test_data/otherImage1.jpg")])
        
        data_list = df.to_dict('records')
        logging.info(data_list)

        return data_list