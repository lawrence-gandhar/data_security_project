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


function activate_records(){
	
	opt = $(".activate_records").val();
	datalist = $(".case").val();
	
	$.post("{% url activate_records %}",{'opt':opt, 'datalist':datalist},function(){
		
	});
	
}