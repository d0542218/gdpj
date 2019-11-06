
var files ;
var file_count = 0;
var imgform = new FormData();
var current = 0;
// var backFiles = [];
// var img_count = 0;
$('#file-uploader').change(function(evt){
    if((file_count+evt.target.files.length)<=5){
        file_count += evt.target.files.length;
        files = evt.target.files;
        for (var i in files) {
            if ((files[i].type == 'image/jpeg') | (files[i].type == 'image/png')) {
                    //將圖片在頁面預覽
                    var fr = new FileReader();
                    fr.onload = openfile;
                    fr.readAsDataURL(files[i]);
                    imgform.append('esNote_score_pic',files[i]);
                }
            }
        }
        else{
            alert("太多圖片了");
        }
    });
function dragoverHandler(evt) {
    evt.preventDefault();
    $('#upload_page_IMG').hide();
};
function dropHandler(evt) {
    evt.preventDefault();
    if((file_count+evt.dataTransfer.files.length)<=5){
        files = evt.dataTransfer.files;//由DataTransfer物件的files屬性取得檔案物件
        file_count += files.length;
        $('#upload_page_IMG').show();

        for (var i in files) {
            if ((files[i].type == 'image/jpeg') | (files[i].type == 'image/png')) {
                var fr = new FileReader();
                fr.onload = openfile;
                fr.readAsDataURL(files[i]);
                imgform.append('esNote_score_pic',files[i]);
            }
        }
    }else{
        alert("太多圖片了");
        $('#upload_page_IMG').show();
    }
}
function openfile(evt) {
    var img = evt.target.result;
    var imgx = document.createElement('img');
    imgx.style.margin = "10px";
    imgx.style.height = "400px";
    imgx.style.width = "400px";
    imgx.src = img;
    $('#upload_page_IMG').hide();
    $('#upload_page_Text').remove();
    document.getElementById('to_upload_img_DIV').appendChild(imgx);
    $('#to_upload_img_DIV').append("<div id ='upload_page_Text'>點擊或拖拉檔案至此</div>");
    document.getElementById('dropDIV').style.width="80%";
    if(file_count>3){
        document.getElementById('dropDIV').style.height="80%";
    }else{
        document.getElementById('dropDIV').style.height="60%";
    }
    document.getElementById('upload_page_Text').style.margin="10px";

}
$('#step-1-next').click(function() {
    if(imgform.getAll("esNote_score_pic").length==0){
        alert("請上傳圖片");
    }else{
        var yesUpload = confirm("是否上傳完畢");
        var token = sessionStorage.getItem('access');
        token=token.replace(/\"/g,"");
        if ((yesUpload == true)){
            $( "body" ).loading();
            $.ajax({
                url: "/api/v1/uploadImages/",
                method: "POST",
                headers: {
                    "Authorization": "bearer "+token,
                },
                processData: false,
                contentType: false,
                mimeType: "multipart/form-data",
                dataType:"json",
                data: imgform,
                success: function(data) {
                    var score_pic = data.esNote_score_pic;
                    sessionStorage.setItem('noteID',JSON.stringify(data.noteID));
                    // console.log(score_pic);
                    $.each(score_pic,function(index,val){
                        // backFiles[img_count] = val.esNote_score_pic;
                        $('#step2-wrap').append("<a href='" +val.esNote_score_pic +"'><img src='"+val.esNote_score_pic +"'></a>");
                                // $('#ImgOrder').append("<option value='"+i+"'>第"+(i+1)+"張</option>");
                                // img_count++;      
                            })
                    // console.log(backFiles);
                    $('#step2-wrap').smoothproducts('#step2-wrap');
                    $( "body" ).loading( "stop" );
                    stepper1.next();
                    return data;
                },
                error: function(msg){
                    return null;
                }
            });
        }
    }
});
$('#step-2-previous').click(function(){
    var token = sessionStorage.getItem('access').replace(/\"/g,"");
    $.ajax({
        async:true,
        crossDomain:true,
        url: "/api/v1/esNoteScore/"+sessionStorage.getItem('noteID').replace(/\"/g,"")+'/',
        method: "DELETE",
        headers: {
            "Authorization": "bearer "+token,
        },
        success: function(data) {
            $( "body" ).loading();
            window.location.reload();
            $( "body" ).loading( "stop" );
        },
        error: function(msg){
            console.log(msg);
            return null;
        }
    });
});

$('#step-2-next').click(function() {
    if(document.getElementById('step3-wrap1')){
        var f = document.getElementById('step3-content1');
        var step3Child = f.childNodes;
        for(var i = step3Child.length - 1; i >= 0; i--) {
            f.removeChild(step3Child[i]);
        }
        f = document.getElementById('step3-content2');
        step3Child = f.childNodes;
        for(var i = step3Child.length - 1; i >= 0; i--) {
            f.removeChild(step3Child[i]);
        }
    }
    $('#step3-content1').append("<div class='sp-wrap' style='display: inline-block;' id='step3-wrap1'></div>");
    $('#step3-content2').append("<div class='sp-wrap' style='display: inline-block;' id='step3-wrap2'></div>");
    $( "body" ).loading();
    var id = sessionStorage.getItem('noteID').replace(/\"/g,"");
    var token = sessionStorage.getItem('access').replace(/\"/g,"");
    var step3Flag = 0;
    for(i=1;i<file_count+1;i++){
        $.ajax({
            url: "/api/v1/fakePredict/?id="+id+"&order="+i,
            method: "GET",
            dataType:"json",
            headers: {
                "Authorization": "bearer "+token,
            }
        }).done(function(data){
            step3Flag++;
            var predictIMG = JSON.parse(JSON.stringify(data));
            $('#step3-wrap1').append("<a href='data:image/png;base64,"+predictIMG.pic +"'><img src= 'data:image/png;base64,"+predictIMG.pic +"'></a>");
            for(j=0;j<predictIMG.simple_url.length;j++){
                $('#step3-wrap2').append("<a href='"+predictIMG.simple_url[j]+"'><img src= '"+predictIMG.simple_url[j]+"'></a>");
            }
            if(step3Flag==file_count){
                $( "body" ).loading( "stop" );
                $('#step3-content1').smoothproducts('#step3-content1');
                $('#step3-content2').smoothproducts('#step3-content2');
                stepper1.next();
            }
        })
        .fail(function (jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        });
        sleep(1500);
    }
})
$('#step-3-pdf').click(function(){
    var form = new FormData();
    var name = $('#step3Label').text();
    var id = sessionStorage.getItem('noteID').replace(/\"/g,"");
    var token = sessionStorage.getItem('access').replace(/\"/g,"");
    form.append("scoreName",name);
    $.ajax({
        url:"/api/v1/change_score_name/"+id+"/",
        method:"PUT",
        headers: {
            "Authorization": "bearer "+token,
            "Content-Type": "multipart/form-data;"
        },
        dataType:"json",
        processData:false,
        contentType:false,
        mimeType: "multipart/form-data",
        data:form

    }).done(function(data){
        console.log(data);
    }).fail(function(jqXHR,textStatus,errorThrown){
        console.log(jqXHR,textStatus,errorThrown);
    })
    $.ajax({
        url:"/api/v1/get_simple_score?id="+id+"&PDF=1",
        method:"GET",
        headers: {
            "Authorization": "bearer "+token,
        },
        processData:false,
    }).done(function(data){
        console.log(data);
    }).fail(function(jqXHR,textStatus,errorThrown){
        console.log(jqXHR,textStatus,errorThrown);
    })
})
$('#step-3-jpg').click(function(){
    var form = new FormData();
    var name = $('#step3Label').text();
    var id = sessionStorage.getItem('noteID').replace(/\"/g,"");
    var token = sessionStorage.getItem('access').replace(/\"/g,"");
    form.append("scoreName",name);
    $.ajax({
        url:"/api/v1/change_score_name/"+id+"/",
        method:"POST",
        headers: {
            'X-HTTP-Method-Override': 'PATCH',
            "Authorization": "bearer "+token,
            "Content-Type": "multipart/form-data;"
        },
        dataType:"json",
        processData:false,
        contentType:false,
        mimeType: "multipart/form-data",
        data:form

    }).done(function(data){
        console.log(data);
        $()
    }).fail(function(jqXHR,textStatus,errorThrown){
        console.log(jqXHR,textStatus,errorThrown);
    })
    $.ajax({
        url:"/api/v1/get_simple_score?id="+id+"&ZIP=1",
        method:"GET",
        headers: {
            "Authorization": "bearer "+token,
        },
        processData:false,
    }).done(function(data){
        $('#step-3-jpg').attr("href",data);
    }).fail(function(jqXHR,textStatus,errorThrown){
        console.log(jqXHR,textStatus,errorThrown);
    })
})
function sleep(ms = 0){
    return new Promise(r=> setTimeout(r,ms));
}
$('#ImgOrder').change(function(){
    var order = $('#ImgOrder option:selected').val();
})
$('#rotate_right').click(function(){
    current = (current+90)%360;
    document.getElementById('sp-current-big-img').style.transform = 'rotate('+current+'deg)';
})

$('#rotate_left').click(function(){
    current = (current-90)%360;
    document.getElementById('sp-current-big-img').style.transform = 'rotate('+current+'deg)';
})

$('#editName_btn').click(function(){
    $('#step3Label').css('display','none');
    $('#step3Input').css('display','');
})

$("#step3Input").on("change paste", function() {
    $('#step3Label').css('display','');
    $('#step3Input').css('display','none');
    $('#step3Label').html($('#step3Input').val());
});
        // data:JSON.stringify({
        //     'scoreName':name
        // })