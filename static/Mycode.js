var all_videos = new Array();
var all_pics = new Array();
var processed_list = new Array();

function selectvideo(list) {
    for (var listKey in list) {
        if ((all_videos.indexOf(list[listKey]) != -1) || (all_pics.indexOf(list[listKey]) != -1)) {
            continue
        }
        if (list[listKey].search('.mp4') != -1) {
            all_videos.push(list[listKey])
        } else {
            all_pics.push(list[listKey])
        }
    }
}

function GetFileName() {
    $.ajax({
        url: '/getFileName/',
        type: 'POST',
        data: '',
        processData: false,  // tell jquery not to process the data
        contentType: false, // tell jquery not to set contentType
        success: function (data, status) {
            //console.log('Got Files.');
            selectvideo(data.msg.RowFileNameList);
            processed_list = data.msg.ProcessedFileNameList;
            RenderJPG();
        }
    })
}

function RenderMP4() {
    $('#forpic').hide();
    $('#forvideo').show();
    var len = all_videos.length
    var re = "";
    for (var i = 0; i < len; i++) {
        var videoname = all_videos[i];
        var rep = "/static/Upload_File/" + videoname
        if (i < 2) {
            re += '<div class="col-md-4"> <div class="thumbnail"> <div class="embed-responsive embed-responsive-16by9"> <video controls> <source src=' + rep + ' type="video/mp4"> </video> </div> <div class="caption"> <h3>' + videoname + '</h3> <p>...</p> <p><a href="#" class="btn btn-primary" role="button"  data-toggle="modal" data-target="#videoDisplay" onclick="processed_video_display(this,' + "'" + videoname + "'" + ')">播放处理结果</a> <a href="#" class="btn btn-default" role="button" data-toggle="modal" data-target="#videoDisplay" onclick="video_display(' + "'" + videoname + "'" + ')">在线目标检测</a></p> </div></div></div> ';
        }
        if (i >= 2) {
            re += '<div class="col-md-4 col-md-offset-2"> <div class="thumbnail"> <div class="embed-responsive embed-responsive-16by9"> <video controls> <source src=' + rep + ' type="video/mp4"> </video> </div> <div class="caption"> <h3>' + videoname + '</h3> <p>...</p> <p><a href="#" class="btn btn-primary" role="button" data-toggle="modal" data-target="#videoDisplay" onclick="processed_video_display(this,' + "'" + videoname + "'" + ')">播放处理结果</a> <a href="#" class="btn btn-default" role="button" data-toggle="modal" data-target="#videoDisplay" onclick="video_display(' + "'" + videoname + "'" + ')">在线目标检测</a></p> </div></div></div> ';
        }
    }
    document.getElementById('forvideo').innerHTML = re;
}

function RenderJPG() {
    $('#forvideo').hide();
    $('#forpic').show();
    var len = all_pics.length
    var re = "";
    for (var i = 0; i < len; i++) {
        var picname = all_pics[i];
        var rep = "/static/Upload_File/" + picname
        if (i >= 2 && i % 2 === 0) {
            re += '<div class="col-md-4 col-md-offset-2"> <div class="thumbnail"> <div class="embed-responsive embed-responsive-16by9"> <img style="display: inline-block; width: 100%; max-width: 100%; height: auto;" src=' + rep + '> </div> <div class="caption"> <h3>' + picname + '</h3> <p>...</p> <p><a href="#" class="btn btn-primary" data-toggle="modal" data-target="#videoDisplay" role="button" onclick="pic_zoom(' + "'" + picname + "'" + ')">显示大图</a> <a href="#" class="btn btn-default" role="button" data-toggle="modal" data-target="#videoDisplay" onclick="pic_display(' + "'" + picname + "'" + ')">单图片目标检测</a></p> </div></div></div> ';
        } else {
            re += '<div class="col-md-4"> <div class="thumbnail"> <div class="embed-responsive embed-responsive-16by9"> <img style="display: inline-block; width: 100%; max-width: 100%; height: auto;"  src=' + rep + '> </div> <div class="caption"> <h3>' + picname + '</h3> <p>...</p> <p><a href="#" class="btn btn-primary" data-toggle="modal" data-target="#videoDisplay" role="button" onclick="pic_zoom(' + "'" + picname + "'" + ')">显示大图</a> <a href="#" class="btn btn-default" role="button" data-toggle="modal" data-target="#videoDisplay" onclick="pic_display(' + "'" + picname + "'" + ')">单图片目标检测</a></p> </div></div></div> ';
        }
    }
    document.getElementById('forpic').innerHTML = re;
}

