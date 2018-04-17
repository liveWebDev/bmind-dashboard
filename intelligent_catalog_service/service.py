from intelligent_catalog_service.catalog import Catalog
from intelligent_catalog_service.catalog import STATUS
from intelligent_catalog_service.settings import Settings


def main():
    # Load settings to Class attributes
    catalog = Catalog(Settings.get())
    catalog.set_status(STATUS["Ready"])
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # utilizado para Carregar arquivos CSV para o BIGQUERY  
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    source_file_name = "/Users/leandrolopes/git/pandas_jupyter/ExtracaoEsporteLazer_2103.txt"
    dataset_name = 'product_match'
    table_name = 'esportelazer_2103'
    
    #return_check = catalog.load_data(source_file_name, dataset_name, table_name)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    return_check = catalog.check_new_version()
    return_check = "Yes"
    # Check new version is available
    if return_check == "Yes":
        # if Yes, load new catalog version
        return_load = catalog.load_new_version()
        return_load = "Done"

        if return_load == "Done":
            # if Done, process new catalog version
            return_catalog = catalog.process_catalog(True)
        else:
            # Error found
            print("Error found")
    elif return_check != "No":
        # Error found
        print("Error found 2")
    else:
        # Done, nothing to do
        print("Done")


def mytestmain():
    # Load settings to Class attributes
    catalog = Catalog(Settings.get())
    catalog.set_status(STATUS["Ready"])
    catalog.run_other()


if __name__ == '__main__':
    main()
