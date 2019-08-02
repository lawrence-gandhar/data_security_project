#
#	module written by Lawrence Gandhar
#	Date : 25 June 2019
#

import re

from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

from app.models import *
from django.http import QueryDict

register = template.Library()


@register.simple_tag
def paginate(value, query_string):
	html = []
	
	try:
		min_index = 1	
		max_index = value.paginator.num_pages
		current_value = value.number

		if value is None:
			pass

		else:

			# Handling query string parameters
			#======================================================================

			q_string = []
			query_string = dict(QueryDict(query_string))

			query_string.pop("page",None)
			for x in query_string.items():
				x = list(x)
				for j in x[1]:
					q_string.append(x[0]+"="+j)
			q_string = '&'.join(q_string)
		

			# Handling page numbers 
			#======================================================================

			if current_value - 3 >= 1:
				min_index = current_value - 3		


			if current_value + 3 <= value.paginator.num_pages:
				max_index = current_value + 3
		
			for i in range(min_index, max_index+1):
				active = 'btn-default'
				if current_value == i:
					active = "btn-success"	

				html.append("<a style='border-radius:0px' class='btn btn-sm "+active+"' href='?page="+str(i)+"&"+q_string+"'>"+str(i)+"</a>")
			
	except:
		pass

	finally:
		return mark_safe(''.join(html))