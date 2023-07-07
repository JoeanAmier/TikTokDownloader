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

function picter_input() {
    navigator.clipboard.readText()
        .then(function (text) {
            $('#picture_url').val(text);
        })
        .catch(function (error) {
            console.error('读取剪贴板失败: ', error);
        });
}

function get_parameters() {
    
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
    const container = document.querySelector(".container");
    container.innerHTML = "";
    document.getElementById('Button_Post').value = 'Waiting...';
    var inputElement = document.getElementById("playApi");
    inputElement.value = '';
    var inputElement = document.getElementById("desc");
    inputElement.value = '';
    var inputElement = document.getElementById("acc");
    inputElement.value = '';
    $.post("/solo/", {url: $("#solo_url").val(), download: download}, function (result) {
        document.getElementById('Button_Post').value = '解析视频';
        
        var data = JSON.parse(result);
        console.log(data.happen);
        if(data.happen == 1){
            console.log('图集');
            var imageUrls = data.image_urls;
            var description = data.description;
            console.log(imageUrls);
                if(imageUrls.length > 15){
                    console.log('你妹的解析那么多干什么');
                    createTextBoxFromArray(imageUrls);
                }else{
                    for (var i = 0; i < imageUrls.length; i++) {
                    createImageCard(imageUrls[i], "文案:",description + i);
                    }
                }
            
        }else{
            var data = JSON.parse(result);
        if(data.happen == 0){
            console.log('视频');
            var extractedVideoUrl = data.video_url;
            var extractedTitle = data.description;
            var extractedText = data.music_info;
            //console.log(imageUrls);
            var inputElement = document.getElementById("playApi");
            inputElement.value = extractedVideoUrl;
            var inputElement = document.getElementById("desc");
            inputElement.value = extractedTitle;
            var inputElement = document.getElementById("acc");
            inputElement.value = extractedText;
            
        }else{
            if(data.happen == 400){
                var data = JSON.parse(result);
                console.log(data.text);
                alert(data.text);
            }
        }   
        }
        

        /*
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
        document.getElementById('Button_Post').value = '解析视频';
        */
    });
}



function picter_post() {
    alert("Making...");
    /*
    $.post("/live/", {url: $("#live_url").val()}, function (result) {
        $("#live_state").val(result["text"]);
        $("#live_preview").attr("src", result["preview"]);
    });
    */
}


document.addEventListener("DOMContentLoaded", function() {
    var copyDescButton = document.getElementById("copyDescButton");
    var descInputElement = document.getElementById("desc");
    copyDescButton.addEventListener("click", function() {
      descInputElement.select();
      navigator.clipboard.writeText(descInputElement.value)
        .then(function() {
          alert("视频简介已复制！");
        })
        .catch(function(err) {
          console.error("复制失败:", err);
        });
    });
  
    var copyPlayApiButton = document.getElementById("copyPlayApiButton");
    var playApiInputElement = document.getElementById("playApi");
    copyPlayApiButton.addEventListener("click", function() {
      playApiInputElement.select();
      navigator.clipboard.writeText(playApiInputElement.value)
        .then(function() {
          alert("视频链接已复制！");
        })
        .catch(function(err) {
          console.error("复制失败:", err);
        });
    });
  
    var copyAccButton = document.getElementById("copyAccButton");
    var accInputElement = document.getElementById("acc");
    copyAccButton.addEventListener("click", function() {
      accInputElement.select();
      navigator.clipboard.writeText(accInputElement.value)
        .then(function() {
          alert("原声链接已复制！");
        })
        .catch(function(err) {
          console.error("复制失败:", err);
        });
    });
  });
  




var openLinkButton = document.getElementById("openLinkButton");
  var playApiInputElement = document.getElementById("playApi");
  openLinkButton.addEventListener("click", function() {
  var link = playApiInputElement.value;
  openLinkWithoutReferer(link);
});
  
function openLinkWithoutReferer(link) {
  var a = document.createElement("a");
  a.href = link;
  a.rel = "noreferrer";
  a.target = "_blank";
  a.click();
}

  
  

function createImageCard(imageLink, name, cost, starRating) {
    const container = document.querySelector(".container");
  
    const foodCard = document.createElement("div");
    foodCard.className = "food-card";
  
    const pic = document.createElement("div");
    pic.className = "pic";
  
    const img = document.createElement("img");
    img.src = imageLink;
  
    pic.appendChild(img);
    foodCard.appendChild(pic);
  
    // 创建详情部分
    const detail = document.createElement("div");
    detail.className = "detail";
  
    const colLeft = document.createElement("div");
    colLeft.className = "col left";
  
    const foodName = document.createElement("div");
    foodName.className = "name";
    foodName.innerText = name;
  
    colLeft.appendChild(foodName);
    detail.appendChild(colLeft);
  
    const colRight = document.createElement("div");
    colRight.className = "col right";
  
    const foodCost = document.createElement("div");
    foodCost.className = "cost";
    foodCost.innerText = cost;
  
    colRight.appendChild(foodCost);
  
    foodCost.addEventListener("click", function() {
      const link = document.createElement("a");
      link.href = imageLink; // 替换为你要下载的图片链接变量
      link.download = "image.jpg"; // 替换为你要下载的图片文件名
      link.target = "_blank";
      link.click();
    });
  
    detail.appendChild(colRight);
  
    foodCard.appendChild(detail);
  
    container.appendChild(foodCard);
  }
  
  // 根据图片链接数量创建图片卡片
  /*
  imageLinks.forEach((link, index) => {
    createImageCard(link,"文案:","[文案内容]" + index , 5 );
  });
  */
 function createTextBoxFromArray(text) {
  const container = document.querySelector(".container");

  const textBox = document.createElement("textarea");
  textBox.rows = text.length;
  textBox.value = text.map((value, index) => `第${index+1}张: ${value}`).join("\n");

  // 设置文本框样式
  textBox.style.width = "1"; // 设置宽度
  textBox.style.height = "200px"; // 设置高度
  textBox.style.whiteSpace = "nowrap"; // 禁用自动换行

  container.appendChild(textBox);
}
