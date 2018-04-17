"""
Definition of views.
"""

import json
import math
import os
import re
from datetime import datetime

import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpRequest, JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Import View to work with CBV Class Based views - Leandro 11/12/2017
from django.views.generic import View

from DataViz.settings import DATA_ROOT
# Import User and UserInfo Forms
from app.forms import UserForm, UserProfileInfoForm

BASE_DIR_FILE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from intelligent_catalog_service import catalog as catalog_service
from intelligent_catalog_service import settings as catalog_settings

config = ''
file_catalog_dir = ''
df = []
df_changed = []
# df_items_count = []
# df_all_clusters = []
df_set_filter = []
filters_applied = {}
page_size = 20
df_resume_n1_headers = {}
df_resume_n2_headers = {}
df_resume_n1_items = []
df_resume_n2_items = []
qt_cluster_sum = 0
qt_name_sum = 0
graph_html = ''
catalog_name = ''
catalog_version = ''
catalog_status = ''
catalog_date = ''
info_clusters_number = 0
info_clusters_items = 0
info_clusters_interacted = 0
ics_data = None
items_updated_file_path = ""
items_updated_file_name = ""
catalog_lock_status = "0"
CUSTOMER = 'viavarejo'
_current_filters = ''

# Create a dataframe with the structure of df frame, without data
df_filter = df[:0]
total_record_num = 0
is_setted_filter = 0

def catalog_load():
    global config, file_catalog_dir, catalog_name, catalog_version, catalog_status, catalog_date, df, df_changed, \
        df_items_count, df_all_clusters, df_set_filter, filters_applied, page_size, ics_data, catalog_service, \
        catalog_settings, items_updated_file_path, items_updated_file_name, CUSTOMER

    file_catalog_dir = DATA_ROOT + '/'

    internal_settings = catalog_settings.Settings.get()
    ics_data = catalog_service.Catalog(internal_settings)

    items_updated_file_path = ics_data.settings['items_updated_file_path']
    items_updated_file_name = ics_data.settings['items_updated_file_name']

    catalog_status_data = get_catalog_status()

    # Read the file to a dataframe
    catalog_file_path = ics_data.settings["web_data_file_path"]
    catalog_file_name = ics_data.settings["web_data_file_name"]
    catalog_file_type = ics_data.settings["web_data_file_type"]

    if catalog_file_type == 'json':
        df = pd.read_json(file_catalog_dir + catalog_file_name)
    elif catalog_file_type == 'csv':
        df = pd.read_csv(file_catalog_dir + catalog_file_name, low_memory=False)

    # Fill NaN data with blank value
    df = df.fillna('')

    df[['CLUSTER_ID']] = df[['CLUSTER_ID']].astype(float)
    # Dotz -> erro no processamen to 14/03
    if CUSTOMER == 'dotz':
        df['Category_Name_1'] = df['Category_ID_1']
        df['Category_Name_2'] = df['Category_ID_2']
        df['Category_Name_3'] = df['Category_ID_3']
        #df['Category_Name_4'] = df['Category_ID_4']

    # Remove quotes and apostrophes
    df['Category_Name_1'] = df['Category_Name_1'].apply(
        lambda x: str(x).replace('"', "").replace("'", "").replace("\\", "").replace("/", "").replace(",", "").replace(
            "{", "").replace("}", "").replace("[", "").replace("]", "").replace('+', "_").replace('-',
                                                                                                  "_").strip()).apply(
        lambda x: str(x).replace('"', "").replace("'", "").replace("\\", "").replace("/", "").replace(",", "").replace(
            "{", "").replace("}", "").replace("[", "").replace("]", "").replace('+', "_").replace('+', "_").strip())
    df['Category_Name_2'] = df['Category_Name_2'].apply(
        lambda x: str(x).replace('"', "").replace("'", "").replace("\\", "").replace("/", "").replace(",", "").replace(
            "{", "").replace("}", "").replace("[", "").replace("]", "").replace('+', "_").replace('+', "_").strip())
    df['Category_Name_3'] = df['Category_Name_3'].apply(
        lambda x: str(x).replace('"', "").replace("'", "").replace("\\", "").replace("/", "").replace(",", "").replace(
            "{", "").replace("}", "").replace("[", "").replace("]", "").replace('+', "_").replace('+', "_").strip())
    # df['Category_Name_4'] = df['Category_Name_4'].apply(
    #     lambda x: str(x).replace('"', "").replace("'", "").replace("\\", "").replace("/", "").replace(",", "").replace(
    #         "{", "").replace("}", "").replace("[", "").replace("]", "").replace('+', "_").replace('+', "_").strip())
    df['Brand_Name'] = df['Brand_Name'].apply(
        lambda x: str(x).replace('"', "").replace("'", "").replace("\\", "").replace("/", "").replace(",", "").replace(
            "{", "").replace("}", "").replace("[", "").replace("]", "").replace('+', "_").replace('+', "_").strip())
    
    # Cria colunas WRONG e COMMENT
    df['WRONG'] = 0
    df['COMMENT'] = ''

    # Adicionar os itens modificados ao dataframe principal
    # If file does not exist, create one with {} content
    if not os.path.exists(items_updated_file_path + items_updated_file_name):
        file = open(items_updated_file_path + items_updated_file_name, 'w')
        file.write("{}")
        file.close()
    # Read the changed data from json and load at df_changed
    data_changed_catalog = json.loads(open(items_updated_file_path + items_updated_file_name).read())
    df_changed = pd.DataFrame(data_changed_catalog)

    # Load all itens updated by userinterface if has content
    if len(df_changed) > 0:
        #TODO: Alterar ROW_INDEX para o HASH

        # Limpar Row_Main anterior
        for item in range(len(df_changed)):
            df.loc[df['ROW_INDEX'] == df_changed.ROW_MAIN_OLD[item], 'ROW_MAIN'] = 0
        
        # Set ROW_MAIN, WRONG e COMMENT
        for item in range(len(df_changed)):
            # Wrong
            df.loc[df['ROW_INDEX'] == df_changed.ROW_INDEX[item], 'WRONG'] = df_changed.WRONG[item]
            # Comment
            df.loc[df['ROW_INDEX'] == df_changed.ROW_INDEX[item], 'COMMENT'] = df_changed.COMMENT[item]
            # Row_Main
            df.loc[df['ROW_INDEX'] == df_changed.ROW_INDEX[item], 'ROW_MAIN'] = df_changed.ROW_MAIN[item]

        # Atribui ROW_MAIN que foram alterados
        # df['ROW_MAIN'] = df.apply(lambda row: 1 if len(row['ROW_INDEX'].isin(df_changed['ROW_INDEX'].values)) > 0 else 0,axis=1)
        
        # Limpa ROW_MAIN que foram alterado
        # df['ROW_MAIN'] = df.apply(lambda row: 0 if len(row['ROW_INDEX'].isin(df_changed['ROW_MAIN_OLD'].values)) > 0 else row['ROW_MAIN'],axis=1)

    # Fill Nulls
    df = df.fillna('')

    # Sort dataframe pela quantidade de itens no dataframe 
    df = df.sort_values(['nunique'], ascending=[0])
    
    # Create a filter dataframe to use in selects (filters page)
    df_set_filter = df[['nunique', 'Category_Name_1', 'Category_Name_2', 'Category_Name_3', 'Brand_Name', 'categoryid1',
                        'categoryid2', 'categoryid3', 'brandid', 'count', 'COMMENT']]

    # Clean filters 
    filters_applied = {}

    # Set quantity of clusters per page
    page_size = 20

    print("Catalog Loaded")

