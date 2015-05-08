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
                    logging.info("Trying to upload file %s!"%(ele))
                    if os.access(ele,os.W_OK):
                        self.check_quota()
                        logging.info('Ready to upload file %s' % ele)
                        try:
                            with open(ele,'rb') as file:
                                self.client.put_file(ele,file)
                                logging.info('Uploaded %s' % ele)
                            os.remove(ele)
                        except Exception as e:
                            logging.error(str(e))
                            break
                    else:
                        logging.info("Failed to get lock!")

    def check_quota(self):
        logging.info("Checking quota of Dropbox")
        while True:
            info = self.client.account_info()
            logging.info("Current Quota {0}".format(info['quota_info']['quota']-info['quota_info']['normal']))
            if (info['quota_info']['quota']-info['quota_info']['normal']) < 10000000:
                logging.info("Not enough space");
                folder_metadata = self.client.metadata('/')
                logging.info("Removing some files for space {0}".format(folder_metadata['contents'][0]['path']))
                self.client.file_delete(folder_metadata['contents'][0]['path'])
            else:
                logging.info("Check quota Okay!");
                break
