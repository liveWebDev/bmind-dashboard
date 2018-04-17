from catalog import Catalog
from catalog import STATUS
from settings import Settings


def main():
    # Load settings to Class attributes
    catalog = Catalog(Settings.get())

    status = catalog.get_schedule_status()

    if int(status) == 1:
        print("Scheduled!")
        catalog.unschedule_process()
        print("Starting processing")
        if catalog.process_catalog(False) == "Done":
            if catalog.copy_processed_catalog_to_web() == "Done":
                catalog.set_unlocked()
                print("Process Finished")


if __name__ == '__main__':
    VERIFICATION_TOKEN = ""
    main()