def page_cluster(request):
    global _current_filters, df_filter, df_all_clusters, df, ics_data

    page = int(request.GET.get('page', 1))
    ini = int(request.GET.get('ini', 0))
    c1 = request.GET.get('c1', '')
    c2 = request.GET.get('c2', '')
    c3 = request.GET.get('c3', '')
    b = request.GET.get('b', '')
    g = request.GET.get('g', '')
    txt = request.GET.get('txt', '')

    # Receive GET parameters in a vfilters variable
    vfilters = c1 + c2 + c3 + b + g + txt

    # Define pagination
    page_ini = 0 if page == 1 else ((page - 1) * page_size) + 1
    page_end = page_size if page == 1 else ((page - 1) * page_size) + page_size

    # Verify if filters are setted and if filters are changed
    if len(vfilters) > 0 and vfilters != _current_filters:
        # Verify if unique or duplicated are selected
        if g == '1':
            df_filter = df[df['nunique'] == 1]
        elif g != '':
            df_filter = df[df['nunique'] > 1]
        else:
            df_filter = df

        if len(c1) > 0:
            df_filter = df_filter[df_filter['categoryid1'].isin(c1.split(','))]

        if len(c2) > 0:
            df_filter = df_filter[df_filter['categoryid2'].isin(c2.split(','))]

        if len(c3) > 0:
            df_filter = df_filter[df_filter['categoryid3'].isin(c3.split(','))]

        if len(b) > 0:
            df_filter = df_filter[df_filter['brandid'].isin(b.split(','))]

        phrase = txt.upper()
        array_words = phrase.split()

        if len(txt) > 0:
            for word in array_words:
                df_filter = df_filter[df_filter['Product_Name'].str.contains(word, case=False, na=True)]

        df_clusters = df_filter.groupby(['CLUSTER_ID'])['Product_Name'].nunique().reset_index(name='nunique').sort_values(['nunique'], ascending=False)
        #df_clusters = df_clusters.sort_values(['CLUSTER_ID'], ascending=[1])
        #df_filter = df_clusters
    elif len(vfilters) > 0:
        df_clusters = df_filter
    else:
        df_clusters = df

    _current_filters = c1 + c2 + c3 + b + g + txt
    # page_end = 500
    # BUG Quando o cluster possui mais itens que o tamanho da pagina 
    # Define unique clusters to paging
    arr_clusters_unique = pd.unique(df_clusters['CLUSTER_ID'])
    # Get clusters by page number parameter (UI)
    iclusters = arr_clusters_unique[page_ini:page_end]
    # Creates a new dataframe with just only clusters numbers
    df_resume = df[df['CLUSTER_ID'].isin(iclusters)]

    cols_ui = [item['value'] for item in ics_data.settings['ui_features'] if item['type'] != 'sys']
    cols_sys = ['CLUSTER_ID', 'count', 'nunique', 'ROW_MAIN', 'COMMENT', 'WRONG', 'ROW_INDEX']
    df_resume = df_resume[cols_sys + cols_ui]
    
    # Calcula o numero de paginas conforme front end
    global total_record_num
    if (len(df_clusters) / page_size) % 2 == 0:
        total_record_num = len(df_clusters) / page_size
    else:
        total_record_num = math.ceil(len(df_clusters) / page_size)

    #total_record_num = math.ceil(len(df_clusters) / page_size)

    page_data = {'data': [{'cluster_id': str(c),
                           'cluster_items': json.loads(
                               df_resume[df_resume['CLUSTER_ID'] == c].reset_index().to_json(orient='records'))}
                          for c in iclusters],
                 'total_record_num': total_record_num,
                 'headers': ics_data.settings['ui_features']}

    #TODO: Esta dando erro quando o conteudo contem ' plic
    page_data = json.loads(str(page_data).replace("'", '"').replace('  ', '&nbsp;'))
    page_data = JsonResponse(page_data, safe=False)

    return page_data


