import scrapy


class Git1Spider(scrapy.Spider):
    name = 'git1'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/xuexiba0320']  # 这是一个登录后才能访问的页面

    def start_requests(self):
        """重构start_requests方法携带cookies"""
        # 抓包获取登录页面的coolies值
        cookies_str = '_octo=GH1.1.1723321190.1633457190; _device_id=c095b04889a8a883d9c4dfebcef2578e; has_recent_activity=1; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; tz=Asia%2FShanghai; tz=Asia%2FShanghai; user_session=_-bwmjVsxJ7Z7hYNBpcounAuEO7OJ1AST16iART1bsSwUhzu; __Host-user_session_same_site=_-bwmjVsxJ7Z7hYNBpcounAuEO7OJ1AST16iART1bsSwUhzu; logged_in=yes; dotcom_user=xuexiba0320; _gh_sess=QJKGgsrR%2FEfHG8NxbgzHC2QWV%2F3zfYmiSUzedVhzUey3wDht7fFMHd3WWH1y869s%2FQ%2F4GSTGkYIfE7aDAB1q3P4zu4f1LAE4QdPxUZBENTdNP8qogEXioD07XDdjoyR1wWCfABfMFJeRIaGMTEIfqNDtpky5EFZaeJ8xna58TTB%2BB3C9%2BTp%2BEDZB4j28i92o0EGbL1hzFI4HE8XiL0QEXEOab72R4g26%2FhnRXN%2FisfbcnJtewFseaoBYezo8BVIuI%2FP966MzeTrH4FwCwnoTHYKaajVtUC8ULfSm%2BTrmNQVGiUBILH7qOo050qemwH2mJ%2FgkF6HoPHQ2rCYJmjcZ1LckAwsDjUM81N%2BSQJzXGgvKzIygzJhRppAbZM1UVXhRS7nPuCXnvqfLxlUlGldOM%2BqRc1pJwXWENWQ0T8rVndO7kFvef31GVc55NvU9mZiOSftJ9i0bfa%2F%2Bw75oAXxNda55J%2BjCEv4bnREbNe%2F76HeDa1aDwkPqkGLdsLkhFPsRvukrr8FcenkBiloRDggWh%2Ft%2F1ZYv4k6XSxjla2UhnLrRqYaX%2B%2BpQGcEJ9e3SSLMgObxSqe5uN4%2FRw4aY%2FUXgKsttvuI3q%2Bf8As8OtUeintdZE%2Ftq5ZePcknuIltqoikeZi4W7Spc4NIFPsJfwJ9%2BhLytA8VX3jLjYioj0U6XdbbnnKFMsXu6bEfpPWZBawd3bE5yO%2BHia0pdKE3Vm24gRaEPx0epb8fLrb%2FZPRT0HfEOCkWYqZRXG8xPo%2FEB4fK5--8rOm3CRvKUG%2B5bBo--2VO%2BnNTkDn7Hvdnq1Vq0uw%3D%3D'
        # 将cookie转化为字典格式
        cookie__dict = {i.split('=')[0]: i.split('=')[-1] for i in cookies_str.split('; ')}
        print(cookie__dict)
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=cookie__dict
        )

    def parse(self, response):
        # response = response.body.decode()
        # # 使用正则提取个人页面的用户名：用户名不带 .GitHub则为登录成功
        # res = re.findall('<title>(.*?)</title>', response)[0]
        # print(res)
        print(response.xpath('/html/head/title/text()').extract_first())
        with open("git_with_post.html", "w")as f:
            f.write(response.body.decode('gbk', 'ignore'))
