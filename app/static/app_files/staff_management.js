
$(function(){
	$("select#id_dedicated_to_category").change(function(){
				
		if($(this).val()!=''){
			$.get("/get_sub_category/", {'cat_id':$(this).val()}, function(data){
				if(data!=''){
					$("#id_dedicated_to_sub_category").empty().html(data);
				}
			});		
		}
	});
	
});


