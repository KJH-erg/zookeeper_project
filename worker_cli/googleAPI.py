from google.cloud import storage
class googleAPI():
    def __init__(self):
        self.storage_client = storage.Client()

    def download_blob(self,source_blob_name):
        try:
            bucket = self.storage_client.bucket('zookeeper_project')
            dest = './csv_tmp/'+source_blob_name
            blob = bucket.blob('csv/'+source_blob_name)
            blob.download_to_filename(dest)
            print('Downloaded storage object '+source_blob_name+' is downloaded')
        except:
            print('error occured plz check your file_name')