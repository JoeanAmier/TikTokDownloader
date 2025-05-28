# Cookie 获取教程

本教程仅演示部分能够获取所需 `Cookie` 的方法，仍有其他方法能够获取所需 `Cookie`；本教程使用的浏览器为 `Microsoft Edge`
，部分浏览器的开发人员工具可能不支持中文语言。

**方法一\(推荐\)：**

1. 打开浏览器\(可选无痕模式启动\)，访问`https://www.douyin.com/`
2. 登录抖音账号\(可跳过\)
3. 按 `F12` 打开开发人员工具
4. 选择 `网络` 选项卡
5. 勾选 `保留日志`
6. 在 `筛选器` 输入框输入 `cookie-name:odin_tt`
7. 点击加载任意一个作品的评论区
8. 在开发人员工具窗口选择任意一个数据包\(如果无数据包，重复步骤7\)
9. 全选并复制 `Cookie` 的值
10. 运行 `main.py` ，根据提示写入 `Cookie`

**截图示例：**

<img src="screenshot/Cookie获取教程1.png" alt="开发人员工具">

**方法二\(不适用本项目\)：**

1. 打开浏览器\(可选无痕模式启动\)，访问`https://www.douyin.com/`
2. 登录抖音账号\(可跳过\)
3. 按 `F12` 打开开发人员工具
4. 选择 `控制台` 选项卡
5. 输入 `document.cookie` 后回车确认
6. 检查 `Cookie` 是否包含 `passport_csrf_token` 和 `odin_tt` 字段
7. 如果未包含所需字段，尝试刷新网页或者点击加载任意一个作品的评论区，回到步骤5
8. 全选并复制 `Cookie` 的值
9. 运行 `main.py` ，根据提示写入 `Cookie`

**截图示例：**

<img src="screenshot/Cookie获取教程2.png" alt="开发人员工具">

# device_id 参数

`device_id` 参数获取方法与 Cookie 类似。

<img src="screenshot/device_id获取示例图.png" alt="开发人员工具">
