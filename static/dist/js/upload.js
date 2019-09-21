
var files ;
var imgform = new FormData();
function dragoverHandler(evt) {
    evt.preventDefault();
    $('#upload_page_IMG').hide();
}
function dropHandler(evt) {//evt 為 DragEvent 物件
    evt.preventDefault();
    files = evt.dataTransfer.files;//由DataTransfer物件的files屬性取得檔案物件
    $('#upload_page_IMG').show();

    for (var i in files) {
        console.log(files[i].type);
        if ((files[i].type == 'image/jpeg') | (files[i].type == 'image/png')) {
                    //將圖片在頁面預覽
                    var fr = new FileReader();
                    fr.onload = openfile;
                    fr.readAsDataURL(files[i]);
                    imgform.append('sheet_image[]',files[i]);
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
            var yesUpload = confirm("是否上傳完畢");
            var token = sessionStorage.getItem('refresh');
            console.log(token);
            if (yesUpload == true){
                $.ajax({
                    headers:{ "Authorization": 'Bearer ' + token },
                    type:"POST",
                    url: "/api/v1/uploadImages/",
                    dataType: "json",
                    data:JSON.stringify({
                        "scoreInfoJason":imgform
                    }),
                    
                    success: function(data) {
                        console.log(data)
                        $('#stepper1').next();
                        return data;
                    },
                    error: function(msg){
                        return null;
                    }
                })}else{
                }
            })