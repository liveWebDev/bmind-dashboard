"""
Module for process and create a model based on Catalog class.
"""
import datetime
import json
import os

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from cluster_engine.bmind.nlp import cleaning
from cluster_engine.bmind.nlp import tokenize
from cluster_engine.bmind.nlp.word2vec import gsim
from cluster_engine.bmind.purify import dedup


def preprocessing(text):
    """
    Process for cleaning and tokenize the raw text.
    """
    text = cleaning.sentence_clean(text, remove_num=False)
    text = tokenize.word_tokenize(text)
    return text


def create_model(dataframe, index_features, ui_features):
    """
    Create a Word2Vec model based on corpus collection of sentences.
    """
    # Preprocessing: Tokenize and join columns based on index_features
    corpus = tokenize_corpus(dataframe, index_features, ui_features)
    model = gsim.create_model(corpus)

    return model


def save_model(model):
    return 0


def load_model(model_path):
    return 0


def process_catalog(catalog, to_process=0):
    """
    Process a Catalog based on word2vec model and relative dictionary.
    """
    # Read Data Source JSON
    if to_process == 1:
        pre_processed_file_name = catalog.settings['pre_processed_file_name_full'] + \
            '.' + catalog.settings['pre_processed_file_type_full']
        pre_processed_file_path = catalog.settings['pre_processed_file_path_full']
        processed_file_name = catalog.settings['web_data_file_name']
        processed_file_path = catalog.settings['web_data_file_path']
    else:
        pre_processed_file_name = catalog.settings['pre_processed_file_name']
        pre_processed_file_path = catalog.settings['pre_processed_file_path']
        processed_file_name = catalog.settings['processed_file_name']
        processed_file_path = catalog.settings['processed_file_path']

    index_features = catalog.index_features
    ui_features = [item['value'] for item in catalog.settings['ui_features'] if item['type'] != 'sys']
    source_file = pre_processed_file_path + pre_processed_file_name
    items_updated_file_name = catalog.items_updated_file_name
    items_updated_file_path = catalog.items_updated_file_path
    items_updated_file_type = catalog.items_updated_file_type

    __print('Initializing process...')
    __print('Process Catalog for {}, with columns {}'.format(
        pre_processed_file_name, str(index_features)), True)

    __print('Reading File...')
    df = pd.read_json(source_file)
    df = df.fillna('')
    __print('{} read!'.format(pre_processed_file_name))

    if to_process == 1:
        # Create or Load word2vec model
        __print('Creating Model...')
        model = create_model(df, index_features, ui_features)
        __print('Model created!')

        # Instance a Dedup Class for process
        dp = dedup.Dedup(model, modelpath='')  # TODO: Option to load model from file

        # Index Row
        # df['ROW_INDEX'] = df.apply(lambda row: dp.set_row_index, axis=1)

        # Create a relative dictionary
        __print('Creating Relative Dictionary...')
        df.apply(lambda row: dp.create_relative_dict(
            row['index_features']), axis=1)  # TODO: save dp.relative_words
        dp.update_dict()
        __print('Relative Dictionary created!')

        __print('Processing Clusters...')
        df = process_clusters(dp, df)
        __print('Clusters created!')

    if items_updated_file_name != '':
        __print('Apply validation...')
        # file_path = items_updated_file_path + '/' + items_updated_file_name
        # if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        #     if 'BRAND' in df.columns:
        #         df = apply_validation(df, file_path)

        __print('Validation applied!')
    # Apply unique - conta quantos itens o cluster possui para filtro de UNIQUE e DUPLICATED
    # criando coluna nunique
    df_unique = df.groupby(['CLUSTER_ID'])['CLUSTER_ID'].count(
         ).reset_index(name='nunique')
    # Realiza merge df com df_unique pelo CLUSTER_ID
    df = pd.merge(df, df_unique, how='inner', on=['CLUSTER_ID'])
    # TODO: Leandro 08/03/2018 - Manter abaixo para compatibilidade com UI - verificar utilidade
    df['count'] = 1
    # Criar indice unico de item por cluster - ROW_INDEX
    # CLUSTER_ID + Numero do item/linha
    __print('Creating Primary Key for items ...')
    df['ITEM_ID_TEMP'] = df.groupby(['CLUSTER_ID']).cumcount()+1
    df['CLUSTER_ID_str'] = df['CLUSTER_ID'].astype(str)
    df['ITEM_ID_str'] = df['ITEM_ID_TEMP'].astype(str)
    df['ROW_INDEX'] = df['CLUSTER_ID_str'] + df['ITEM_ID_str']
    
    del df['ITEM_ID_TEMP'], df['CLUSTER_ID_str'], df['ITEM_ID_str']

    __print('Apply Row Main...')
    df = dp.set_row_main(df)

    __print('Saving Clusters...')

    df.to_json(path_or_buf=processed_file_path+processed_file_name, orient='records')

    catalog_json = json.loads(df.to_json(orient='records', double_precision=0), encoding='utf-8')
    json_out = processed_file_path + processed_file_name

    with open(json_out, 'w', encoding='utf-8') as outfile:
        json.dump(catalog_json, outfile)
        __print('Clusters saved {}'.format(json_out))

    return 0


