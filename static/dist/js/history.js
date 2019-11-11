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
				$("#historyTable").append("<tr><td>"+val.scoreName+"</td><td>"+val.scoreCreateTime.substring(0,10)+"</td><td><button id='jpg"+i+"' class='btn btn-lg btn-blue'>JPG<i class='fa fa-download'></i></button><button id='pdf"+i+"' class='btn btn-lg btn-blue'>PDF<i class='fa fa-download'></i></button></td></tr>");				getfile(val.noteID,token,document.getElementById('jpg'+i),document.getElementById('pdf'+i));
				var id = val.noteID;
				var jpg = $('#jpg'+i);
				var pdf = $('#pdf'+i);
				getfile(id,token,jpg,pdf);
				i+=1; 
			})
		},
		error: function(msg){
			return null;
		}
	})
});
function getfile(id,token,jpg,pdf){
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
		jpg.attr('download',step3File.filename);
		jpg.attr("href","data:application/zip;base64,"+step3File.file);
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
		pdf.attr('download',step3File.filename);
		pdf.attr("href","data:application/zip;base64,"+step3File.file);
	}).fail(function(jqXHR,textStatus,errorThrown){
		console.log(jqXHR,textStatus,errorThrown);
	}) 
}