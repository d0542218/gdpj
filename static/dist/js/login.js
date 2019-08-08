function login(){
	var username = document.forms["loginForm"]["username"].value;
	// var email = document.forms["loginForm"]["email"].value;
	var pw = document.forms["loginForm"]["PW"].value;
	var data ="username :"+username+','+"password:"+pw;
	alert(data);
	$.ajax({
		type:"POST",
		url:"/auth/jwt/create",
		contentType:"application/json",
		dataType:"json",
		async: false,
		data:JSON.stringify({
			"username": username,
			"password": pw
		}),
		success: function(data){
			// $("#result").data($data);
			console.log(data);
			alert(data);
			window.location.href='../';
		},
		error: function(msg){
			alert(msg.responseText);
			return null;
		}
	})
// JSON.stringify(data),

}