from app.model.bigquery_model import BigQueryModel
import json
from DataViz.settings import DATA_ROOT


class Catalog(object):
    def __init__(self):
        config = json.loads(open(DATA_ROOT + '/catalog.config').read())
        file_catalog = DATA_ROOT + '/' + config[0]["service_account_json_file"]
        self.bq = BigQueryModel(file_catalog)

    def set_dataset(self, dataset_name):
        self.dataset = self.get_dataset(dataset_name)

    def get_dataset(self, dataset_name):
        return self.bq.get_dataset(dataset_name)

    def publish(self, filename):
        from google.cloud.bigquery import SchemaField
        # TODO: O schema devera ser parametrizado para publicacao
        schema = [
            SchemaField('ROW_INDEX', 'STRING'),
            SchemaField('PRODUCT_ID', 'STRING'),
            SchemaField('GTIN', 'FLOAT'),
            SchemaField('MANUFACTURER_ID', 'STRING'),
            SchemaField('PARTNER_ID', 'STRING'),
            SchemaField('CATEGORY_ID_1', 'INTEGER'),
            SchemaField('CATEGORY_ID_2', 'INTEGER'),
            SchemaField('CATEGORY_ID_3', 'INTEGER'),
            SchemaField('CATEGORY_ID_4', 'INTEGER'),
            SchemaField('PARTNER', 'STRING'),
            SchemaField('CATEGORY_NAME_1', 'STRING'),
            SchemaField('CATEGORY_NAME_2', 'STRING'),
            SchemaField('CATEGORY_NAME_3', 'STRING'),
            SchemaField('CATEGORY_NAME_4', 'STRING'),
            SchemaField('NAME', 'STRING'),
            SchemaField('INTRODUCED_DATE', 'STRING'),
            SchemaField('RETIRED_DATE', 'STRING'),
            SchemaField('UNIT', 'STRING'),
            SchemaField('BRAND_ID', 'INTEGER'),
            SchemaField('BRAND', 'STRING'),
            SchemaField('PACKAGE_SIZE', 'STRING'),
            SchemaField('PACKAGE_UNIT', 'STRING'),
            SchemaField('PRIVATE_LABEL_FLAG', 'STRING'),
            SchemaField('CLUSTER_N1_ID', 'INTEGER'),
            SchemaField('CLUSTER_ID', 'INTEGER'),
            SchemaField('B_WEIGHT', 'STRING'),
            SchemaField('B_CONTENT', 'STRING'),
            SchemaField('B_SIZE', 'STRING'),
            SchemaField('B_ALPHA_NUM', 'STRING'),
            SchemaField('ROW_MAIN', 'FLOAT'),
            SchemaField('nunique', 'INTEGER'),
            SchemaField('count', 'INTEGER'),
            SchemaField('WRONG', 'STRING'),
            SchemaField('COMMENT', 'STRING'),
        ]

        table = self.bq.create_table_from_csv(self.dataset, 'products_v3', filename, schema)

    def get_table_data(self):
        dataset_ref = self.get_dataset("intelligent_catalog")
        table_ref = self.bq.get_table(dataset_ref, 'products_v2')
        table_data = self.bq.get_table_rows(table_ref)

        return table_data


class ExportData(object):
    def __init__(self):
        config = json.loads(open(DATA_ROOT + '/catalog.config').read())
        self.file_catalog = DATA_ROOT + '/' + config[0]["service_account_json_file"]

    def from_bigquery(self, file_destination, file_type):
        return_message = ""
        try:
            bq = BigQueryModel(self.file_catalog)
            df_return = bq.get_dataframe_from_table('dotzcloud-datalabs-sku-185314', 'intelligent_catalog', 'products_v2')
        except Exception as e:
            print(str(e))
        else:
            return_message = "Done"
            if file_type == 'json':
                df_return.to_json(file_destination + '.' + file_type)
            elif file_type == 'csv':
                df_return.to_csv(file_destination + '.' + file_type)
            else:
                return_message = "Permitted file types: json or csv"

        return return_message
