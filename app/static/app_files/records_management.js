
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
		$("#hide_show_settings").toggle();
		$("."+$(this).attr("params")).show();
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
		
	});
}
	

