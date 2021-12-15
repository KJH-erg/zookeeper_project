from google.cloud import storage
import os
class googleAPI():
    def __init__(self):
        self.storage_client = storage.Client()
        self.cnt =0

    def download_blob(self,source_blob_name):
        try:
            bucket = self.storage_client.bucket('zookeeper_project')
            dest = './csv_tmp/'+source_blob_name
            blob = bucket.blob('csv/'+source_blob_name)
            blob.download_to_filename(dest)
            print('Downloaded storage object '+source_blob_name+' is downloaded')
        except:
            print('error occured plz check your file_name')
    def create_instance(self,id):
        self.cnt+=1
        os.system("""gcloud compute instances delete {}""".format(id))
        os.system("""gcloud beta compute instances create {} --project=quick-replica-330115 --zone=asia-northeast3-a --machine-type=n1-standard-1
        --network-interface=network-tier=PREMIUM,subnet=default --maintenance-policy=MIGRATE --service-account=893801870030-compute@developer.gserviceaccount.com
        --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,
        https://www.googleapis.com/auth/service.management.readonly,
        https://www.googleapis.com/auth/trace.append
        --min-cpu-platform=Automatic --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --reservation-affinity=any --source-machine-image=worker""".format('worker'+str(self.cnt)))