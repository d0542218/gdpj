function login(){
	var username = document.forms["loginForm"]["username"].value;
	// var email = document.forms["loginForm"]["email"].value;
	var pw = document.forms["loginForm"]["PW"].value;
	var data ="username :"+username+','+"password:"+pw;
	alert(data);
	$.ajax({
		type:"post",
		url:"/auth/jwt/create",
		contentType:"application/json",
		dataType:"json",
		data:{
			"username": "user",
			"password": "djangopassword"
		},
		success: function(data){
			// $("#result").data($data);
			console.log(data.success); 
			alert("success");
			window.location.href='../';
		},
		error: function(msg){
			alert("error");
			return null;
		}
	})
	alert("登入失敗");
// JSON.stringify(data),

}