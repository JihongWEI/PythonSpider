### 搭建开发环境

首先，确认系统安装的Python版本是3.5.x：

    
    
    $ python3 --version
    Python 3.5.1
    

然后，用`pip`安装开发Web App需要的第三方库：

异步框架aiohttp：

    
    
    $pip3 install aiohttp
    

前端模板引擎jinja2：

    
    
    $ pip3 install jinja2
    

MySQL 5.x数据库，从[官方网站](http://dev.mysql.com/downloads/mysql/5.6.html)下载并安装，安装完毕后
，请务必牢记root口令。为避免遗忘口令，建议直接把root口令设置为`password`；

MySQL的Python异步驱动程序aiomysql：

    
    
    $ pip3 install aiomysql
    

### 项目结构

选择一个工作目录，然后，我们建立如下的目录结构：

    
    
    awesome-python3-webapp/  <-- 根目录
    |
    +- backup/               <-- 备份目录
    |
    +- conf/                 <-- 配置文件
    |
    +- dist/                 <-- 打包目录
    |
    +- www/                  <-- Web目录，存放.py文件
    |  |
    |  +- static/            <-- 存放静态文件
    |  |
    |  +- templates/         <-- 存放模板文件
    |
    +- ios/                  <-- 存放iOS App工程
    |
    +- LICENSE               <-- 代码LICENSE
    

创建好项目的目录结构后，建议同时建立git仓库并同步至GitHub，保证代码修改的安全。

要了解git和GitHub的用法，请移步[Git教程](http://www.liaoxuefeng.com/wiki/001373951630592960
6dd18361248578c67b8067c8c017b000)。

### 开发工具

自备，推荐用Sublime Text，请参考[使用文本编辑器](/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014316399410395f704750ee9440228135925a6ca1dad8000)。

### 参考源码

[day-01](https://github.com/michaelliao/awesome-python3-webapp/tree/day-01)