def filters(request):
    fields = [{'name': 'Category_Name_1', 'value': 'categoryid1'},
              {'name': 'Category_Name_2', 'value': 'categoryid2'},
              {'name': 'Category_Name_3', 'value': 'categoryid3'},
              {'name': 'Brand_Name', 'value': 'brandid'}
              ]

    filters_data = []

    global is_setted_filter

    for f in fields:
        f_name = f['name']
        f_value = f['value']

        if is_setted_filter == 1:
            global df_set_filter
            df_filters = df_set_filter[[f_name, f_value, 'count']]
        else:
            df_filters = df[[f_name, f_value, 'count']]

        df_filters = df_filters.groupby([f_name, f_value])['count'].sum()
        df_filters = df_filters.reset_index(name='count').sort_values(['count'], ascending=False)

        # df_filters = df_filters.sort_values([f_name], ascending=True)
        df_filters = df_filters[df_filters['count'] > 1]

        del df_filters['count']
        df_filters = df_filters.drop_duplicates()

        filters_data.append(
            {'filter': f_name,
             'items': [{'item': item[f_name], 'value': item[f_value]} for index, item in df_filters.iterrows()]}
        )

    filters_data.append(
        {'filter': 'nunique',
         'items': [{'item': 'Unique', 'value': 1}, {'item': 'Duplicated', 'value': 2}]
         }
    )

    filters_data.append(
        {'filter': 'CLUSTER_ID',
         'items': [{'item': 'More Restrictive: Considering Attributes', 'value': 1},
                   {'item': 'Less Restrictive: Disregarding Attributes', 'value': 2}]
         }
    )

    page_data = str(filters_data).replace("'", '"').replace('\\x', '')
    page_data = json.loads(page_data)
    page_data = JsonResponse(page_data, safe=False)

    is_setted_filter = 0

    return page_data


def read_json(filepath):
    with open(filepath) as data_file:
        data = json.dumps(json.load(data_file))
    return data

@csrf_exempt
def set_filter(request):
    element = request.POST.get('element', '')
    json_data = request.POST.get('json_data', '')

    # element = 'mfcategory1'

    json_value = json.loads(json_data)

    global df_set_filter, is_setted_filter, filters_applied, df
    # local_df_set_filter = df_set_filter

    if json_value['value'] > 0:
        if element == "mfgroup":
            if json_value['value'] == 1:
                filters_applied['nunique'] = '==1'
            elif json_value['value'] == 2:
                filters_applied['nunique'] = '>1'
            else:
                filters_applied['nunique'] = '>0'

            key = 'categoryid1'
            if key in filters_applied:
                del filters_applied[key]

            key = 'categoryid2'
            if key in filters_applied:
                del filters_applied[key]

            key = 'categoryid3'
            if key in filters_applied:
                del filters_applied[key]

            key = 'brandid'
            if key in filters_applied:
                del filters_applied[key]
        elif element == "mfcategory1":
            filters_applied['categoryid1'] = '==' + str(json_value['value'])

            key = 'categoryid2'
            if key in filters_applied:
                del filters_applied[key]

            key = 'categoryid3'
            if key in filters_applied:
                del filters_applied[key]

            key = 'brandid'
            if key in filters_applied:
                del filters_applied[key]
        elif element == "mfcategory2":
            filters_applied['categoryid2'] = '==' + str(json_value['value'])

            key = 'categoryid3'
            if key in filters_applied:
                del filters_applied[key]

            key = 'brandid'
            if key in filters_applied:
                del filters_applied[key]
        elif element == "mfcategory3":
            filters_applied['categoryid3'] = '==' + str(json_value['value'])

            key = 'brandid'
            if key in filters_applied:
                del filters_applied[key]
        elif element == "mfbrand":
            filters_applied['brandid'] = '==' + str(json_value['value'])

        is_setted_filter = 1

        str_query = ' & '.join(['{}{}'.format(k, v) for k, v in filters_applied.items()])

        df_set_filter = df[
            ['nunique', 'Category_Name_1', 'Category_Name_2', 'Category_Name_3', 'Brand_Name', 'categoryid1', 'categoryid2', 'categoryid3',
             'brandid', 'count']]
        df_set_filter = df_set_filter.query(str_query)
    else:
        is_setted_filter = 0
        filters_applied = {}
        df_set_filter = df[
            ['nunique', 'Category_Name_1', 'Category_Name_2', 'Category_Name_3', 'Brand_Name', 'categoryid1', 'categoryid2', 'categoryid3',
             'brandid', 'count']]

    page_data = {
        'element': element,
        'retorno': 'ok'
    }

    return JsonResponse(page_data, safe=False)


