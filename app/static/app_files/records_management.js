
$(function(){

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
	$("button.hide_show_button").click(function(){
		$("#hide_show_settings").toggle();
	});
	
		
});

function act_records(){
	opt = $("#activate_records").val();
	
	form_elem = $("form#my_form").serialize();
	//form_elem.push({"opt":opt});
	
	
	$.post("/activate_records/",form_elem,function(){
		
	});
}

