$(document).ready(function(){
	var i = 0;
	var token = sessionStorage.getItem('access').replace(/\"/g,"");
	$.ajax({
		type:"GET",
		url:"/api/v1/get_history",
		contentType:"application/json",
		dataType:"json",
		headers: {
			"Authorization": "bearer "+token,
		},
		success: function(data){
			var history = JSON.parse(JSON.stringify(data));
			$.each(history.results,function(index,val){
				$("#historyTable").append("<tr><td>"+val.scoreName+"</td><td>"+val.scoreCreateTime.substring(0,10)+"</td><td><a id='jpg"+i+"' class='btn btn-lg btn-blue'>JPG  <i class='fa fa-download'></i></a><a id='pdf"+i+"' class='btn btn-lg btn-blue'>PDF  <i class='fa fa-download'></i></a></td></tr>");				
				var id = val.noteID;
				getfile(id,token,i);
				i+=1; 
			})
		},
		error: function(msg){
			return null;
		}
	})
});
function getfile(id,token,number){
	$.ajax({
		url:"/api/v1/get_simple_score?id="+id+"&fileType=ZIP",
		method:"GET",
		headers: {
			"Authorization": "bearer "+token,
		},
		processData:false,
		dataType:'json'
	}).done(function(data){
		var step3File = JSON.parse(JSON.stringify(data));
		$('#jpg'+number).attr('download',step3File.filename);
		$('#jpg'+number).attr("href","data:application/zip;base64,"+step3File.file);
	}).fail(function(jqXHR,textStatus,errorThrown){
		console.log(jqXHR,textStatus,errorThrown);
	})
	$.ajax({
		url:"/api/v1/get_simple_score?id="+id+"&fileType=PDF",
		method:"GET",
		headers: {
			"Authorization": "bearer "+token,
		},
		processData:false,
	}).done(function(data){
		var step3File = JSON.parse(JSON.stringify(data));
		$('#pdf'+number).attr('download',step3File.filename);
		$('#pdf'+number).attr("href","data:application/zip;base64,"+step3File.file);
	}).fail(function(jqXHR,textStatus,errorThrown){
		console.log(jqXHR,textStatus,errorThrown);
	}) 
}