@csrf_exempt
def testebq(request):
    page_data = {
        'retorno': 'ok'
    }

    return JsonResponse(page_data, safe=False)


def quantity_per_page(request):
    page_data = [{'item': 10, 'value': 10},
                 {'item': 20, 'value': 20},
                 {'item': 50, 'value': 50},
                 {'item': 75, 'value': 75},
                 {'item': 100, 'value': 100},
                 ]

    return JsonResponse(page_data, safe=False)


@csrf_exempt
def set_quantity_per_page(request):
    quantity = request.POST.get('quantity', 10)

    global page_size
    page_size = int(quantity)

    page_data = {
        'retorno': 'ok'
    }

    return JsonResponse(page_data, safe=False)


@csrf_exempt
def set_catalog(request):
    catalog_folder = request.POST.get('catalog', '')

    config = json.loads(open(DATA_ROOT + '/catalog.config').read())
    config[0]["last_opened"] = catalog_folder

    with open(DATA_ROOT + '/catalog.config', 'w') as f:
        json.dump(config, f)

    catalog_load()
    reports_load()

    page_data = {
        'retorno': 'ok'
    }

    return JsonResponse(page_data, safe=False)


@csrf_exempt
def clear_filters(request):
    global df_set_filter, is_setted_filter, filters_applied, df

    is_setted_filter = 0
    filters_applied = {}
    df_set_filter = df[
        ['nunique', 'Category_Name_1', 'Category_Name_2', 'Category_Name_3', 'Brand_Name', 'categoryid1', 'categoryid2', 'categoryid3',
         'brandid', 'count']]

    page_data = {
        'retorno': 'ok'
    }

    return JsonResponse(page_data, safe=False)


@csrf_exempt
def set_row_main(request):
    global df, df_changed, ics_data

    cluster_id_str = request.POST.get('cluster_id', 0)
    cluster_id = float(cluster_id_str)
    item_index = int(request.POST.get('item_index', 0))

    return_value = 1
    
    # Encontra o row_index do row_main do Cluster
    row_index_main = df.loc[(df['CLUSTER_ID'] == cluster_id) & df['ROW_MAIN'] == 1]['ROW_INDEX'].item()
    
    # Verifica se nao eh o mesmo item que foi selecionado
    if int(row_index_main) != item_index:
        # Set o novo item como ROW_MAIN
        df.loc[df['ROW_INDEX'] == item_index, 'ROW_MAIN'] = 1
        # Limpa o item anterior
        df.loc[df['ROW_INDEX'] == row_index_main, 'ROW_MAIN'] = 0

        # Salvar no arquivo os itens alterados para quando subir novamente realizar a alteracao
        # Verifica se o item alterado ja foi alterado anteriormente
        row_main_new = item_index
        row_main_old = row_index_main
        if len(df_changed) > 0:
            # Procura item atual dentro de items_update 
            if len(df_changed.loc[df_changed['ROW_INDEX'] == row_main_new]) > 0:
                df_changed.loc[df_changed['ROW_INDEX'] == row_main_new, 'ROW_MAIN'] = 1
            # Caso nao encontre adiciona mais um item
            else:
                df_changed = df_changed.append( 
                    {"CLUSTER_ID": cluster_id, "ROW_INDEX": item_index , 
                    "ROW_MAIN_OLD": row_main_old, 
                    "ROW_MAIN": 1, "WRONG" : "",  "COMMENT": "" }, ignore_index=True)
            
            # Verifica se item principal anterior foi alterado
            if len(df_changed.loc[df_changed['ROW_INDEX'] == row_main_old]) > 0:
                # Caso sim, retorna o valor de ROW_MAIN para 0
                df_changed.loc[df_changed['ROW_INDEX'] == row_main_old, 'ROW_MAIN'] = 0

        # Caso nao tenha, append novo item
        else:
            df_changed = df_changed.append( 
                {"CLUSTER_ID": cluster_id, "ROW_INDEX": item_index , 
                "ROW_MAIN_OLD": row_main_old, 
                "ROW_MAIN": 1, "WRONG" : "",  "COMMENT": "" }, ignore_index=True)
        
        # Armazena ateracoes no disco
        df_changed.to_json(items_updated_file_path + items_updated_file_name)
        # Set catalog as Draft again
        set_catalog_status(2)
    
    else:
        return_value = 0 


    page_data = {
        'retorno': return_value
    }

    return JsonResponse(page_data, safe=False)


@csrf_exempt
def get_comment(request):
    global df

    cluster_id_str = request.POST.get('cluster_id', '0')
    cluster_id = float(cluster_id_str)
    item_index = int(request.POST.get('item_index', 0))

    return_value = df.loc[df['ROW_INDEX'] == item_index, 'COMMENT'].item()

    page_data = {
        'retorno': return_value
    }

    return JsonResponse(page_data, safe=False)