def reprocess_catalog():
    return 0


def tokenize_corpus(df, index_features, ui_features):
    df['index_features'] = df[index_features].apply(lambda x: ' '.join(x), axis=1)
    result = [preprocessing(text['index_features']) for index, text in df.iterrows()]

    return result


def process_clusters(dp, df):
    # Atribui numero de cluster SEM remocao do numero do nome do item
    # 
    df['CLUSTER_ID'] = df.apply(lambda row: dp.to_cluster(
        row['index_features'], remove_num=False), axis=1)
    df['CLUSTER_ID'] = df['CLUSTER_ID'].astype('category').cat.codes
    
    # Atribui numero de cluster COM remocao do numero do nome do item
    #
    df['CLUSTER_N1_ID'] = df.apply(lambda row: dp.to_cluster(
        row['index_features'], remove_num=True), axis=1)
    df['CLUSTER_N1_ID'] = df['CLUSTER_N1_ID'].astype('category').cat.codes
    
    # Cria novas colunas no dataframe para controle de filtros da tela
    df['categoryid1'] = df['Category_ID_1'].astype('category').cat.codes
    df['categoryid2'] = df['Category_ID_2'].astype('category').cat.codes
    df['categoryid3'] = df['Category_ID_3'].astype('category').cat.codes
    #df['categoryid4'] = df['CATEGORY_4'].astype('category').cat.codes

    df['brandid'] = df['Brand_Name'].astype('category').cat.codes

    return df


def apply_validation(df, val_file_path):
    """
    Apply the user validation to fix the clusters process.
    """
    df_val = pd.read_json(__read_json(val_file_path))

    if 'WRONG' in df_val.columns:
        df_val = df_val[df_val['WRONG'] == 1]
        df_val[['CLUSTER_ID']] = df_val[['CLUSTER_ID']].astype(float)

        for item in df_val.iterrows():
            arr_items_to_change = df.loc[(df['CLUSTER_ID'] == item[1]['CLUSTER_ID']) & (
                df['NAME'] == item[1]['NAME']) & (df['BRAND'] == item[1]['BRAND'])].index.values
            cluster_to_change = item[1]['CLUSTER_ID']
            for cluster_element in arr_items_to_change:
                df.at[cluster_element, 'CLUSTER_ID'] = cluster_to_change + 0.1

        # Truncating validations file
        try:
            file_change = open(val_file_path, 'w')
            file_change.write("{}")
            file_change.close()
        except FileNotFoundError:
            pass

    return df


def __read_json(filepath):
    with open(filepath) as data_file:
        data = json.dumps(json.load(data_file))
    return data


def __print(msg, breakline=False):
    time = str(datetime.datetime.now())
    if msg == 'time':
        msg = time
    else:
        msg = time + ' | ' + msg

    if breakline:
        msg += '\n'

    print(msg)
