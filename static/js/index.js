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
        chunk: $("#chunk").val(),
        max_size: $("#max_size").val(),
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
        $("#download_url").data("link", result["download"]);
        $("#music_url").data("link", result["music"]);
        $("#origin_url").data("link", result["origin"]);
        $("#dynamic_url").data("link", result["dynamic"]);
        $("#solo_preview").attr("src", result["preview"]);
        if (result["download"] !== false) {
            $('#solo_url').val("");
        }
    });
}

function get_download() {
    let link = $("#download_url").data("link");
    if (!Array.isArray(link)) {
        open_link(link);
    }
}

function get_images() {
    let link = $("#download_url").data("link");
    let $text = $("#solo_url_text");
    $text.empty();
    if (Array.isArray(link)) {
        link.forEach(function (element, index) {
            let paragraph = $("<p>").text(`图片-${index}: ${element}`);
            $text.append(paragraph);
        });
        $text.toggle();
    }
}

function get_music() {
    let link = $("#music_url").data("link");
    open_link(link);
}

function get_origin() {
    let link = $("#origin_url").data("link");
    open_link(link);
}

function get_dynamic() {
    let link = $("#dynamic_url").data("link");
    open_link(link);
}

function open_link(link) {
    if (link) {
        let a = document.createElement("a");
        a.href = link;
        a.setAttribute("rel", "noreferrer noopener");
        a.setAttribute("target", "_blank");
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
}

function live_post() {
    $.post("/live/", {url: $("#live_url").val()}, function (result) {
        $("#live_state").val(result["text"]);
        let urls = result["urls"];
        if (urls) {
            $("#live_url").val("");
            $("#all_url").data("link", urls);
            $("#best_url").data("link", result["best"]);
        } else {
            $("#all_url").removeData("link");
            $("#best_url").removeData("link");
        }
        $("#live_preview").attr("src", result["preview"]);
    });
}

function get_all() {
    let link = $("#all_url").data("link");
    let $text = $("#live_url_text");
    $text.empty();
    for (let key in link) {
        let paragraph = $("<p>").text(`清晰度${key}: ${link[key]}`);
        $text.append(paragraph);
    }
    $text.toggle();
}


function get_best() {
    let link = $("#best_url").data("link");
    open_link(link);
}
