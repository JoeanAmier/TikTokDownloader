function single_input() {
    // 点击按钮时获取剪贴板文本并写入输入框
    // 使用 Clipboard API 获取剪贴板文本
    navigator.clipboard.readText()
        .then(function (text) {
            // 将剪贴板文本写入输入框
            $('#single_url').val(text);
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
        folder_name: $("#folder_name").val(),
        name_format: $("#name_format").val(),
        date_format: $("#date_format").val(),
        split: $("#split").val(),
        music: $("#music:checked").val(),
        download: $("#download:checked").val(),
        folder_mode: $("#folder_mode:checked").val(),
        storage_format: $("#storage_format").val(),
        default_mode: $("#default_mode").val(),
        dynamic_cover: $("#dynamic_cover:checked").val(),
        original_cover: $("#original_cover:checked").val(),
        proxies: $("#proxies").val(),
        chunk: $("#chunk").val(),
        max_size: $("#max_size").val(),
        max_retry: $("#max_retry").val(),
        max_pages: $("#max_pages").val(),
        cookie: $("#cookie").val(),
        ffmpeg: $("#ffmpeg").val(),
    }
}

function update_parameters() {
    $.ajax({
        type: "POST",
        url: "/settings/",
        contentType: "application/json",
        data: JSON.stringify(get_parameters()),
        success: function () {
            window.location.href = "/";
        },
        error: function () {
            alert("保存配置失败！");
        }
    });
}


function single_post(download = false) {
    const data = {
        url: $("#single_url").val(), download: download
    };
    let $text = $("#single_url_text");
    $text.hide();
    $.ajax({
        type: "POST", url: "/single/", contentType: "application/json",  // 设置请求的 Content-Type 为 JSON
        data: JSON.stringify(data),  // 将 JSON 对象转为字符串
        success: function (result) {
            $("#single_state").val(result["text"]);
            $("#download_url").data("link", result["download"]);
            $("#music_url").data("link", result["music"]);
            $("#origin_url").data("link", result["origin"]);
            $("#dynamic_url").data("link", result["dynamic"]);
            $("#single_preview").attr("src", result["preview"]);
            if (result["author"] !== null) {
                $('#single_url').val("");
            }
            get_images();
        }, error: function () {
            alert("获取作品数据失败！");
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
    let $text = $("#single_url_text");
    $text.empty();
    if (Array.isArray(link)) {
        link.forEach(function (element, index) {
            let paragraph = $("<span>").html("<a href='" + element + "' target='_blank'>" + "图片-" + (index + 1) + "</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;");
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
    const data = {
        url: $("#live_url").val()
    };
    let $text = $("#live_url_text");
    $text.hide();
    $.ajax({
        type: "POST", url: "/live/", contentType: "application/json",  // 设置请求的 Content-Type 为 JSON
        data: JSON.stringify(data),  // 将 JSON 对象转为字符串
        success: function (result) {
            $("#live_state").val(result["text"]);
            let flv = result["flv"];
            let m3u8 = result["m3u8"];
            if (flv) {
                $("#live_url").val("");
                $("#all_url").data({"flv": flv, "m3u8": m3u8});
                $("#best_url").data("link", result["best"]);
                get_all();
            } else {
                $("#all_url").removeData(["flv", "m3u8"]);
                $("#best_url").removeData("link");
                $text.empty();
            }
            $("#live_preview").attr("src", result["preview"]);
        }, error: function () {
            alert("获取直播数据失败！");
        }
    });
}


function get_all() {
    let urls = $("#all_url").data();
    let $text = $("#live_url_text");
    $text.empty();
    for (let key in urls.flv) {
        let paragraph = $("<p>").text(`FLV 清晰度 ${key}: ${urls.flv[key]}`);
        $text.append(paragraph);
    }
    for (let key in urls.m3u8) {
        let paragraph = $("<p>").text(`M3U8 清晰度 ${key}: ${urls.m3u8[key]}`);
        $text.append(paragraph);
    }
    $text.toggle();
}


function get_best() {
    let link = $("#best_url").data("link");
    open_link(link);
}
