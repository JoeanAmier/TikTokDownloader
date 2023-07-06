function solo_input() {
    // 点击按钮时获取剪贴板文本并写入输入框
    // 使用 Clipboard API 获取剪贴板文本
    navigator.clipboard.readText()
        .then(function (text) {
            // 将剪贴板文本写入输入框
            $('#solo_url').val(text);
        })
        .catch(function (error) {
            console.error('读取剪贴板失败: ', error);
        });
}

function live_input() {
    navigator.clipboard.readText()
        .then(function (text) {
            $('#live_url').val(text);
        })
        .catch(function (error) {
            console.error('读取剪贴板失败: ', error);
        });
}

function get_parameters() {
    // 获取当前参数设置
    return {
        root: $("#root").val(),
        folder: $("#folder").val(),
        name: $("#name").val(),
        time: $("#time").val(),
        split: $("#split").val(),
        music: $("#music:checked").val(),
        save: $("#save").val(),
        dynamic: $("#dynamic:checked").val(),
        original: $("#original:checked").val(),
        proxies: $("#proxies").val(),
        log: $("#log:checked").val(),
        cookie: $("#cookie").val(),
    }
}

function update_parameters() {
    $.ajax({
        type: "POST", url: "/save/", data: get_parameters(), success: function () {
            window.location.href = "/";
        }, error: function () {
            alert("保存配置文件失败！");
        }
    });
}


function solo_post(download = false) {
    $.post("/solo/", {url: $("#solo_url").val(), download: download}, function (result) {
        $("#solo_state").val(result["text"]);
        $("#solo_preview").attr("src", result["preview"]);
    });
}
function solo_post_downvido(download = false) {
    $.post("/solo/", {url: $("#solo_url").val(), download: download}, function (result) {
        var text = result["text"];

        // 提取视频下载地址
        var videoUrlRegex = /视频下载地址:(.*?)\n/;
        var extractedVideoUrl = videoUrlRegex.exec(text)[1];
        console.log("视频下载地址:", extractedVideoUrl);

        // 提取文件标题
        var titleRegex = /标题:(.*?)\n/;
        var extractedTitle = titleRegex.exec(text)[1];
        //extractedTitle = extractedTitle + ".mp4"
        console.log("文件标题:", extractedTitle);
        window.open(extractedVideoUrl);
        //down(extractedVideoUrl, extractedTitle);
        
        //down(extractedVideoUrl, extractedTitle);
        //console.log("执行文件下载操作，视频下载地址:", redirectedUrl, "文件标题:", extractedTitle);
    
    });
}


//solo_post_downyy
function solo_post_downyy(download = false) {
    $.post("/solo/", {url: $("#solo_url").val(), download: download}, function (result) {
        var text = result["text"];
        var regex = /原声下载地址:(.*?)\n/;
        var extractedText = regex.exec(text)[1];
        console.log(extractedText);
    });
}


function live_post() {
    $.post("/live/", {url: $("#live_url").val()}, function (result) {
        $("#live_state").val(result["text"]);
        $("#live_preview").attr("src", result["preview"]);
    });
}
