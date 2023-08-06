from django.core.files.storage import FileSystemStorage
import boto3 
import os
from django.conf import settings

class UploadToS3Folder:
    
    #   generate a filename for upload specific to a client
    def generate_file_name(self,company_name,myfile):
        file_name = company_name.replace(" ", "_")+'__'+myfile.name.replace(" ", "_")
    
        return file_name
    
    #   retrieve the file from local upload and determine which folder it should be saved to
    def rename_and_upload_file_to_s3_folder(self, file_name, bucket, folder):

        object_key = file_name
        save_path = settings.MEDIA_ROOT
        complete_name = os.path.join(save_path, object_key)
        
        # Upload the file to S3
        s3_client = boto3.client('s3')
        
         #   expense type determines the S3 Bucket folder to ssave to
        if('travel'==folder):
            response = s3_client.upload_file(complete_name, bucket, 'travel/{}'.format(file_name))
        elif('food'==folder):
            response = s3_client.upload_file(complete_name, bucket, 'food/{}'.format(file_name))
        elif('accomodation'==folder):
            response = s3_client.upload_file(complete_name, bucket, 'accomodation/{}'.format(file_name))
        elif('equipment'==folder):
            response = s3_client.upload_file(complete_name, bucket, 'equipment/{}'.format(file_name))
        else: 
            response = s3_client.upload_file(complete_name, bucket, object_key)
        
        return response
      

if __name__ == '__main__':
    utsf = UploadToS3Folder()        
        