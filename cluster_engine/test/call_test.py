import importlib.util
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

spec = importlib.util.spec_from_file_location("pc", BASE_DIR + "/cluster-engine/process.py")
pc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pc)

spec2 = importlib.util.spec_from_file_location("catalog", BASE_DIR + "/intelligent-catalog-service/catalog.py")
catalog = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(catalog)

settings = {
    'check': {'interval': 0, 'checkcode': 0},
    'input_type': '',
    'input_settings': '',
    'index_features': 'NAME',
    'ui_features': '',
    'output_type': '',
    'output_settings': '',
    "pre_processed_file_path": BASE_DIR + "/cluster-engine/test/",
    "pre_processed_file_name": "sample_test.json",
    "pre_processed_file_type": 'json',
    "processed_file_path": BASE_DIR + "/cluster-engine/test/",
    "processed_file_name": "sample_test_clusters.json",
    "processed_file_type": 'json',
    "processed_yet_file_path": BASE_DIR + "/cluster-engine/data/processed/",
    "web_data_file_path": BASE_DIR + "/intelligent-catalog-web/app/data/",
    "web_data_file_name": "dotz_model.json",
    "web_data_file_type": "json",
    "items_updated_file_path": BASE_DIR + "/intelligent-catalog-web/app/data/",
    "items_updated_file_name": "items_updated.json",
    "items_updated_file_type": "json",
}

catalog = catalog.Catalog(settings)

result = pc.process_catalog(catalog)

print(result)
