import json
import datetime
import importlib.util
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\','/')

#spec = importlib.util.spec_from_file_location("data_manager", BASE_DIR + "/data-manager/data_manager.py")
#dm = importlib.util.module_from_spec(spec)
#spec.loader.exec_module(dm)

#spec_ce = importlib.util.spec_from_file_location("cluster_engine", BASE_DIR + "/cluster-engine/process.py")
#ce = importlib.util.module_from_spec(spec_ce)
#spec_ce.loader.exec_module(ce)
import data_manager.data_manager as dm
from cluster_engine import process as ce


"""
Catalog Status
"Init" - initial status when catalog object is created
"Ready to Publish" - when catalog was processed
"Draft" - when catalog was updated through web interface
"Published" - when catalog was published
"""
STATUS = {"Init": 0, "Ready": 1, "Draft": 2, "Published": 3}


class Catalog(object):

    def __init__(self, settings):
        self.settings = settings
        self.interval = settings["check"]["interval"]
        self.checkcode = settings["check"]["checkcode"]
        self.input_type = settings["input_type"]
        self.input_settings = settings["input_settings"]
        self.pre_processed_file_name = settings["pre_processed_file_name"]
        self.pre_processed_file_path = settings["pre_processed_file_path"]
        self.pre_processed_file_type = settings["pre_processed_file_type"]
        self.items_updated_file_name = settings["items_updated_file_name"]
        self.items_updated_file_path = settings["items_updated_file_path"]
        self.items_updated_file_type = settings["items_updated_file_type"]
        self.processed_file_name = settings["processed_file_name"]
        self.processed_file_path = settings["processed_file_path"]
        self.processed_file_type = settings["processed_file_type"]
        self.index_features = settings["index_features"]
        self.ui_features = [item['value'] for item in settings['ui_features'] if item['type'] == 'user']
        self.output_type = settings["output_type"]
        self.output_settings = settings["output_settings"]
        self.status = STATUS["Init"]
        self.new_version = False
        self.last_changed = datetime.datetime.now()

    def set_status(self, status):
        self.status = status
        self.last_changed = datetime.datetime.now()
        file = open(BASE_DIR + '/intelligent_catalog_service/config/status.config', 'w')
        strstatus = str(status)
        file.write(strstatus)
        file.close()

    def get_status(self):
        status = ""
        if self.status == "" or self.status == STATUS["Init"]:
            file = open(BASE_DIR + '/intelligent_catalog_service/config/status.config', 'r')
            status = file.read()
            file.close()
            if status is not None:
                self.status = status
            else:
                status = STATUS["Init"]
        else:
            status = self.status

        if status == "" or status is None:
            status = STATUS["Init"]

        return status

    def get_last_changed(self):
        return self.last_changed

    def set_new_version(self, status):
        self.new_version = status
        if status:
            self.check_new_version(self)

    def check_new_version(self):
        datamanager = dm.DataManager()
        datamanager.load_settings(self)

        #get the last change data from lastmodified.config
        file = open(BASE_DIR + '/intelligent_catalog_service/config/lastmodified.config', 'r')
        lastmodified = file.read()
        file.close()

        return_data = datamanager.check_new_version(lastmodified)

        return return_data

    def load_new_version(self):
        datamanager = dm.DataManager()
        datamanager.load_settings(self)
        return_data = datamanager.load_new_version()
        self.set_status(STATUS["Ready"])

        return return_data

    def process_catalog(self, full_process=False):
        if full_process:
            to_process = 1
        else:
            to_process = 0

        datamanager = dm.DataManager()
        datamanager.load_settings(self)

        self.set_locked()

        # if datamanager.copy_from_web_to_process() == "Done":
        return_process = ce.process_catalog(self, to_process)

        self.set_unlocked()

        if return_process == 0:
            return_data = "Done"
        else:
            return_data = return_process
        # else:
        #     return_data = "Error copying data!"

        return return_data

    def publish_catalog(self, df):
        datamanager = dm.DataManager()
        datamanager.load_settings(self)

        self.set_locked()

        return_data = False
        # Get catalog status
        self.status = self.get_status()

        if int(self.status) == STATUS["Ready"]:
            return_data = datamanager.publish_catalog(df)

            if return_data == "Done":
                self.set_status(STATUS["Published"])
        
        self.set_unlocked()
        
        return return_data

    def copy_processed_catalog_to_web(self):
        datamanager = dm.DataManager()
        datamanager.load_settings(self)
        return_data = datamanager.copy_processed_to_web()

        return return_data

    def run_other(self):
        datamanager = dm.DataManager()
        datamanager.load_settings(self)
        return_data = datamanager.run_other()

        return return_data

    def set_locked(self):
        file = open(BASE_DIR + '/intelligent_catalog_service/config/lock.config', 'w')
        file.write('1')
        file.close()

    def set_unlocked(self):
        file = open(BASE_DIR + '/intelligent_catalog_service/config/lock.config', 'w')
        file.write('0')
        file.close()

    def get_lock_status(self):
        file = open(BASE_DIR + '/intelligent_catalog_service/config/lock.config', 'r')
        status = file.read()
        file.close()

        return status

    def schedule_process(self):
        return_data = "Done"
        status = self.get_lock_status()

        if int(status) == 0:
            file = open(BASE_DIR + '/intelligent_catalog_service/config/schedule.config', 'w')
            file.write('1')
            file.close()
        elif int(status) == 1:
            return_data = "Already processing"
        else:
            return_data = ""

        return return_data

    def unschedule_process(self):
        file = open(BASE_DIR + '/intelligent_catalog_service/config/schedule.config', 'w')
        file.write('0')
        file.close()


    def get_schedule_status(self):
        file = open(BASE_DIR + '/intelligent_catalog_service/config/schedule.config', 'r')
        status = file.read()
        file.close()

        return status

    def load_data(self, source_file_name, dataset_name, table_name):
        datamanager = dm.DataManager()
        datamanager.load_settings(self)

        status = datamanager.insert_from_csv(source_file_name, dataset_name, table_name)

        return status

