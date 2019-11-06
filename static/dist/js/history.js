$(document).ready(function(){
	var token = sessionStorage.getItem('access').replace(/\"/g,"");
	$.ajax({
		type:"GET",
		url:"/api/v1/get_history",
		contentType:"application/json",
		dataType:"json",
		headers: {
			"Authorization": "bearer "+token,
		},
		success: function(data){
			var history = JSON.parse(JSON.stringify(data));
			console.log(history.results);
		},
		error: function(msg){
			return null;
		}
	})
});
