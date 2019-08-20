
$(function(){});

function save_remarks(id){
	
	$.get("/get_record_details/",{'rec_id': id}, function(data){
		
		$("#id_contact_person").val(data.rec[0]["contact_person"]);
		$("#id_contact_number").val(data.rec[0]["contact_number"]);
		$("#id_email").val(data.rec[0]["email"]);
		$("#id_disposition").val(data.rec[0]["disposition"]);
		$("#id_remarks").val(data.rec[0]["remarks"]);	
		$("#abcd").val(data.rec[0]["id"]);
	});
	
	$("#myModal").modal('show');
}