function login(){
	var username = document.forms["loginForm"]["username"].value;
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
				sessionStorage.setItem('username',JSON.stringify(username));
				sessionStorage.setItem('refresh',JSON.stringify(jwt.refresh));
				sessionStorage.setItem('access',JSON.stringify(jwt.access));
				window.location.href='../';
			},
			error: function(msg){
				console.log(msg.responseText);
				alert("錯誤的帳號密碼");
				return null;
			}
		}
		)
	}

}	