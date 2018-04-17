import os
import json

class Settings(object):
    @staticmethod
    def get():
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        CUSTOMER = 'viavarejo'

        if CUSTOMER == 'dotz':
            return_value = {
                "check": {
                    "interval": 3600,
                    "checkcode": "checkcode.py"
                },
                "input_type": "bigquery",
                "input_settings": {
                    "project_name": "dotzcloud-datalabs-sandbox",
                    "dataset_name": "Teste_Acardoso",
                    "table_name": "TB_PADRONIZA_SKU_BMIND_FINAL",
                    #"table_name": "DUMMIE",
                    "APIKey": BASE_DIR + "/intelligent_catalog_service/config/bmind-bigquery-sandbox.json",
                    "file_name": "catalog",
                    "file_path": BASE_DIR + "/cluster_engine/data/",
                    "file_type": "json",
                },
                "pre_processed_file_path_full": BASE_DIR + "/cluster_engine/data/",
                "pre_processed_file_name_full": "catalog",
                "pre_processed_file_type_full": 'json',
                "pre_processed_file_path": BASE_DIR + "/app/data/",
                "pre_processed_file_name": "dotz_model.json",
                "pre_processed_file_type": 'json',
                "processed_file_path": BASE_DIR + "/cluster_engine/data/",
                "processed_file_name": "catalog_clustered.json",
                "processed_file_type": 'json',
                "processed_yet_file_path": BASE_DIR + "/cluster_engine/data/processed/",
                "web_data_file_path": BASE_DIR + "/app/data/",
                "web_data_file_name": "dotz_model.json",
                "web_data_file_type": "json",
                "items_updated_file_path": BASE_DIR + "/app/data/",
                "items_updated_file_name": "items_updated.json",
                "items_updated_file_type": "json",
                "index_features": ["Product_Name", "Brand_Name"],
                "ui_features": read_json(BASE_DIR + '/intelligent_catalog_service/config/dotz.json')["ui_features"],
                "output_type": "bigquery",
                "output_settings": {
                    "project_name": "dotzcloud-datalabs-sandbox",
                    "dataset_name": "SKU",
                    "table_name": "GOLDEN_CATALOG",
                    "APIKey": BASE_DIR + "/intelligent_catalog_service/config/bmind-bigquery-sandbox.json",
                    "file_name": "catalog",
                    "file_path": BASE_DIR + "/cluster_engine/data/",
                    "file_type": "json",
                }
            }
        elif CUSTOMER == 'viavarejo':
            return_value = {
                "check": {
                    "interval": 3600,
                    "checkcode": "checkcode.py"
                },
                "input_type": "bigquery",
                "input_settings": {
                    "project_name": "alpine-surge-149218",
                    "dataset_name": "product_match",
                    "table_name": "eletrodomestico_2103",
                    "APIKey": BASE_DIR + "/intelligent_catalog_service/config/key_vv.json",
                    "file_name": "catalog",
                    "file_path": BASE_DIR + "/cluster_engine/data/",
                    "file_type": "json",
                },
                "pre_processed_file_path_full": BASE_DIR + "/cluster_engine/data/",
                "pre_processed_file_name_full": "catalog",
                "pre_processed_file_type_full": 'json',
                "pre_processed_file_path": BASE_DIR + "/app/data/",
                "pre_processed_file_name": "viavarejo_model.json",
                "pre_processed_file_type": 'json',
                "processed_file_path": BASE_DIR + "/cluster_engine/data/",
                "processed_file_name": "catalog_clustered.json",
                "processed_file_type": 'json',
                "processed_yet_file_path": BASE_DIR + "/cluster_engine/data/processed/",
                "web_data_file_path": BASE_DIR + "/app/data/",
                "web_data_file_name": "eletrodomestico_2103.json",
                "web_data_file_type": "json",
                "items_updated_file_path": BASE_DIR + "/app/data/",
                "items_updated_file_name": "items_updated.json",
                "items_updated_file_type": "json",
                "index_features": ["Product_Name", "Brand_Name"],
                "ui_features": read_json(BASE_DIR + '/intelligent_catalog_service/config/viavarejo.json')["ui_features"],
                "output_type": "bigquery",
                "output_settings": {
                    "project_name": "alpine-surge-149218",
                    "dataset_name": "product_match",
                    "table_name": "eletrodomestico_2103_ret",
                    "APIKey": BASE_DIR + "/intelligent_catalog_service/config/key_vv.json",
                    "file_name": "catalog",
                    "file_path": BASE_DIR + "/cluster_engine/data/",
                    "file_type": "json",
                }
            }       
        return return_value

def read_json(filepath):
    with open(filepath, encoding='utf-8') as data_file:
        data = json.loads(json.dumps(json.load(data_file)))
    return data