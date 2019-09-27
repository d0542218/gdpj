
var files ;
var imgform = new FormData();
$('#file-uploader').change(function(evt){
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
        });
function dragoverHandler(evt) {
    evt.preventDefault();
    $('#upload_page_IMG').hide();
};
function dropHandler(evt) {
    evt.preventDefault();
    files = evt.dataTransfer.files;//由DataTransfer物件的files屬性取得檔案物件
    $('#upload_page_IMG').show();

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
        function openfile(evt) {
            var img = evt.target.result;
            var imgx = document.createElement('img');
            imgx.style.margin = "10px";
            imgx.style.width = "200px";
            imgx.style.height = "200px";
            imgx.src = img;
            document.getElementById('to_upload_img_DIV').appendChild(imgx);
        }
        $('#step-1-next').click(function() {
            if(imgform.getAll("esNote_score_pic").length==0){
                alert("請上傳圖片");
            }else{
                var yesUpload = confirm("是否上傳完畢");
                var token = sessionStorage.getItem('access');
                token=token.replace(/\"/g,"");
                if ((yesUpload == true)){

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
                            console.log(data.noteID);
                            $.each(score_pic,function(index,val){
                                $('.sp-wrap').append("<a href='" +val.esNote_score_pic +"'><img src='"+val.esNote_score_pic +"'></a>");      
                            })
                            $('.sp-wrap').smoothproducts();
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
