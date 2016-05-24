MVVM模式不但可用于Form表单，在复杂的管理页面中也能大显身手。例如，分页显示Blog的功能，我们先把后端代码写出来：

在`apis.py`中定义一个`Page`类用于存储分页信息：

    
    
    class Page(object):
    
        def __init__(self, item_count, page_index=1, page_size=10):
            self.item_count = item_count
            self.page_size = page_size
            self.page_count = item_count // page_size + (1 if item_count % page_size > 0 else 0)
            if (item_count == 0) or (page_index > self.page_count):
                self.offset = 0
                self.limit = 0
                self.page_index = 1
            else:
                self.page_index = page_index
                self.offset = self.page_size * (page_index - 1)
                self.limit = self.page_size
            self.has_next = self.page_index < self.page_count
            self.has_previous = self.page_index > 1
    
        def __str__(self):
            return 'item_count: %s, page_count: %s, page_index: %s, page_size: %s, offset: %s, limit: %s' % (self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit)
    
        __repr__ = __str__
    

在`handlers.py`中实现API：

    
    
    @get('/api/blogs')
    def api_blogs(*, page='1'):
        page_index = get_page_index(page)
        num = yield from Blog.findNumber('count(id)')
        p = Page(num, page_index)
        if num == 0:
            return dict(page=p, blogs=())
        blogs = yield from Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
        return dict(page=p, blogs=blogs)
    

管理页面：

    
    
    @get('/manage/blogs')
    def manage_blogs(*, page='1'):
        return {
            '__template__': 'manage_blogs.html',
            'page_index': get_page_index(page)
        }
    

模板页面首先通过API：`GET /api/blogs?page=?`拿到Model：

    
    
    {
        "page": {
            "has_next": true,
            "page_index": 1,
            "page_count": 2,
            "has_previous": false,
            "item_count": 12
        },
        "blogs": [...]
    }
    

然后，通过Vue初始化MVVM：

    
    
    <script>
    function initVM(data) {
        var vm = new Vue({
            el: '#vm',
            data: {
                blogs: data.blogs,
                page: data.page
            },
            methods: {
                edit_blog: function (blog) {
                    location.assign('/manage/blogs/edit?id=' + blog.id);
                },
                delete_blog: function (blog) {
                    if (confirm('确认要删除“' + blog.name + '”？删除后不可恢复！')) {
                        postJSON('/api/blogs/' + blog.id + '/delete', function (err, r) {
                            if (err) {
                                return alert(err.message || err.error || err);
                            }
                            refresh();
                        });
                    }
                }
            }
        });
        $('#vm').show();
    }
    $(function() {
        getJSON('/api/blogs', {
            page: {{ page_index }}
        }, function (err, results) {
            if (err) {
                return fatal(err);
            }
            $('#loading').hide();
            initVM(results);
        });
    });
    </script>
    

View的容器是`#vm`，包含一个table，我们用`v-repeat`可以把Model的数组`blogs`直接变成多行的`<tr>`：

    
    
    <div id="vm" class="uk-width-1-1">
        <a href="/manage/blogs/create" class="uk-button uk-button-primary"><i class="uk-icon-plus"></i> 新日志</a>
    
        <table class="uk-table uk-table-hover">
            <thead>
                <tr>
                    <th class="uk-width-5-10">标题 / 摘要</th>
                    <th class="uk-width-2-10">作者</th>
                    <th class="uk-width-2-10">创建时间</th>
                    <th class="uk-width-1-10">操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-repeat="blog: blogs" >
                    <td>
                        <a target="_blank" v-attr="href: '/blog/'+blog.id" v-text="blog.name"></a>
                    </td>
                    <td>
                        <a target="_blank" v-attr="href: '/user/'+blog.user_id" v-text="blog.user_name"></a>
                    </td>
                    <td>
                        <span v-text="blog.created_at.toDateTime()"></span>
                    </td>
                    <td>
                        <a href="#0" v-on="click: edit_blog(blog)"><i class="uk-icon-edit"></i>
                        <a href="#0" v-on="click: delete_blog(blog)"><i class="uk-icon-trash-o"></i>
                    </td>
                </tr>
            </tbody>
        </table>
    
        <div v-component="pagination" v-with="page"></div>
    </div>
    

往Model的`blogs`数组中增加一个Blog元素，table就神奇地增加了一行；把`blogs`数组的某个元素删除，table就神奇地减少了一行。所有
复杂的Model-View的映射逻辑全部由MVVM框架完成，我们只需要在HTML中写上`v-repeat`指令，就什么都不用管了。

可以把`v-repeat="blog: blogs"`看成循环代码，所以，可以在一个`<tr>`内部引用循环变量`blog`。`v-text`和`v-att
r`指令分别用于生成文本和DOM节点属性。

完整的Blog列表页如下：

![awesomepy-manage-blogs](http://www.liaoxuefeng.com/files/attachments/0014025813192591fb147e5d8564257b6a94ca831a7f39f000)

### 参考源码

[day-12](https://github.com/michaelliao/awesome-python3-webapp/tree/day-12)

