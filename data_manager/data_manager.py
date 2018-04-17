import pandas as pd
import shutil
from datetime import datetime
import json
import importlib.util
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#spec = importlib.util.spec_from_file_location("bigquery_model", BASE_DIR + "/data-manager/models/bigquery_model.py")
#bqm = importlib.util.module_from_spec(spec)
#spec.loader.exec_module(bqm)
from data_manager.models import bigquery_model as bqm

class DataManager(object):
    """ Get, transform and export data from any to any catalog data sources."""

    def __init__(self):
        # PRIVATE ATTRIBUTES
        self.__catalog = None
        self.__dataframe = None
        self.__transformed_data = None
        self.__input_file = ""
        self.__output_file = ""

    def load_settings(self, catalog):
        """ Load catalog settings
            :type catalog: object Catalog
            :param catalog: the catalog containing all configurations used by DataManager

            Returns:
                Nothing
        """
        self.__catalog = catalog

    def check_new_version(self, last_change = ""):
        """ Check new Catalog version available

            Returns:
                str: a status message of the process
                    "Yes" - exists a new version
                    "No" - no exists a new version, process complete.
                    "Error ..." - Error message, some problems found!
        """
        if self.__catalog.input_type == 'bigquery':
            # get the last modified time from bigquery and compare with internal file
            return_status = "No"
        else:
            return_status = "No"

        return return_status

    def load_new_version(self):
        """ Load a new version of a Catalog, getting data from source, transforming and exporting to Cluster Engine

            Returns:
                str: a status message of the process
                    "Done" - all right!
                    "Error ..." - Error message, some problems found!
        """
        return_status = "Done"
        return_import = self.__import()

        if return_import == "Done":
            return_transform = self.__transform()
            if return_transform == "Done":
                return_export = self.__export()
                if return_export != "Done":
                    return_status = "Error exporting data! Error message: " + return_export
            else:
                return_status = "Error transforming data! Error message: " + return_transform
        else:
            return_status = "Error importing data! Error message: " + return_import

        return return_status

    def get_data(self):
        """ Get data from source

        Returns:
             str: a status message of the process
                "Done" - all right!
                "Error ..." - Error message, some problems found!
        """
        return_message = self.__import()

        return return_message

    # PUBLIC METHOD
    def transform_data(self):
        """ Transform data after import

        Returns:
             str: a status message of the process
                "Done" - all right!
                "Error ..." - Error message, some problems found!
        """
        data = self.__transform()
        self.__transformed_data = data
        return_message = "Done"

        return return_message

    # PUBLIC METHOD
    def export_data(self):
        """ Export data after transform """
        self.__export()

        return True

    def publish_catalog(self, df):
        """ Routine to publish catalog """
        return_message = self.__publish(df)

        return return_message

    def copy_processed_to_web(self):
        file_before_processing = self.__catalog.settings["pre_processed_file_path"] + self.__catalog.settings["pre_processed_file_name"]
        file_before_processing_destination = self.__catalog.settings["processed_yet_file_path"] + datetime.now().strftime('%Y%m%d%H%M%S') + "_" + self.__catalog.settings["pre_processed_file_name"]
        file_source = self.__catalog.settings["processed_file_path"] + self.__catalog.settings["processed_file_name"]
        file_destination = self.__catalog.settings["web_data_file_path"] + self.__catalog.settings["web_data_file_name"]
        file_after_processing_destination = self.__catalog.settings["processed_yet_file_path"] + datetime.now().strftime('%Y%m%d%H%M%S') + "_" + self.__catalog.settings["processed_file_name"]

        try:
            if shutil.copyfile(file_source, file_destination) != "":
                shutil.copyfile(file_before_processing, file_before_processing_destination)
                shutil.move(file_source, file_after_processing_destination)
        except FileNotFoundError:
            print("File not found!")

        return_message = "Done"

        return return_message

    def copy_from_web_to_process(self):
        file_source = self.__catalog.settings["web_data_file_path"] + self.__catalog.settings["web_data_file_name"]
        file_destination = self.__catalog.settings["pre_processed_file_path"] + self.__catalog.settings["pre_processed_file_name"]

        print(file_source)

        try:
            if shutil.copyfile(file_source, file_destination) != "":
                return_message = "Done"
            else:
                return_message = "Error"
        except FileNotFoundError:
            print("File not found!")

        return return_message

    def insert_from_csv(self, source_file_name, dataset_name, table_name):
        ''' 
            Utilizado para carregar dados manualmente de arquivos para BiqQuery
        '''
        key = self.__catalog.input_settings['APIKey']
        bq = bqm.BigQueryModel(key)

        return_message = bq.insert_from_csv(source_file_name, dataset_name, table_name)

        return return_message

    def __import(self):
        """ Private method to import data from source

            Returns:
                str: a status message of the process
                    "Done" - all right!
                    "Error ..." - Error message, some problems found!
        """
        return_message = "Done"

        if self.__catalog.input_type == 'bigquery':
            # CREATING A INSTANCE OF CLASS PASSING APIKEY TO AUTHORIZE
            key = self.__catalog.input_settings['APIKey']
            bq = bqm.BigQueryModel(key)
            
            # GETTING DATAFRAME FROM BIGQUERY, USING PANDAS TOOL
            self.__dataframe = bq.get_dataframe_from_table(self.__catalog.input_settings['project_name'],
                                                           self.__catalog.input_settings['dataset_name'],
                                                           self.__catalog.input_settings['table_name'])
        elif self.__catalog.input_type == 'file':
            self.__input_file = self.__catalog.input_settings['file_path'] + self.__catalog.input_settings[
                'file_name'] + '.' + self.__catalog.input_settings['file_type']

            if self.__catalog.input_settings['file_type'] == 'json':
                self.__dataframe = pd.read_json(self.__input_file)
            elif self.__catalog.input_settings['file_type'] == 'csv':
                self.__dataframe = pd.read_csv(self.__input_file, low_memory=False)
            else:
                return_message = "File type " + self.__catalog.input_settings['file_type'] + "not implemented yet"
        elif self.__catalog.input_type == 'google-datastore':
            self.__input_file = self.__catalog.input_settings['file_path'] + self.__catalog.input_settings[
                'file_name'] + self.__catalog.input_settings['file_type']
            # ACCESS BUCKET
            # GET CONTENT AND SAVE IN MEMORY
            # CONVERT TO DATAFRAME
        else:
            return_message = "Unknown input type: " + self.__catalog.input_type

        return return_message

    def __transform(self):
        """ Private method to transform data from a internal Pandas Dataframe to an output type

            Returns:
                str: a status message of the process
                    "Done" - all right!
                    "Error ..." - Error message, some problems found!
        """
        return_message = "Done"

        if self.__catalog.output_type == 'bigquery':
            pass
        elif self.__catalog.output_type == 'file':
            if self.__catalog.output_settings['file_type'] == 'json':
                # EXPORTING A DATAFRAME TO JSON
                self.__transformed_data = self.__dataframe.to_json()
            elif self.__catalog.output_settings['file_type'] == 'csv':
                # EXPORTING A DATAFRAME TO CSV
                self.__transformed_data = self.__dataframe.to_csv()
            else:
                return_message = "File type " + self.__catalog.output_settings['file_type'] + "not implemented yet"

        elif self.__catalog.output_type == 'google-datastore':
            # ACCESS BUCKET
            # GET CONTENT AND SAVE IN MEMORY
            # CONVERT TO DATAFRAME
            pass
        else:
            return_message = "Unknown output type: " + self.__catalog.output_type

        return return_message


    def __export(self):
        """ Private method to export an internal transformed data to a selected destination

            Returns:
                 str: a status message of the process
                      "Done" - all right!
                      "Error ..." - Error message, some problems found!
        """
        return_message = "Done"

        self.__output_file = self.__catalog.output_settings['file_path'] + self.__catalog.output_settings['file_name'] + '.' + self.__catalog.output_settings['file_type']

        if self.__catalog.output_type == 'bigquery':
            if self.__catalog.output_settings['file_type'] == 'json':
                self.__dataframe.to_json(self.__output_file)
        # EXPORTING A DATAFRAME TO CSV
        elif self.__catalog.output_type == 'file':
            if self.__catalog.output_settings['file_type'] == 'json':
                # EXPORTING A DATAFRAME TO JSON
                self.__transformed_data = self.__dataframe.to_json()
            elif self.__catalog.output_settings['file_type'] == 'csv':
                # EXPORTING A DATAFRAME TO CSV
                self.__transformed_data = self.__dataframe.to_csv()
            else:
                return_message = "File type " + self.__catalog.output_settings['file_type'] + "not implemented yet"
        elif self.__catalog.output_type == 'google-datastore':
            # ACCESS BUCKET
            # GET CONTENT AND SAVE IN MEMORY
            # CONVERT TO DATAFRAME
            pass
        else:
            return_message = "Unknown output type: " + self.__catalog.output_type

        return return_message

    def __publish(self, dataframe):
        """ Private method to publish the catalog

                    Returns:
                         str: a status message of the process
                              "Done" - all right!
                              "Error ..." - Error message, some problems found!
                """
        
        key = self.__catalog.input_settings['APIKey']
        bq = bqm.BigQueryModel(key)
        df = dataframe
        file_origin = self.__catalog.settings["web_data_file_path"] + self.__catalog.settings["web_data_file_name"]
        #df = pd.read_json(file_origin)
        # TODO: Tratar os campos que estao vindo do json e somente deixar os itens que serao publicaos
        # Receber como parametro os campos a serem exportados
        # del dataframe['index_features']

        return_message = bq.write_dataframe_to_bigquery(df, self.__catalog.output_settings['project_name'], self.__catalog.output_settings['dataset_name'], self.__catalog.output_settings['table_name'])

        # if df_return == "Done":
        #     return_message = "Done"
        # else:
        #     return_message = df_return

        return return_message


    def run_other(self):
        # CREATING A INSTANCE OF CLASS PASSING APIKEY TO AUTHORIZE
        key = self.__catalog.input_settings['APIKey']
        bq = bqm.BigQueryModel(key)

        # GETTING DATAFRAME FROM BIGQUERY, USING PANDAS TOOL

        self.__dataframe = bq.get_dataframe_from_table(self.__catalog.input_settings['project_name'],
                                                       self.__catalog.input_settings['dataset_name'],
                                                       self.__catalog.input_settings['table_name'])

        self.__output_file = self.__catalog.output_settings['file_path'] + self.__catalog.output_settings['file_name'] + \
                             '.' + self.__catalog.output_settings['file_type']

        self.__dataframe.to_json(self.__output_file)

        # key = self.__catalog.input_settings['APIKey']
        # bq = bqm.BigQueryModel(key)
        # df = bq.mytest("dotzcloud-datalabs-uat", "SKU", "1300", "gs://dotzcloud-datalabs-sku-185314/*", BASE_DIR + "/data-manager/")
        # df.to_json(self.__output_file)