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
			async: false,
			data:JSON.stringify({
				"email" : email,
				"username" : username,
				"password" : pw,
			}),
			success: function(data){
				alert("success");
				$("#result").data($data); 
				console.log(data.success);
				for(x in data){
					alert(x);
				}
				console.log(data);
				window.location.href='../';
			},
			error: function(msg){
				alert(msg.responseText);
				var errorlist = document.createElement('ul');
				var errorText = document.createElement('li');
				errorlist.appendChild(errorText);
				errorText.innerHTML = msg.responseText;
				document.getElementById("errorText").appendChild(errorlist);
				// return null;	
			}
		})
		alert("註冊失敗");
	}
}