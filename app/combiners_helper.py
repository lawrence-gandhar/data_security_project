# Django authentication
from django.contrib.auth.models import User
from app.models import *
from django.db import IntegrityError


#===========================================================================================
# Category & Sub Category, Brand Insertion   
# ==========================================================================================
# 
def category_sub_brand_insertion(category, sub_category, brand, pe):
    
    cat = None
    sub_cat = None
    brand_ins = None
    pe_ins = None

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
        if sub_category is not None:
            try:
                cat_insert = Category(
                    category_name = sub_category.strip(),
                    category_is_parent = False,
                    category_parent_id = cat,
                )
                sub_cat = cat_insert.save()
            except IntegrityError:
                try:
                    sub_cat = Category.objects.get(category_name = sub_category.strip(), category_is_parent = False)
                except Category.DoesNotExist:
                    sub_cat = None
            
            
    #===========================================================================================
    #   Brands Insertion
    #===========================================================================================

    if brand is not None:
        try:
            brand_insert = Brand(
                brand_name = brand.strip(),
            )

            brand_ins = brand_insert.save()
        except IntegrityError: 
            brand_ins = Brand.objects.get(brand_name = brand.strip())
            

    #===========================================================================================
    #   Previous Exhibition Insertion
    #===========================================================================================

    if pe is not None:
        try:
            pe_insert = PreviousExhibition(
                name = pe.strip(),
            )

            pe_ins = pe_insert.save()
        except IntegrityError: 
            pe_ins = PreviousExhibition.objects.get(name = pe.strip())
    
    return cat, sub_cat, brand_ins, pe_ins


#==========================================================================================
#   Category, Sub Category & Brand Lists
#==========================================================================================
#
def CategoryList():
    return Category.objects.filter(is_active = True, category_is_parent = True,)
    
    
def SubCategoryList(cate = None):
    sub_cat = Category.objects.filter(is_active = True, category_is_parent = False,)
    if cate is not None and len(cate)>0:
        sub_cat = sub_cat.filter(category_parent_id__in = cate)
    return sub_cat    
    
    
def BrandList(cat = None, sub_cat = None):    
    return Brand.objects.filter(is_active = True,).order_by('brand_name')
    

def PEList():
    return PreviousExhibition.objects.filter(is_active = True,).order_by('name')

