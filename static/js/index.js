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

/*
function solo_post(download = false) {
    $.post("/solo/", {url: $("#solo_url").val(), download: download}, function (result) {
        $("#solo_state").val(result["text"]);
        $("#solo_preview").attr("src", result["preview"]);
    });
}
*/
function solo_post(download = false) {
    $.post("/solo/", {url: $("#solo_url").val(), download: download}, function (result) {
        var text = result["text"];

        var videoUrlRegex = /视频下载地址: (.*?)\n/;
        var extractedVideoUrl = videoUrlRegex.exec(text)[1];
        var titleRegex = /标题: (.*?)\n/;
        var extractedTitle = titleRegex.exec(text)[1];
        var regex = /原声下载地址: (.*?)\n/;
        var extractedText = regex.exec(text)[1];
        var inputElement = document.getElementById("playApi");
        inputElement.value = extractedVideoUrl;
        var inputElement = document.getElementById("desc");
        inputElement.value = extractedTitle;
        var inputElement = document.getElementById("acc");
        inputElement.value = extractedText;
    });
}


//solo_post_downyy
/*
function solo_post_downyy(download = false) {
    $.post("/solo/", {url: $("#solo_url").val(), download: download}, function (result) {
        var text = result["text"];
        var regex = /原声下载地址:(.*?)\n/;
        var extractedText = regex.exec(text)[1];
        console.log(extractedText);
    });
}
*/

function live_post() {
    $.post("/live/", {url: $("#live_url").val()}, function (result) {
        $("#live_state").val(result["text"]);
        $("#live_preview").attr("src", result["preview"]);
    });
}


var copyDescButton = document.getElementById("copyDescButton");
var descInputElement = document.getElementById("desc");
copyDescButton.addEventListener("click", function() {
  descInputElement.select();
  document.execCommand("copy");
  window.getSelection().removeAllRanges();
  alert("视频标题已复制！");
});

var copyAccButton = document.getElementById("copyAccButton");
var accInputElement = document.getElementById("acc");
copyAccButton.addEventListener("click", function() {
  accInputElement.select();
  document.execCommand("copy");
  window.getSelection().removeAllRanges();
  alert("原声链接已复制！");
});

var copyPlayApiButton = document.getElementById("copyPlayApiButton");
var playApiInputElement = document.getElementById("playApi");
copyPlayApiButton.addEventListener("click", function() {
  playApiInputElement.select();
  document.execCommand("copy");
  window.getSelection().removeAllRanges();
  alert("视频链接已复制！");
});
