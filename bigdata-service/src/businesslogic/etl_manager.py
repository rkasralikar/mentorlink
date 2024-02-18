"""  Etl Manager class
Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: This class implements
the Schema Etls.
"""
from src.businesslogic.etl_jobs import EtlJobs
import threading
from datetime import datetime
from datetime import timedelta
import time
from common_modules.logger.mnt_logging import MntLogging as MyLog


class EtlManager:
    def __init__(self, etl_objs: list[EtlJobs], exp_time):
        self.etl_objs = etl_objs
        self.etl_start = datetime.utcnow()
        self.threshold_time = timedelta(days=exp_time)
        self.sleep_time = exp_time

    def start(self):
        done = False
        while True:
            if (datetime.utcnow() <= self.etl_start) and (done is True):
                time.sleep(self.sleep_time)
                done = False
                continue
            else:
                self.etl_start = datetime.utcnow() + self.threshold_time
                thread_thr = []
                for etl in self.etl_objs:
                    retry_count = 5
                    while retry_count > 0:
                        if not etl.login():
                            retry_count -= 1
                        else:
                            break
                    if retry_count:
                        MyLog().getlogger().debug("Starting etl")
                        thr = threading.Thread(target=etl.start())
                        thr.start()
                        thread_thr.append(thr)

                MyLog().getlogger().debug("Job Finished")
                done = True
                for thr in thread_thr:
                    thr.join()
