# Django authentication
from django.contrib.auth.models import User
from app.models import *
from django.core.paginator import Paginator
import openpyxl, os, sys, re
from django.conf import settings
from django.db import IntegrityError

#===========================================================================================
# Excel to DB insertion 
# ==========================================================================================
#

def insert_into_db(file_ins, file_path):
    path = settings.MEDIA_ROOT+file_path

    wb_obj = openpyxl.load_workbook(path) 
    sheet_obj = wb_obj.active 

    total_rows = sheet_obj.max_row 
    total_columns = sheet_obj.max_column

    msg = "Total Rows: {0}, Total Columns: {1}".format(total_rows- 1 , total_columns)

    # Loop will print all columns name 
    for row in range(2, total_rows + 1): 

        category = sheet_obj.cell(row = row, column = 1).value
        sub_category = sheet_obj.cell(row = row, column = 2).value
        brand = sheet_obj.cell(row = row, column = 3).value

        cat, sub_cat, brand_ins = category_sub_brand_insertion(category, sub_category, brand)
       
        
        record = RecordsManagement(
            record_file = file_ins,
            is_active = file_ins.is_active,
            category = cat,
            sub_category = sub_cat,
            brand = brand_ins,
            contact_person = sheet_obj.cell(row = row, column = 4).value,
            contact_number = sheet_obj.cell(row = row, column = 5).value,
            email = sheet_obj.cell(row = row, column = 6).value,
        )

        record.save()
        
    return msg


#===========================================================================================
# Category & Sub Category, Brand Insertion   
# ==========================================================================================
# 

def category_sub_brand_insertion(category, sub_category, brand):
    
    cat = None
    sub_cat = None
    brand_ins = None

    try:
        cat_insert = Category(
            category_name = category.strip(),
            category_is_parent = True,
        )

        cat = cat_insert.save()
    
    except IntegrityError:
        cat = Category.objects.get(category_name = category.strip())

    #===========================================================================================
    # Sub category   
    #===========================================================================================
        
    if cat is not None:
        sub_category = sub_category.strip()

        try:
            cat_insert = Category(
                category_name = sub_category.strip(),
                category_is_parent = False,
                category_parent_id = cat,
            )
            sub_cat = cat_insert.save()
        except IntegrityError:
            sub_cat = Category.objects.get(category_name = sub_category.strip(), category_is_parent = False)
    
    #===========================================================================================
    #   Brands Insertion
    #===========================================================================================

    print(category, sub_category, brand)

    try:
        brand_insert = Brand(
            brand_name = brand.strip(),
        )

        brand_ins = brand_insert.save()
    except IntegrityError: 
        brand_ins = Brand.objects.get(brand_name = brand.strip())
    
    return cat, sub_cat, brand_ins


def RecordsList():
    file_ins = FileSubmission.objects.exclude(is_active = False).latest('id')

    records = RecordsManagement.objects.filter(record_file = file_ins)
    records = records.select_related('category', 'sub_category','brand', 'record_file')
    records = records.values('category__category_name', 'sub_category__category_name', 'brand__brand_name', 
                'contact_person', 'contact_number', 'email', 'is_active', 'record_file__uploaded_on')

            
    print(records)
    return records



