from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_elastic import StorageElastic
from common_modules.logger.mnt_logging import MntLogging as MyLog


def clear_db_table(table_name: list[str], resmgr):
    for table in table_name:
        MyLog().getlogger().debug(f"Deleting Table {table}")
        try:
            resmgr.delete(index=table, force=True)
        except Exception as ex:
            MyLog().getlogger().info(ex)
            MyLog().getlogger().critical("Delete failed for index:%s" % table)


def main():
    tables = [""]
    clear_db_table(tables, ResourceMgr(StorageElastic()))


if __name__ == "__main__":
    main()
