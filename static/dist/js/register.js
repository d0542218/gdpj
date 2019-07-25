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
			url:"/auth/users/create",
			contentType:"application/json",
			dataType:"json",
			data:{
				"csrfmiddlewaretoken" : token,
				"email" : email,
				"username" : username,
				"password1" : pw,
			},
			success: function(data){
				alert("success");
				$("#result").data($data); 
				console.log(data.success); 
				alert(success);
				alert(data);
				console.log(data);
				// return data;
				window.location.href='../';
			},
			error: function(msg){
				alert("error");
				alert(msg);
				return null;	
			}
		})
		alert("註冊失敗");
	}
}