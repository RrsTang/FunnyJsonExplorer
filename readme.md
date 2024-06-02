## 作者

汤焯俊 21307272

## 使用方法

在命令行中使用以下命令即可使用不同的风格与图标族打印json文件

```
python fje.py <-f FILE> <-s STYLE> <-i ICON>
```

以下为参数说明

- -f 或 --file：接受 JSON 文件的路径。
- -s 或 --style：接受显示风格（tree 或 rectangle）。
- -i 或 --icon：接受图标族名称（icon1或icon2）。

如果什么参数都不输入，则默认路径为`test.json`，风格为`tree`，图标族名称为`icon1`。

如果以默认模式运行代码，可直接使用`run.bat`脚本。
