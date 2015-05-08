import threading
import dropbox
import logging
import time
import os
from config import Config

class DropboxStorage(threading.Thread):

    def __init__(self):
        super(DropboxStorage,self).__init__(name = 'Dropbox-Thread')
        self.is_working = False
        self.access_token = Config.DROPBOX_TOKEN
        self.client = dropbox.client.DropboxClient(self.access_token)
        logging.info('Login Dropbox! %s'%self.client.account_info())



    def start_uploader(self):
        self.is_working = True
        self.start()

    def stop_uploader(self):
        self.is_working = False
        self.join()

    def run(self):
        while self.is_working:
            time.sleep(1)
            files = os.listdir(Config.STORAGE_PATH)
            for ele in files:
                if '.flv' in ele:
                    if os.access(ele,os.R_OK|os.W_OK):
                        self.check_quota()
                        self.log.info('Ready to upload file %s' % ele)
                        try:
                            with open(ele,'rb') as file:
                                self.client.put_file(ele,file)
                                self.log.info('Uploaded %s' % ele)
                            os.remove(ele)
                        except Exception as e:
                            self.log.error(str(e))
                            break

    def check_quota(self):
        self.log.info("Checking quota of Dropbox")
        while True:
            info = self.client.account_info()
            self.log.info("Current Quota {0}".format(info['quota_info']['quota']-info['quota_info']['normal']))
            if (info['quota_info']['quota']-info['quota_info']['normal']) < 10000000:
                self.log.info("Not enough space");
                folder_metadata = self.client.metadata('/')
                self.log.info("Removing some files for space {0}".format(folder_metadata['contents'][0]['path']))
                self.client.file_delete(folder_metadata['contents'][0]['path'])
            else:
                self.log.info("Check quota Okay!");
                break
