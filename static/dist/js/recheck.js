$('#step-2-previous').click(function(){
	window.location.reload();
	var token = sessionStorage.getItem('access').replace(/\"/g,"");
	$.ajax({
		url: "/api/v1/esNoteScore/"+sessionStorage.getItem('noteID').replace(/\"/g,""),
		method: "DELETE",
		headers: {
			"Authorization": "bearer "+token,
		},
		processData: false,
		contentType: false,
		success: function(data) {
			console.log(data);
		},
		error: function(msg){
			console.log(msg);
			return null;
		}
	});
	// $.ajax({
	// 	url: 'static/dist/js/upload.js',
	// 	dataType: 'script',
	// 	async: false
	// });
})