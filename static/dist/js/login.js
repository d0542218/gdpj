function login(){
	var username = document.forms["loginForm"]["username"].value;
	// var email = document.forms["loginForm"]["email"].value;
	var pw = document.forms["loginForm"]["PW"].value;
	var csrfToken = document.forms["loginForm"]["csrfmiddlewaretoken"].value
	var data ="username :"+username+','+"password:"+pw;
	alert(data);

	$.ajax({
		type:"post",
		url:"/auth/jwt/create",
		contentType:"application/json",
		dataType:"json",
		async: false,
		data:JSON.stringify({
			"username" : username,
			"password" : pw

		}),
		success: function(data){
			console.log(data.success); 
			alert("success");
			window.location.href='../';
		},
		error: function(msg){
			alert("error");
			return null;
		}
	})
}