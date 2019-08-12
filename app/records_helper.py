# Django authentication
from django.contrib.auth.models import User
from app.models import *
from django.core.paginator import Paginator
import openpyxl, os, sys, re
from django.conf import settings
from django.db import IntegrityError


def insert_into_db(file_path):
    path = settings.MEDIA_ROOT+file_path

    wb_obj = openpyxl.load_workbook(path) 
    sheet_obj = wb_obj.active 

    msg = "Total Rows: {0}, Total Columns: {1}".format(sheet_obj.max_row - 1 , sheet_obj.max_column)

    total_rows = sheet_obj.max_row 
    total_columns = sheet_obj.max_column


    # Loop will print all columns name 
    for row in range(2, total_rows + 1): 

        category_insertion(sheet_obj.cell(row = row, column = 1).value)
        sub_category_insertion(sheet_obj.cell(row = row, column = 1).value)

        for col in range(1, total_columns + 1): 
            cell_obj = sheet_obj.cell(row = row, column = col) 
          
    print(msg)


def category_insertion(category):
    try:
        cat_insert = Category(
            category_name = category.strip(),
            category_is_parent = True,
        )

        cat_insert.save()
    except IntegrityError:
        pass
        

def sub_category_insertion(category, sub_category):

    #category = category.upper().strip()

    cat = Category.objects.filter(category_name__contains = category)

    if a == b:
        pass
    try:
        cat_insert = Category(
            category_name = category.strip(),
            category_is_parent = True,
        )

        cat_insert.save()
    except IntegrityError:
        pass