@csrf_exempt
def set_comment(request):
    global df, df_changed, ics_data
    
    item_index = int(request.POST.get('item_index', '0'))
    comment_text = request.POST.get('comment_text', '')

    return_value = 1
    #TODO: tratar entrada de dados para evitar separate columns na variavel comment_text '"/:,
    if df.loc[df['ROW_INDEX'] == item_index, 'COMMENT'].item() != comment_text:
        df.loc[df['ROW_INDEX'] == item_index, 'COMMENT'] = comment_text
        # verifica se ja possui item no df_changed para persistir
        if len(df_changed.loc[df_changed['ROW_INDEX'] == item_index]) > 0:
            # Atualiza o item com comentario
            df_changed.loc[df_changed['ROW_INDEX'] == item_index, 'COMMENT'] = comment_text

        # Caso nao encontre adiciona mais um item
        else:
            df_changed = df_changed.append( 
                {"CLUSTER_ID": df.loc[df['ROW_INDEX'] == item_index, 'CLUSTER_ID'].item(), 
                "ROW_INDEX": item_index , 
                "ROW_MAIN_OLD": 0, 
                "ROW_MAIN": df.loc[df['ROW_INDEX'] == item_index, 'ROW_MAIN'].item(),
                "WRONG" : df.loc[df['ROW_INDEX'] == item_index, 'WRONG'].item(),
                "COMMENT": comment_text }, ignore_index=True)
        
        # Armazena ateracoes no disco
        df_changed.to_json(items_updated_file_path + items_updated_file_name)
        # Set catalog as Draft again
        set_catalog_status(2)
    
    else:
        return_value = 0
    
    page_data = {
        'retorno': return_value
    }

    return JsonResponse(page_data, safe=False)

@csrf_exempt
def set_wrong(request):
    global df, df_changed, ics_data

    cluster_id_str = request.POST.get('cluster_id', 0)
    cluster_id = float(cluster_id_str)
    item_index = int(request.POST.get('item_index', 0))

    return_value = 1
    # pega o valor de ROW_MAIN para verificar se o item e o principal do cluster
    # Nao pode excluir do cluster um item que eh o princial
    row_main = df.loc[df['ROW_INDEX'] == int(item_index)]['ROW_MAIN'].item()
    
    # Verifica se o item e um ROW_MAIN
    if row_main != 1:
        # Verifica se o item ja esta selecionado
        if df.loc[df['ROW_INDEX'] == item_index, 'WRONG'].item() == 1:
            df.loc[df['ROW_INDEX'] == item_index, 'WRONG'] = 0
        else:
            df.loc[df['ROW_INDEX'] == item_index, 'WRONG'] = 1
        
        # Verifica se ja possui item no df_changed para persistir
        if len(df_changed.loc[df_changed['ROW_INDEX'] == item_index]) > 0:
            # Atualiza o item com WRONG
            df_changed.loc[df_changed['ROW_INDEX'] == item_index, 'WRONG'] = \
                df.loc[df['ROW_INDEX'] == item_index, 'WRONG'].item()

        # Caso nao encontre adiciona mais um item
        else:
            df_changed = df_changed.append( 
                {"CLUSTER_ID": df.loc[df['ROW_INDEX'] == item_index, 'CLUSTER_ID'].item(), 
                "ROW_INDEX": item_index , 
                "ROW_MAIN_OLD": 0, 
                "ROW_MAIN": df.loc[df['ROW_INDEX'] == item_index, 'ROW_MAIN'].item(),
                "WRONG" : df.loc[df['ROW_INDEX'] == item_index, 'WRONG'].item(),
                "COMMENT": df.loc[df['ROW_INDEX'] == item_index, 'COMMENT'].item() }, ignore_index=True)
        
        # Armazena ateracoes no disco
        df_changed.to_json(items_updated_file_path + items_updated_file_name)

        # Set catalog as Draft again
        set_catalog_status(2)
    else:
        return_value = 0 

    page_data = {
        'retorno': return_value
    }

    return JsonResponse(page_data, safe=False)
  
@csrf_exempt
def get_catalog_info(request):
    page_data = get_catalog_status()

    return JsonResponse(page_data, safe=False)


def get_catalog_status():
    global catalog_version, catalog_name, catalog_status, catalog_date, ics_data

    catalog_status = ics_data.get_status()
    _status_last_changed = ics_data.get_last_changed()
    catalog_date = _status_last_changed.strftime('%d/%m/%Y %H:%M')
    catalog_name = "Products"
    catalog_version = "20180201"

    if str(catalog_status) == '2':
        _status_description = "Draft"
        _can_publish = False
        _can_process = True
    elif str(catalog_status) == '1':
        _status_description = "Ready to publish"
        _can_publish = True  # False to block function
        _can_process = False
    else:
        _status_description = "Published"
        _can_publish = False
        _can_process = False

    page_data = {
        'catalogName': catalog_name,
        'catalogVersion': catalog_version,
        'catalogStatus': _status_description,
        'catalogDate': catalog_date,
        'canProcess': _can_process,
        'canPublish': _can_publish
    }

    return page_data

@csrf_exempt
def get_statistics_info(request):
    global info_clusters_number, info_clusters_items, info_clusters_interacted

    page_data = {
        'clusterNumber': info_clusters_number,
        'clusterItems': info_clusters_items,
        'clustersInteracted': info_clusters_interacted,
    }

    return JsonResponse(page_data, safe=False)