function processed_video_display(th, id) {
    console.log(id)
    console.log("test.mp4")
    if (processed_list.indexOf(id) == -1) {
        alert("后台暂无该视频检测数据");
        th.setAttribute("data-toggle", "")
        return false;
    }
    var img = document.getElementById('ModalPic')
    var form_data = new FormData();
    form_data.append('videoname', id);
    form_data.append('type', "processed");
    $.ajax({
        url: '/comfirmName/',
        type: 'POST',
        data: form_data,
        processData: false,  // tell jquery not to process the data
        contentType: false, // tell jquery not to set contentType
        success: function (data, status) {
            img.setAttribute("src", "http://127.0.0.1:8080/monitor/")
            //console.log('Video Name Got.');
        }
    })
}

function video_display(id) {
    var img = document.getElementById('ModalPic')
    var form_data = new FormData();
    form_data.append('videoname', id);
    form_data.append('type', "raw");
    $.ajax({
        url: '/comfirmName/',
        type: 'POST',
        data: form_data,
        processData: false,  // tell jquery not to process the data
        contentType: false, // tell jquery not to set contentType
        success: function (data, status) {
            img.setAttribute("src", "http://127.0.0.1:8080/monitor/")
            //console.log('Video Name Got.');
        }
    })
    console.log(id)
}

function pic_display(id) {
    var img = document.getElementById('ModalPic')
    var form_data = new FormData();
    form_data.append('picname', id);
    $.ajax({
        url: '/picsave/',
        type: 'POST',
        data: form_data,
        processData: false,  // tell jquery not to process the data
        contentType: false, // tell jquery not to set contentType
        success: function (data, status) {
            img.setAttribute("src", "/static/Processed_File/" + id)
            //console.log('Video Name Got.');
        }
    })
}

function pic_zoom(id) {
    var img = document.getElementById('ModalPic')
    img.setAttribute("src", "/static/Upload_File/" + id)
}

function aTest() {
    console.log(all_videos)
    console.log(all_pics)
}

function ShowSideBar() {
    $('#plain-pic').hide();
    $('#foot').hide();
    $('#sideB').show();
}

function file_upload() {
    var form_data = new FormData();
    var file_info = document.getElementById('File_upload').files[0]
    console.log(file_info)
    if (file_info == undefined) {
        alert('请选择文件')
        return false;
    }
    form_data.append('file', file_info);
    $.ajax({
        url: '/uploadFiles/',
        type: 'POST',
        data: form_data,
        processData: false,  // tell jquery not to process the data
        contentType: false, // tell jquery not to set contentType
        success: function (data, status) {
            $('#kv-success-1').html('<h4>Upload Result</h4><ul></ul>').hide();
            var fname = data.msg.filename,
                out = '<li>' + 'Uploaded file ' + fname + ' - ' + ' successfully.' + '</li>';
            $('#kv-success-1 ul').append(out);
            $('#kv-success-1').fadeIn('slow');
            //console.log('Upload Finsh.');
            mainpage();
            $('#exampleModal').modal('hide')
        }
    });
}

$(function () {
    $('#videoDisplay').on('hide.bs.modal', function () {
        var img = document.getElementById('ModalPic')
        img.setAttribute("src", "")
    })
});

function mainpage() {
    ShowSideBar();
    GetFileName();
}

// 预载模型
function LoadModel(id) {
    alert(id)
    console.log(id)
}

$("#File_upload").fileinput({
    language: 'zh',
    showPreview: false,
    showUpload: false,
    browseOnZoneClick: true,
    allowedPreviewTypes: false,
    maxFileSize: 15000,
    // uploadAsync: false,
    uploadAsync: true,
    theme: "explorer-fas",
    removeFromPreviewOnError: true,
    allowedFileExtensions: ['jpg', 'png', 'mp4'],
    maxFileCount: 10,
    overwriteInitial: false,
    fileActionSettings: {
        showUpload: false,
        showZoom: false,
    },
})

