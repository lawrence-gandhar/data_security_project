# Django authentication
from django.contrib.auth.models import User
from app.models import UserProfile, AppPermission
from django.core.paginator import Paginator
import openpyxl, os, sys, re
from django.conf import settings


def insert_into_db(file_path):
    path = settings.MEDIA_ROOT+file_path

    wb_obj = openpyxl.load_workbook(path) 
    sheet_obj = wb_obj.active 

    msg = "Total Rows: {0}, Total Columns: {1}".format(sheet_obj.max_row - 1 , sheet_obj.max_column)

    total_rows = sheet_obj.max_row 
    total_columns = sheet_obj.max_column


    # Loop will print all columns name 
    for row in range(2, total_rows + 1): 
        for col in range(1, total_columns + 1): 
            cell_obj = sheet_obj.cell(row = row, column = col) 
             

    print(msg)