# def home(request):
def clusters(request):
    """Renders the clusters page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        # AQUIAQUI
        'app/clusters.html',
        {
            'randvalue': '?v=' + datetime.now().strftime('%Y%m%d%H%M%S'),
        }
    )

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:home'))


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # Using set_password we apply HASH method to encrypt the password - Leandro 13/12/2017
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'app/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('user_name', 0)
        password = request.POST.get('pass_word', 0)

        user = authenticate(username=username, password=password)
        # User is authenticated
        if user:
            # User is activated
            if user.is_active:
                login(request, user)
                # SELECT HERE THE PAGE AFTER LOGIN
                page_data = {
                    'retorno': 'ok'
                }
                # return HttpResponseRedirect(reverse('app:home'))
                return JsonResponse(page_data, safe=False)
            else:
                # Account is not active
                page_data = {
                    'retorno': 'error1',
                    'message': 'Account is not active'
                }

                return JsonResponse(page_data, safe=False)
        else:
            # print("Someone tried to login and failed")
            # print("Username: {} and password {} ".format(username, password))
            # Invalid Login
            page_data = {
                'retorno': 'error2',
                'message': 'Invalid username or password'
            }

            return JsonResponse(page_data, safe=False)
    else:
        return render(request, 'app/login.html', {
            'randvalue': '?v=' + datetime.now().strftime('%Y%m%d%H%M%S'),
        })

class LoginPage(View):
    def get(self, request):
        return HttpResponse(LoginPage)


def settings(request):
    return render(
        request,
        'app/settings.html',
        {
            'title': 'Settings',
            'year': datetime.now().year,
            'randvalue': '?v=' + datetime.now().strftime('%Y%m%d%H%M%S'),
        }
    )


def home(request):
    return render(
        request,
        'app/home.html',
        {
            'title': 'Home',
            'year': datetime.now().year,
            'randvalue': '?v=' + datetime.now().strftime('%Y%m%d%H%M%S'),
        }
    )


def report(request):
    """Renders the report page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/report.html',
        {
            'title': 'Report',
            'message': 'Report Page.',
            'year': datetime.now().year,
            'randvalue': '?v=' + datetime.now().strftime('%Y%m%d%H%M%S'),
        }
    )


