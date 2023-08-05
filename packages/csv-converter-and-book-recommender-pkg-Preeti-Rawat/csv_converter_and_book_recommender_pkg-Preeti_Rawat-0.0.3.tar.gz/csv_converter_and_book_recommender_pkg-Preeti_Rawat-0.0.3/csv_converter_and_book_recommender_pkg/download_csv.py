import csv
from django.http import HttpResponse

#This class is responsible for creating the csv file from the model data and downloading it.
class CSV_Downloader(object):
    #constructor to initialize,  
    #data:  it is model data which forms the content of the csv file.
    #content type:  initialize the content type of csv file
    #content_disposition: initialize the content_disposition of the download csv file
    def __init__(self, data):
        self.data=data
        self.content_type='text/csv'
        self.content_disposition = 'attachment;filename=export.csv'
        
    #method downloads the csv file using the model data as content.
    def download_csv_file(self):
        metadata=self.data.model._meta
        model =self.data.model
        csv_file_response = HttpResponse(content_type=self.content_type)
        # force download.
        csv_file_response['Content-Disposition'] = self.content_disposition
        #csv writer to create the response
        csv_writer=csv.writer(csv_file_response)
        name_of_fields=[field.name for field in metadata.fields]
        #header information
        csv_writer.writerow(name_of_fields)
        #writes the row content of csv file
        for unit in self.data:
            csv_writer.writerow([getattr(unit, field) for field in name_of_fields])
        print(csv_file_response)
        return csv_file_response