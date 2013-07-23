expense
=======

python写的简易的收支管理系统，基于webpy，目标：能用，够用！

依赖：
-------

1. python2.6/2.7。2.5和3.x没测试；2.4肯定不行，放弃吧少年。
2. web.py0.37 (基于这个版本开发的)

使用：
-------

1. 默认使用sqlite数据库，存放在 data/ 目录下，expense.db是数据库文件，tbl.sql是建表sql语句；create.sh用于初始化一个空的数据库文件。如果有需要可以改成使用mysql，但是。。没必要吧？
2. 配置分散在config.py和local\_config.py里头，一般不建议修改config.py，除非你知道你在做啥。一般来说改 local\_config.py 就够了，包括端口、数据库配置，以及人员配置（小A、小B、小C什么的……）
3. 使用start.sh启动server，然后默认的9999端口就可以访问了。
4. 如果有必要的话，可以使用apache/nginx的转发来访问：  

    upstream expense {
        server 127.0.0.1:9999;
    }

    server {
        server_name example.com;
        location / {
            proxy_pass http://expense;
        }
    }

5. 如果需要用户名和密码的话，修改 local\_config.py 里的 need\_login = True 即可。同时可以修改/添加用户名和密码。
