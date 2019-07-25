	function checkPW_emptyOrTrue(){ 
		var pw = document.forms["registerForm"]["PW"];
		var checkPW = document.forms["registerForm"]["checkPW"];
		if(pw.value!=checkPW.value)
		{
			alert("密碼錯誤")
			pw.value = "";
			checkPW.value = "";
		}
	}
