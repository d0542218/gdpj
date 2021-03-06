function register(){
	var username = document.forms["registerForm"]["username"].value;
	var email = document.forms["registerForm"]["email"].value;
	var pw = document.forms["registerForm"]["PW"].value;
	var checkPW = document.forms["registerForm"]["checkPW"].value;
	console.log(username+email+pw);
	if(username==""||email==""||pw==""||checkPW==""){
		alert("還有資訊未填");
	}else{
		$.ajax({
			type:"POST",
			url:"/auth/users/",
			contentType:"application/json",
			dataType:"json",
			async: false,
			data:JSON.stringify({
				"email" : email,
				"username" : username,
				"password" : pw,
			}),
			success: function(data){
				sessionStorage.setItem('username',JSON.stringify(username));
				sessionStorage.setItem('password',JSON.stringify(pw));
				userActivation(JSON.stringify(data.user_id));
				alert("註冊成功");
				window.location.href='../account/login';
			},
			error: function(msg){
				$("#errorText").empty();
				var usernameError = JSON.parse(msg.responseText).username;
				var pwError = JSON.parse(msg.responseText).password;
				if(usernameError&&pwError){
					var errorMsg = usernameError+pwError;
				}else if (usernameError){
					var errorMsg =usernameError;
				}else if(pwError){
					var errorMsg =pwError;
				}
				var errorlist = document.createElement('ul');
				var errorText = document.createElement('li');
				errorlist.appendChild(errorText);
				errorText.innerHTML = errorMsg;
				document.getElementById("errorText").appendChild(errorlist);
				// return null;	
			}
		})
	}
}
function userActivation(id){
	$.ajax({
		type:"POST",
		url:"/api/v1/activation/",
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify({
			"user_id": id,
		})
	}).done(function(data){
	}).fail(function(jqXHR, textStatus, errorThrown){
		var error = JSON.parse(JSON.stringify(jqXHR));
		console.log(error+textStatus+errorThrown);
	})
}