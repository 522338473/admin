class Pagination(object):
    """
    自定义分页
    """

    def __init__(self, current_page, total_count, base_url, params, per_page_count=7, max_pager_count=11):
        '''
        :param current_page: 从前端get请求传过来的页码
        :param total_count:  总共的数据长度
        :param base_url: URL前缀
        :param per_page_count: 每一页显示的数据
        :param max_pager_count: 所有的数据/每页的数据=页码
        '''
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1
        if current_page <= 0:
            current_page = 1
        # 获取到当前的页面
        self.current_page = current_page

        # 数据总条数
        self.total_count = total_count

        # 每页显示10条数据
        self.per_page_count = per_page_count

        # 页面上应该显示的最大页码
        max_page_num, div = divmod(total_count, per_page_count)
        if div:  # 如果有剩余，页码 = 页码+1
            max_page_num += 1
        self.max_page_num = max_page_num

        # 页面上默认显示11个页面（当前页在中间）
        self.max_pager_count = max_pager_count
        # max_pager_count最大的页码

        # 中间页面
        self.half_max_pager_count = int((max_pager_count - 1) / 2)

        # URL前缀
        self.base_url = base_url

        import copy
        params = copy.deepcopy(params)
        params._mutable = True
        self.params = params
        print("self.Params", self.params)

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_count

    @property
    def end(self):
        return self.current_page * self.per_page_count

    def page_html(self):
        # 如果总页数 <= 11
        if self.max_page_num <= self.max_pager_count:
            pager_start = 1
            pager_end = self.max_page_num
        # 如果总页数 > 11
        else:
            # 如果当前页 <= 5
            if self.current_page <= self.half_max_pager_count:
                pager_start = 1
                pager_end = self.max_pager_count
            else:
                # 当前页 + 5 > 总页码
                if (self.current_page + self.half_max_pager_count) > self.max_page_num:
                    # 当前的页码+中间的页码大于最长的页码（最后五个页码的时候执行）
                    pager_end = self.max_page_num  # 不指定结束位置会一直往后走
                    pager_start = self.max_page_num - self.max_pager_count + 1
                else:  # 中间的其它数据执行
                    pager_start = self.current_page - self.half_max_pager_count
                    pager_end = self.current_page + self.half_max_pager_count

        page_html_list = []
        self.params["page"] = 1
        first_page = "<li><a href='%s?%s'>首页</a></li>" % (self.base_url, self.params.urlencode())
        page_html_list.append(first_page)
        for i in range(pager_start, pager_end + 1):
            self.params["page"] = i
            # range遍历顾头不顾尾，所以末尾+1
            if i == self.current_page:
                # 如果遍历的结果为当前获取到的页面，执行if
                temp = '<li class="active"><a href="%s?%s">%s</a></li>' % (self.base_url, self.params.urlencode(), i,)
            else:
                temp = '<li><a href="%s?%s">%s</a></li>' % (self.base_url, self.params.urlencode(), i,)
            page_html_list.append(temp)
        self.params["page"] = self.max_page_num
        last_page = "<li><a href='%s?%s'>尾页</a></li>" % (self.base_url, self.params.urlencode())
        page_html_list.append(last_page)

        return ''.join(page_html_list)
