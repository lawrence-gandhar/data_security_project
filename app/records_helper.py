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

        category_insertion(sheet_obj.cell(row = row, column = 1).value, sheet_obj.cell(row = row, column = 2).value)
       
        for col in range(3, total_columns + 1): 
            cell_obj = sheet_obj.cell(row = row, column = col) 
          
    print(msg)


#===========================================================================================
# Category & Sub Category Insertion   
# ==========================================================================================
# 

def category_insertion(category, sub_category):
    
    cat = None

    try:
        cat_insert = Category(
            category_name = category.strip(),
            category_is_parent = True,
        )

        cat = cat_insert.save()
    
    except IntegrityError:
        cat = Category.objects.get(category_name = category.strip())

    # Sub category   
    # 
        
    if cat is not None:
        sub_category = sub_category.strip()

        try:
            cat_insert = Category(
                category_name = sub_category.strip(),
                category_is_parent = False,
                category_parent_id = cat,
            )
            cat_insert.save()
        except IntegrityError:
            pass

#====================================================================================
#   Brands Insertion
#====================================================================================