function checkLogin(){
	if(!sessionStorage.getItem('access')){
		window.location.href='/account/login';
		// $('#step-1-next');
	}else{
		var access = sessionStorage.getItem("access")
		access=access.replace(/\"/g,"");
		$.ajax({
			type:"POST",
			url:"/auth/jwt/verify",
			contentType:"application/json",
			dataType:"json",
			data:JSON.stringify({
				"token": access,
			}),
			success: function(data){
			},
			error: function(msg){
				refresh();
				return null;
			}

		})

	}
}
$(document).ready(function(){
	if(sessionStorage.getItem('access')){
		var token = sessionStorage.getItem('access');
		var base64Url = token.split('.')[1];
		var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
		var jsonPayload = JSON.parse(decodeURIComponent(atob(base64).split('').map(function(c) {
			return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
		}).join('')));
		sessionStorage.setItem('user_id',JSON.stringify(jsonPayload.user_id));
		var username = JSON.parse(sessionStorage.getItem('username'));
		$(".navbar-custom-menu ul").empty();
		$(".navbar-custom-menu ul").append('<li><a><span class="tab">'+username+'</span></a> <a class="btn btn-primary"><span class="tab" onclick="logout()">登出</span></a></li>');
	}
	checkLogin();
});


function refresh(){
	if(!sessionStorage.getItem('refresh')){
		// window.location.href='/account/login'
	}else{
		var refresh = sessionStorage.getItem("refresh")
		refresh=refresh.replace(/\"/g,"");
		$.ajax({
			type:"POST",
			url:"/auth/jwt/refresh",
			contentType:"application/json",
			dataType:"json",
			data:JSON.stringify({
				"refresh": refresh,
			}),
			success: function(data){
				var jwt = JSON.parse(JSON.stringify(data));
				console.log(jwt);
			},
			error: function(msg){
				window.location.href='/account/login'
				return null;
			}
		})
	}
}