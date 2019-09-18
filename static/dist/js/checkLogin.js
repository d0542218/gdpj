function checkLogin(){
	if(!sessionStorage.getItem('access')){
		window.location.href='/account/login'
	}else{
		$.ajax({
			type:"POST",
			url:"/auth/jwt/verify",
			contentType:"application/json",
			dataType:"json",
			data:JSON.stringify({
				"Token": sessionStorage.getItem("access"),
			}),
			success: function(data){
				console.log("success access");
			},
			error: function(msg){
				alert("error"+msg.responseText);
				return null;
			}

		})

	}
}
$(document).ready(function(){
	console.log('aa');
	if(sessionStorage.getItem('access')){
		var token = sessionStorage.getItem('access');
		var base64Url = token.split('.')[1];
		var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
		var jsonPayload = JSON.parse(decodeURIComponent(atob(base64).split('').map(function(c) {
			return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
		}).join('')));
		console.log(jsonPayload.user_id);
		sessionStorage.setItem('user_id',JSON.stringify(jsonPayload.user_id));
		var username = JSON.parse(sessionStorage.getItem('username'));
		$(".navbar-custom-menu ul").empty();
		$(".navbar-custom-menu ul").append('<li><a><span class="tab">'+username+'</span></a> <a class="btn btn-primary"><span class="tab" onclick="logout()">登出</span></a></li>');
	}

});

function logout(){
	sessionStorage.clear();
	$(".navbar-custom-menu ul").empty();
	$(".navbar-custom-menu ul").append('<li><a href="/account/login" class="btn btn-outline-primary">登入</a><a href="/register" class="btn btn-primary">註冊</a></li>');
}