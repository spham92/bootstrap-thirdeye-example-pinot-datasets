#!/usr/bin/env python3

import json
import os

import requests

PINOT_CONTROLLER = 'http://localhost:9000'


def bootstrap(path_to_te_examples):
    if 'thirdeye/examples' not in path_to_te_examples:
        raise Exception('Current working directory is not the examples directory')

    for example_table_directory_name in os.listdir(path_to_te_examples):
        path_to_directory = os.path.join(path_to_te_examples, example_table_directory_name)
        files_in_directory = os.listdir(path_to_directory)

        if 'schema.json' not in files_in_directory:
            print('Skipping due to missing schema file for:', example_table_directory_name)
            continue

        if 'table_config.json' not in files_in_directory:
            print('Skipping due to missing table_config file for:', example_table_directory_name)
            continue

        if 'rawdata' not in files_in_directory:
            print('Skipping due to missing rawdata directory for:', example_table_directory_name)
            continue

        with open(os.path.join(path_to_directory, 'schema.json')) as f:
            schema_upload_request = requests.post(f'{PINOT_CONTROLLER}/schemas', json=json.load(f))

            if schema_upload_request.status_code != 200:
                print('Experienced issue uploading schema for:', example_table_directory_name)
                continue

        with open(os.path.join(path_to_directory, 'table_config.json')) as f:
            table_config = json.load(f)
            table_upload_request = requests.post(f'{PINOT_CONTROLLER}/tables',
                                                 json=table_config)

            if table_upload_request.status_code != 200:
                print('Experienced issue uploading table config for:', example_table_directory_name)
                continue

        with open(os.path.join(path_to_directory, 'rawdata', 'data.csv'), 'rb') as f:
            multipart_form_data = {
                'file': ('data.csv', f),
            }

            table_name = table_config['tableName']
            params = {
                'tableNameWithType': f'{table_name}_OFFLINE',
                'batchConfigMapStr': '{"inputFormat":"csv", "recordReader.prop.delimiter":","}'
            }
            response = requests.post(
                f'http://localhost:9000/ingestFromFile',
                params=params,
                files=multipart_form_data)

            if response.status_code != 200:
                print('Experienced issue uploading data for:', example_table_directory_name)
                print(response)

        print('Successfully added: ', table_name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bootstrap(os.getcwd())