def graph(request):
    """Renders the report page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/graph.html',
        {
            'title': 'Graph',
            'message': 'Graph',
            'year': datetime.now().year,
            'randvalue': '?v=' + datetime.now().strftime('%Y%m%d%H%M%S'),
        }
    )


@csrf_exempt
def graph_render(request):
    global graph_html

    return HttpResponse(graph_html)


# ------------------
# REPORTS
# TODO: Mover para modulo de modelo de dados
# ------------------

def reports_load():
    global df_resume_n1_headers, df_resume_n2_headers, df_resume_n1_items, df_resume_n2_items, qt_cluster_sum, qt_name_sum

    # Report Cluster N1 - Considering Attributes
    # ------------------

    df_group = df.groupby(['CLUSTER_ID'])['Product_Name'].count().reset_index(name='GROUP').sort_values(['GROUP'], ascending=False)
    df_temp = pd.merge(df, df_group, how='inner', on='CLUSTER_ID')
    df_group_name = df_temp.groupby(['GROUP'])['Product_Name'].count().reset_index(name='QT_NAME').sort_values(['QT_NAME'], ascending=False)
    df_group_sum = df_group.groupby(['GROUP'])['CLUSTER_ID'].count().reset_index(name='QT_CLUSTER').sort_values(['GROUP'], ascending=True)
    df_resume_n1_items = pd.merge(df_group_name, df_group_sum, how='inner', on='GROUP')

    df_unique = df[df['nunique'] == 1]
    df_head_considering_attributes_unique = df_unique['CLUSTER_ID'].count()

    df_duplicated = df[df['nunique'] != 1]
    df_head_considering_attributes_duplicated = df_duplicated['CLUSTER_ID'].count()

    df_head_considering_attributes_clusters_duplicated = df_duplicated['CLUSTER_ID'].count()
    df_clusters_unique = df_temp[df_temp['nunique'] == 1]['CLUSTER_N1_ID'].count()

    # Total de Itens
    qtd_total_itens = df.shape[0]

    # Total Clusters
    qtd_total_clusters = len(df.groupby(['CLUSTER_ID'])['CLUSTER_ID'].count())

    # Quantidade de Clusters com itens duplicados
    #AQUIAQUI
    df2 = df[df['nunique'] > 1 ]
    qtd_clusters_duplicated = len(df2.groupby(['CLUSTER_ID'])['CLUSTER_ID'].count())

    # Quantidade de Clusters com Itens Unicos
    qtd_clusters_uniques = len(df[df['nunique'] == 1].count(1))

    # Quantidade de itens em Clusterizados
    qtd_itens_in_clusters = len(df[df['nunique'] >= 2].count(1))

    # Percentual de Itens Clusterizados
    per_itens_in_cluster = format_value('{} %', (qtd_itens_in_clusters / qtd_total_itens))

    # Quantidade de Parceiros envolvidos no catalogo
    #qtd_partners = len(df.groupby(['Partner_Name_1'])['Partner_Name_1'].count())
    qtd_partners = 1  # len(df.groupby(['Partner_ID'])['Partner_ID'].count())

    # Total de Itens transformados
    qtde_itens_transformed = '{} -> {}'.format(format_num(qtd_itens_in_clusters), format_num(qtd_clusters_duplicated)) 

    df_resume_n1_headers['a'] = {'text': 'Considering attributes', 'value': '0', 'signal': '(+)', 'color': 'indigo--text',
                                 'percent': '', 'percentColor': ''}
    df_resume_n1_headers['b'] = {'text': format_num(qtd_total_itens), 'value': '1',
                                'percent': '', 'percentColor': 'green--text'}
    df_resume_n1_headers['c'] = {'text': qtde_itens_transformed, 'value': '2',
                                  'percent': ' ({})'.format(per_itens_in_cluster), 'percentColor': 'green--text'}
    df_resume_n1_headers['d'] = {'text': format_num(qtd_total_clusters), 'value': '3',
                                  'percent': '', 'percentColor': 'amber--text'}
    df_resume_n1_headers['e'] = {'text': format_num(qtd_clusters_duplicated), 'value': '4',
                                  'percent': '', 'percentColor': ''}
    df_resume_n1_headers['f'] = {'text': format_num(qtd_clusters_uniques), 'value': '5',
                                  'percent': '', 'percentColor': ''}
    df_resume_n1_headers['g'] = {'text': format_num(qtd_itens_in_clusters), 'value': '6',
                                  'percent': '', 'percentColor': ''}
    df_resume_n1_headers['h'] = {'text': format_num(qtd_clusters_uniques), 'value': '7',
                                  'percent': '', 'percentColor': ''}
    df_resume_n1_headers['i'] = {'text': str(per_itens_in_cluster), 'value': '8',
                                  'percent': '', 'percentColor': ''}
    df_resume_n1_headers['j'] = {'text': format_num(qtd_partners), 'value': '9',
                                  'percent': '', 'percentColor': ''}
    
    qt_cluster_sum = df_resume_n1_items['QT_CLUSTER'].sum()
    qt_name_sum = df_resume_n1_items['QT_NAME'].sum()

    df_resume_n1_items['PC_CLUSTER'] = df_resume_n1_items['QT_CLUSTER'] / qt_cluster_sum
    df_resume_n1_items['PC_NAME'] = df_resume_n1_items['QT_NAME'] / qt_name_sum

    df_resume_n1_items['PC_CLUSTER'] = df_resume_n1_items.apply(lambda row: format_value('{0:.1f}%', row['PC_CLUSTER']),
                                                                axis=1)
    df_resume_n1_items['PC_NAME'] = df_resume_n1_items.apply(lambda row: format_value('{0:.1f}%', row['PC_NAME']),
                                                             axis=1)
    df_resume_n1_items['QT_CLUSTER'] = df_resume_n1_items.apply(lambda row: format_num(row['QT_CLUSTER']), axis=1)
    df_resume_n1_items['QT_NAME'] = df_resume_n1_items.apply(lambda row: format_num(row['QT_NAME']), axis=1)

    # Report Cluster N2 - Disregarding Attributes
    # ------------------
    df_group = df.groupby(['CLUSTER_N1_ID'])['Product_Name'].count().reset_index(name='GROUP').sort_values(['GROUP'],
                                                                                                   ascending=False)
    df_temp2 = pd.merge(df, df_group, how='inner', on='CLUSTER_N1_ID')
    df_group_name = df_temp2.groupby(['GROUP'])['Product_Name'].count().reset_index(name='QT_NAME').sort_values(['QT_NAME'],
                                                                                                        ascending=False)
    df_group_sum = df_group.groupby(['GROUP'])['CLUSTER_N1_ID'].count().reset_index(name='QT_CLUSTER').sort_values(
        ['GROUP'], ascending=True)
    df_resume_n2_items = pd.merge(df_group_name, df_group_sum, how='inner', on='GROUP')

    df_unique = df[df['nunique'] == 1]
    df_head_disregarding_attributes_unique = df_unique['CLUSTER_N1_ID'].count()
    df_duplicated = df[df['nunique'] != 1]
    df_head_disregarding_attributes_duplicated = df_duplicated['CLUSTER_N1_ID'].count()
    df_head_disregarding_attributes_clusters_duplicated = df_duplicated['CLUSTER_N1_ID'].count()

    df_resume_n2_headers['a'] = {'text': 'Disregarding attributes', 'value': '0', 'signal': '-', 'color': 'red--text',
                                 'percent': '', 'percentColor': ''}
    df_resume_n2_headers['b'] = {'text': str(df_head_disregarding_attributes_unique), 'value': '1', 'signal': '-',
                                 'color': 'red--text', 'percent': '50%', 'percentColor': 'green--text'}
    df_resume_n2_headers['c'] = {'text': str(df_head_disregarding_attributes_duplicated), 'value': '2', 'signal': '+',
                                 'color': 'indigo--text', 'percent': '50%', 'percentColor': 'amber--text'}
    df_resume_n2_headers['d'] = {'text': str(df_head_disregarding_attributes_clusters_duplicated), 'value': '3',
                                 'signal': '+', 'color': 'indigo--text', 'percent': '', 'percentColor': ''}
    df_resume_n2_headers['e'] = {'text': '99', 'value': '4', 'signal': '+', 'color': 'indigo--text', 'percent': '',
                                 'percentColor': ''}

    qt_cluster_sum = df_resume_n2_items['QT_CLUSTER'].sum()
    qt_name_sum = df_resume_n2_items['QT_NAME'].sum()

    df_resume_n2_items['PC_CLUSTER'] = df_resume_n2_items['QT_CLUSTER'] / qt_cluster_sum
    df_resume_n2_items['PC_NAME'] = df_resume_n2_items['QT_NAME'] / qt_name_sum

    df_resume_n2_items['PC_CLUSTER'] = df_resume_n2_items.apply(lambda row: format_value('{0:.1f}%', row['PC_CLUSTER']),
                                                                axis=1)
    df_resume_n2_items['PC_NAME'] = df_resume_n2_items.apply(lambda row: format_value('{0:.1f}%', row['PC_NAME']),
                                                             axis=1)
    df_resume_n2_items['QT_CLUSTER'] = df_resume_n2_items.apply(lambda row: format_num(row['QT_CLUSTER']), axis=1)
    df_resume_n2_items['QT_NAME'] = df_resume_n2_items.apply(lambda row: format_num(row['QT_NAME']), axis=1)
    del df_temp, df_group, df_group_name, df_group_sum
    print("Reports Loaded")

def report_n1_headers(request):
    page_data = JsonResponse(df_resume_n1_headers, safe=False)

    return page_data


def report_n2_headers(request):
    page_data = JsonResponse(df_resume_n2_headers, safe=False)

    return page_data


def report_n1_items(request):
    page_data = json.loads(df_resume_n1_items.reset_index().to_json(orient='records'))
    page_data = JsonResponse(page_data, safe=False)

    return page_data


def report_n2_items(request):
    page_data = json.loads(df_resume_n2_items.reset_index().to_json(orient='records'))
    page_data = JsonResponse(page_data, safe=False)

    return page_data


def format_value(mask, value):
    return mask.format(value * 100)


def format_num(value):
    return format(value, ',d').replace(',', '.')


def set_catalog_status(status):
    global ics_data, catalog_status, catalog_date
    # Set catalog as Draft again
    ics_data.set_status(status)
    catalog_status = ics_data.get_status()
    _status_last_changed = ics_data.get_last_changed()
    catalog_date = _status_last_changed.strftime('%d/%m/%Y %H:%M')


@csrf_exempt
def schedule_process(request):
    global ics_data, items_updated_file_path, items_updated_file_name, catalog_lock_status
    print("schedule_process")
    data_changed_catalog = json.loads(open(items_updated_file_path + items_updated_file_name).read())

    if len(data_changed_catalog) == 0:
        return_data = "Nothing to process"
    else:
        status = ics_data.get_lock_status()

        if status != "":
            if int(status) == 0:
                return_data = ics_data.schedule_process()
            else:
                return_data = "Already processing"
        else:
            return_data = ""

    page_data = {
        'retorno': return_data
    }

    return JsonResponse(page_data, safe=False)


@csrf_exempt
def process_catalog_finished(request):
    global ics_data, config, file_catalog_dir, df, df_changed, df_items_count, df_all_clusters, \
        df_set_filter, filters_applied, page_size, df_resume_n1_headers, df_resume_n2_headers, df_resume_n1_items, \
        df_resume_n2_items, qt_cluster_sum, qt_name_sum, graph_html, catalog_name, catalog_version, catalog_status, \
        catalog_date, info_clusters_number, info_clusters_items, info_clusters_interacted, ics_data, \
        items_updated_file_path, items_updated_file_name, catalog_lock_status

    status = ics_data.get_lock_status()

    if int(status) == 0 and int(catalog_lock_status) == 1:
        return_process = "Done"
        catalog_lock_status = "0"
    elif int(status) == 1 and int(catalog_lock_status) == 0:
        # locked now
        return_process = "Processing"
        catalog_lock_status = "1"
    else:
        return_process = ""

    if return_process == "Done":
        set_catalog_status(1)
        return_data = "Done"

        config = ''
        file_catalog_dir = ''
        df = []
        df_changed = []
        df_items_count = []
        df_all_clusters = []
        df_set_filter = []
        filters_applied = {}
        page_size = 20
        df_resume_n1_headers = {}
        df_resume_n2_headers = {}
        df_resume_n1_items = []
        df_resume_n2_items = []
        qt_cluster_sum = 0
        qt_name_sum = 0
        graph_html = ''
        catalog_name = ''
        catalog_version = ''
        catalog_status = ''
        catalog_date = ''
        info_clusters_number = 0
        info_clusters_items = 0
        info_clusters_interacted = 0
        ics_data = None
        items_updated_file_path = ""
        items_updated_file_name = ""
        catalog_load()
        reports_load()
    else:
        return_data = ""

    page_data = {
        'retorno': return_data
    }

    return JsonResponse(page_data, safe=False)


@csrf_exempt
def publish_catalog(request):
    global ics_data
    global df
    
    return_data = ics_data.publish_catalog(df)

    if return_data == "Done":
        set_catalog_status(3)
    else:
        pass
        #TODO: Devolver erro na tela apos publicacao do catalogo
    page_data = {
        'retorno': return_data
    }

    return JsonResponse(page_data, safe=False)


catalog_load()
reports_load()
