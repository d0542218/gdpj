function login(){
	var username = document.forms["loginForm"]["username"].value;
	// var email = document.forms["loginForm"]["email"].value;
	var pw = document.forms["loginForm"]["PW"].value;
	if(username==""||pw==""){
		alert("還有資訊未填");
	}else{
		$.ajax({
			type:"POST",
			url:"/auth/jwt/create",
			contentType:"application/json",
			dataType:"json",
			data:JSON.stringify({
				"username": username,
				"password": pw
			}),
			success: function(data){
				var jwt = JSON.parse(JSON.stringify(data));
				var refresh = jwt.refresh;
				var access = jwt.access;
				sessionStorage.setItem('username',JSON.stringify(username));
				sessionStorage.setItem('refresh',JSON.stringify(refresh));
				sessionStorage.setItem('access',JSON.stringify(access));
				window.location.href='../';
			},
			error: function(msg){
				var err = eval("(" + msg.responseText + ")");
				alert("error "+msg);
				return null;
			}
		}
		)
	}

}	