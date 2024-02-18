from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_elastic import StorageElastic
from common_modules.logger.mnt_logging import MntLogging as ScraperLog


# add storage info here?
class ScraperBase:
    """
    Constructor for ScraperMgr. It will be managing the Scraping jobs
    Every Scraping Job must have name associated to it which will be
    used as key in the data_source_table_mapping table to get the
    capabilities of the given data source

    :param scraper_job: Scraper Job Object, Can be LinkedinJob,MeetupJob etc.
    :type object: Job class Object
    :param storage: Type of storage this job is going to use
    :type storage: Storage Class object
    """

    def __init__(self, url_table: str = None, keyword_table: str = None,
                 data_table: str = None, query_string: str = None,
                 resMgr: ResourceMgr = ResourceMgr(StorageElastic()),
                 logger=ScraperLog().setloglevel('debug')):

        # Local variables to track scraper specific tables
        self._logger = logger
        self.resMgr = resMgr

        self.url_table_name = url_table
        self.keyword_table_name = keyword_table
        self.data_table_name = data_table
        self.query_string = query_string

    def setup(self):

        # Validate everything
        if self.url_table_name is None and self.keyword_table_name is None:
            raise Exception("Both URL table and key table is None")

        if self.query_string is None or self.data_table_name is None:
            raise Exception("Query String or data table is None")

        # Make sure data source specific tables exist in DB else create them
        try:
            # Check if URL table needs to be created
            if self.url_table_name is not None and \
                    not self.resMgr.index_exist(self.url_table_name):
                # create it
                ScraperLog("Creating URL Table %s" % self.url_table_name)
                self.resMgr.index_create(self.url_table_name)

            # Check if keyword table needs to be created
            if self.keyword_table_name is not None and \
                    not self.resMgr.index_exist(self.keyword_table_name):
                # create it
                ScraperLog("Creating KEYWORD Table %s" % self.keyword_table_name)
                self.resMgr.index_create(self.keyword_table_name)

            # Check if data table needs to be created
            if self.data_table_name is not None and \
                    not self.resMgr.index_exist(self.data_table_name):
                # create it
                ScraperLog("Creating Data Table %s" % self.data_table_name)
                self.resMgr.index_create(self.data_table_name)

        except Exception as e:
            ScraperLog(e)
            return None

    def __del__(self):
        """
        Destructor No Cleanup needed
        """
        pass

    def get_url_list(self):
        # call resource manager to query
        url_list = self.resMgr.search(index=self.url_table_name, search_param=self.query_string, raw=True)
        return url_list

    def write_in_url_table(self, key: str, data: dict):
        self.resMgr.update(index=self.url_table_name, key=key, data=data)

    def write_in_data_table(self, key: str, data: dict):
        self.resMgr.update(index=self.data_table_name, key=key, data=data)

    def get_keyword_list(self):
        # call resource manager to query
        keyword_list = self.resMgr.search(index=self.keyword_table_name, search_param=self.query_string)
        return keyword_list
