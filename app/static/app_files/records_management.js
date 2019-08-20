
$(function(){
	
	$("#hide_show_settings").hide();

	// add multiple select / deselect functionality
	$("#selectall").click(function () {
		  $('.case').attr('checked', this.checked);
	});

	// if all checkbox are selected, check the selectall checkbox
	// and viceversa
	$(".case").click(function(){

		if($(".case").length == $(".case:checked").length) {
			$("#selectall").attr("checked", "checked");
		} else {
			$("#selectall").removeAttr("checked");
		}

	});
	
	
	//
	// Hide show settings side bar
	$(".hide_show_button").click(function(){
		$("#hide_show_settings").find("table").css({"display":"none"})
		$("#hide_show_settings").toggle();		
		$("."+$(this).attr("params")).show();
	});
	
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

function act_records(){
	opt = $("#activate_records").val();
	
	form_elem = $("form#my_form").serialize();
	form_elem += "&opt="+opt;
	
	$.post("/activate_records/",form_elem,function(data){
		location.reload();
	});
}

function auto_assign_rec(){
	file_ins = $("#load_data_opt").val();
	opt = $("#auto_assign").val();
	
	$.get('/auto_assign/',{'file_ins':file_ins, 'opt':opt,}, function(){
		location.reload()
	});
}

function set_completed(status, rec_id){
	$.get("/set_completed/",{"status":status, "rec_id":rec_id}, function(data){
		location.reload();
	})
}

function delete_file_data(){
	
	var r = confirm("ALERT! Use only if data insertion is not as expected, or, wrong data insertion, or None fields are inserted even if there is data in the excel file");
	
	if (r == true) {
	  file_ins = $("#load_data_opt").val();
		$.get("/delete_file_data/",{'file_ins':file_ins},function(){
			location.reload();
		});
	}
		
}
	

