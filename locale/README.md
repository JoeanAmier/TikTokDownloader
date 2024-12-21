# 命令参考

**运行命令前，确保已经安装了 `gettext` 软件包，并配置好环境变量。**

**Before running the command, ensure that the `gettext` package is installed and the environment variables are properly
configured.**

* `xgettext --files-from=py_files.txt -d tk -o tk.pot`
* `mkdir zh_CN\LC_MESSAGES`
* `msginit -l zh_CN -o zh_CN/LC_MESSAGES/tk.po -i tk.pot`
* `mkdir en_US\LC_MESSAGES`
* `msginit -l en_US -o en_US/LC_MESSAGES/tk.po -i tk.pot`
* `msgmerge -U zh_CN/LC_MESSAGES/tk.po tk.pot`
* `msgmerge -U en_US/LC_MESSAGES/tk.po tk.pot`

# 翻译贡献指南

* 如果想要贡献支持更多语言，请在终端切换至 `locale` 文件夹，运行命令 `msginit -l 语言代码 -o 语言代码/LC_MESSAGES/tk.po -i tk.pot`
  生成 po 文件并编辑翻译。
* 如果想要贡献改进翻译结果，请直接编辑 `tk.po` 文件内容。
* 仅需提交 `tk.po` 文件，作者会转换格式并合并。

# Translation Contribution Guide

* If you want to contribute support for more languages, please switch to the `locale` folder in the terminal and run the
  command `msginit -l language_code -o language_code/LC_MESSAGES/tk.po -i tk.pot` to generate the po file and edit the
  translation.
* If you want to contribute to improving the translation, please directly edit the content of the `tk.po` file.
* Only the `tk.po` file needs to be submitted, and the author will convert the format and merge it.
