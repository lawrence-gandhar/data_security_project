
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
	
		
	$("#sidebar-id").on('click','.hide_show_button',function(){
		call_divs($(this));
	})
	
	
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


function call_divs(elem){	
	console.log('done');
	if($("#hide_show_settings").is(":visible")){
		$("#hide_show_settings").find(".hide-us").hide();
		$("#"+$(elem).attr("params")).show();
	}else {
		$("#hide_show_settings").show(200);
		$("#hide_show_settings").find(".hide-us").hide();
		$("#"+$(elem).attr("params")).show();
	}
}

function call_hide(){
	if($("#hide_show_settings").is(":visible")){
		$("#hide_show_settings").find(".hide-us").hide();
		$("#hide_show_settings").hide(200);
	}
}


function act_records(){
	opt = $("#assign_selected_opt").val();
	
	form_elem = $("form#my_form").serialize();
	form_elem += "&opt="+opt;
	
	$.post("/activate_records/",form_elem,function(data){
		location.reload();
	});
}


function assign_selected_records(){
	opt = $("#assign_selected_opt").val();
	staff = $("#assign_selected_staff").val();
	
	if(staff == ''){
		alert('Select A Staff');
		return false;
	}
	
	form_elem = $("form#my_form").serialize();
	form_elem += "&opt="+opt;
	form_elem += "&staff="+staff;
	
	$.post("/assign_selected_records/",form_elem,function(data){
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


function approve_records_section(){
	opt = $("#approve_records_opt").val();
	staff = $("#approve_records").val();
	file_ins = $("#load_data_opt").val();
	
	if(staff == '' && opt == '0'){
		alert('Select Options');
		return false;
	}
	
	form_elem = $("form#my_form").serialize();
	form_elem += "&opt="+opt;
	form_elem += "&staff="+staff;
	form_elem += "&file_ins="+file_ins;
	
	$.post("/approve_records/",form_elem,function(data){
		//location.reload();
	});
}
	

