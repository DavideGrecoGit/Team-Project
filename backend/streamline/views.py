import re
import pandas as pd

from django.shortcuts import render
from streamline.models import Url_table, Tables
from django.conf import settings

from .utils import html_to_csv, pdf_to_csv, generics

# Path to which resulting csv files will be saved (will be .../cs20-main/backend/saved)
CSV_PATH = settings.CSV_DIR


'''
 Extracts table data from HTML
'''
def get_page_data_HTML(request):
    
    #Get Url
    url = request.GET.get('topic', None)
    print('topic-HTML:', url)

    #store URL
    web_page = Url_table.objects.create(url=url)
    #process page
    table_count = html_to_csv.extract(url, web_page, save_path=CSV_PATH)
    
    context_dict = generics.create_context(web_page, table_count)

    return render(request, 'streamline/preview_page.html', context=context_dict)

'''
Extracts table data from PDF
'''
def get_page_data_pdf(request):
    url = request.GET.get('topic', None)
    pages = request.GET.get('pages', None)

    print('topic-PDF:', url)
    print('pages-PDF:', pages)

    #store URL
    file = Url_table.objects.create(url=url)
    table_count = 0

    regex = "^all$|^\s*[0-9]+\s*((\,|\-)\s*[0-9]+)*\s*$"

    # Check if page input is valid
    if (re.search(regex, pages)):

        print("Valid input")

        #downloads pdf from right click
        pdf_path = pdf_to_csv.download_pdf(url, save_path=CSV_PATH)
        #convert its table(s) into csv(s) and get table count
        table_count = pdf_to_csv.download_pdf_tables(pdf_path, file, save_path=CSV_PATH, pages=pages)
    
    else:
         print("Invalid input")

    context_dict = generics.create_context(file, table_count)

    return render(request, 'streamline/preview_page.html', context=context_dict)


def download_page(request, url_id=0, table_id=0):
    #pk1 is Url_table.id --- p2k is Tables.Table_Id
    #if pk2 == 0 then download all

    file_path = generics.create_zip(CSV_PATH, url_id, table_id)
    return generics.create_file_response(file_path)
    
    





    



