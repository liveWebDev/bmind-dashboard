import os
import time
import uuid
from google.cloud import storage
from google.cloud import bigquery
from google.cloud.bigquery import Dataset
from google.cloud.bigquery import LoadJobConfig
from google.cloud.bigquery import SchemaField
import json
from pprint import pprint
import pandas_gbq
import pandas as pd


class BigQueryModel(object):

    def __init__(self, service_account_json_key):
        # exported json key file
        self.key = service_account_json_key
        self.client = bigquery.Client.from_service_account_json(self.key)

    def create_dataset(self, dataset_name, dataset_description):
        dataset_ref = self.client.dataset(dataset_name)
        dataset = Dataset(dataset_ref)
        dataset.description = dataset_description
        dataset = self.client.create_dataset(dataset)
        return dataset

    def get_dataset(self, dataset_name):
        dataset_ref = self.client.dataset(dataset_name)
        return self.client.get_dataset(dataset_ref)

    def list_datasets(self):
        return self.client.list_datasets()

    def refresh_dataset(self, dataset):
        dataset = self.client.get_dataset(dataset)
        return dataset

    def update_dataset_description(self, dataset, description):
        dataset.description = description
        dataset = self.client.update_dataset(dataset, ['description'])  # API request
        return dataset.description == description

    def list_tables(self, dataset):
        tables = list(self.client.list_tables(dataset))  # API request(s)
        return tables

    def create_table(self, dataset, schema, new_table_name):
        table_ref = dataset.table(new_table_name)
        table = bigquery.Table(table_ref, schema=schema)
        table = self.client.create_table(table)  # API request
        return table

    def create_table_from_csv(self, dataset, table_name, file_path, schema):
        table_ref = dataset.table(table_name)

        load_config = LoadJobConfig()
        load_config.skip_leading_rows = 1
        load_config.schema = schema

        with open(file_path, 'rb') as readable:
            self.client.load_table_from_file(
                readable, table_ref, job_config=load_config)  # API request

        return

    def get_table(self, dataset, table_name):
        table_ref = dataset.table(table_name)
        table = self.client.get_table(table_ref)  # API request
        return table

    def get_table_rows(self, table):
        rows = self.client.list_rows(table)
        return rows

    def insert_table_rows(self, table, json_data):
        errors = self.client.insert_rows(table, json_data)
        return errors

    def insert_from_stream(self, dataset, table, json_data):
        dataset_ref = self.client.dataset(dataset)
        table_ref = dataset_ref.table(table)
        data = json.loads(json_data)

        # Get the table from the API so that the schema is available.
        table = self.client.get_table(table_ref)

        rows = [data]
        errors = self.client.create_rows(table, rows)

        return errors

    def insert_from_csv(self, source_file_name, dataset, table):
        dataset_ref = self.client.dataset(dataset)
        table_ref = dataset_ref.table(table)

        with open(source_file_name, 'rb') as source_file:
            # This example uses CSV, but you can use other formats.
            # See https://cloud.google.com/bigquery/loading-data
            job_config = bigquery.LoadJobConfig()
            job_config.source_format = 'text/csv'
            job_config.skip_leading_rows = 1
            job_config.autodetect = True
            job_config.max_bad_records = 1800
            job_config.ignore_unknown_values = True
            job_config.field_delimiter = "|"
            job_config.allow_jagged_rows = True
            job_config.ignore_unknown_values = True
            job_config.allow_quoted_newlines = True
            # job = self.client.load_table_from_file(source_file, table_ref, job_config=job_config)
            try:
                print('INFO','insertTable: BigQuery table loading [{}]'.format(table_ref))
                job = self.client.load_table_from_file(source_file, table_ref, job_config=job_config)
                job.result()
            except Exception as ex:
                print('ERROR','insertTable: Biquery load file {} Erro-> {}'.format(table_ref, str(ex)))

        # see job.result() for wait for job complete
        print('Loaded {} rows into {}:{}.'.format(job.output_rows, dataset_ref, table_ref))
        source_file.close()

        return job

    def load_data_from_gcs(self, dataset, table, bucket_name, blob_name):
        # Google Cloud Storage
        # gs://example-bucket/example-data.csv
        dataset_ref = self.client.dataset(dataset)
        table_ref = dataset_ref.table(table)

        gs_url = 'gs://{}/{}'.format(bucket_name, blob_name)
        job_id_prefix = "load_data_job"
        job_config = bigquery.LoadJobConfig()
        job_config.create_disposition = 'NEVER'
        job_config.skip_leading_rows = 1
        job_config.source_format = 'CSV'
        job_config.write_disposition = 'WRITE_EMPTY'
        job = self.client.load_table_from_uri(
            gs_url, table_ref, job_config=job_config,
            job_id_prefix=job_id_prefix)  # API request
        # job.state == 'RUNNING'
        # job.job_type == 'load'
        # job.state == 'DONE'
        # job = self.client.load_table_from_uri(source, table_ref)
        return job

    def query(self, sql_text):
        # sql_text = (
        #    'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
        #    'WHERE state = "TX" '
        #    'LIMIT 100')
        query_job = self.client.query(sql_text)  # API request
        rows = query_job.result()  # Waits for query to finish

        return rows

    def get_dataframe_from_table(self, project, _dataset, _table):
        # TODO: Adicionar as colunas como parametro para buscar 
        #columns = "PARTNER_ID, PRODUCT_ID, MANUFACTURER_ID, CATEGORY_1, CATEGORY_2, CATEGORY_3, CATEGORY_4, NAME, INTRODUCED_DATE, RETIRED_DATE, UNIT, BRAND, PACKAGE_SIZE, PACKAGE_UNIT, PRIVATE_LABEL_FLAG, GTIN"
        columns = "*"
        dtset = _dataset
        tble = _table

        print("tabela ==> " + _table)

        sQuery = "SELECT " + columns + " FROM " + dtset + ".`" + tble + "`"
        df_return = pandas_gbq.read_gbq(sQuery, project, private_key=self.key, dialect='standard')

        return df_return

    def write_dataframe_to_bigquery(self, df, project, _dataset, _table):
        try:
            pandas_gbq.to_gbq(df, _dataset+'.'+_table, project, chunksize=10000, verbose=True, private_key=self.key,if_exists='append')
        except Exception as ex:
            df_return = "Error {}".format(str(ex))
        else:
            df_return = "Done"

        print(df_return)
        return df_return

    def __enter__(self):
        return self

    def mytest(self, project_id, dataset_id, table_id, storage_uri, local_data_path):
        # dataset = self.client.dataset(dataset_id)

        datasetref = self.get_dataset(dataset_id)
        tabela = self.get_table(datasetref, table_id)
        rows = self.client.list_rows(tabela)

        df = pd.DataFrame(data=[list(x.values()) for x in rows], columns=list(rows[0].keys()))

        return df

        # table = dataset.table(table_id)
        # job_name = str(uuid.uuid4())
        #
        # job = self.client.extract_table_to_storage(
        #     job_name, table, storage_uri)
        #
        # job.begin()
        # job.result()  # Wait for job to complete
        #
        # print('Exported {}:{} to {}'.format(
        #     dataset_id, table_id, storage_uri))

    # if __name__ == '__main__':
    #     PROJECT_ID = "my-project"
    #     DATASET_ID = "bq_dataset"
    #     TABLE_ID = "bq_table"
    #     STORAGE_URI = "gs://my-bucket/path/for/dropoff/*"
    #     LOCAL_DATA_PATH = "/path/to/save/"
    #
    #     bq_to_df(PROJECT_ID, DATASET_ID, TABLE_ID, STORAGE_URI, LOCAL_DATA_PATH)
