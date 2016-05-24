由于我们的Web App建立在asyncio的基础上，因此用aiohttp写一个基本的`app.py`：

    
    
    import logging; logging.basicConfig(level=logging.INFO)
    
    import asyncio, os, json, time
    from datetime import datetime
    
    from aiohttp import web
    
    def index(request):
        return web.Response(body=b'<h1>Awesome</h1>')
    
    @asyncio.coroutine
    def init(loop):
        app = web.Application(loop=loop)
        app.router.add_route('GET', '/', index)
        srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
        logging.info('server started at http://127.0.0.1:9000...')
        return srv
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()
    

运行`python app.py`，Web App将在`9000`端口监听HTTP请求，并且对首页`/`进行响应：

    
    
    $ python3 app.py
    INFO:root:server started at http://127.0.0.1:9000...
    

这里我们简单地返回一个`Awesome`字符串，在浏览器中可以看到效果：

![awesome-home](http://www.liaoxuefeng.com/files/attachments/0014327731340820dbf437504bb4436a96036b490048551000/l)

这说明我们的Web App骨架已经搭好了，可以进一步往里面添加更多的东西。

### 参考源码

[day-02](https://github.com/michaelliao/awesome-python3-webapp/tree/day-02)

