import requests


def sp5():
    """翻页设置limit参数，只需要发送一次请求就可以了，就不需要每次都请求18个数据不断访问网站"""
    i = 0
    for i in range(5):
        url = 'https://spa5.scrape.center/api/book/?limit=18&offset={}'.format(i)
        res = requests.get(url).json()
        data = res['results']
        num = i*18
        for j in data:
            i = num +1
            name = j['name']
            authors = ','.join(j['authors']).replace('\n','').strip().replace(' ','')
            cover = j['cover']
            score = j['score']

            print(name, '--',authors, '--', score, '--', cover)
            # 如何将数据整理对齐？？？
            """
            认知心理学及其启示 -- 约翰•R•安德森 -- 8.8 -- https://img9.doubanio.com/view/subject/l/public/s7059106.jpg
            银河帝国2：基地与帝国 -- [美]艾萨克·阿西莫夫,读客文化,银河帝国 -- 9.0 -- https://img3.doubanio.com/view/subject/l/public/s9117163.jpg
            银河帝国：基地 -- [美]艾萨克·阿西莫夫,读客文化,银河帝国 -- 9.0 -- https://img9.doubanio.com/view/subject/l/public/s8973055.jpg
            小学教材全解-四年级语文下 -- 薛金星 -- 7.3 -- https://img9.doubanio.com/view/subject/l/public/s24506696.jpg
            越界言论（第3卷） -- 许子东 -- 8.3 -- https://img3.doubanio.com/view/subject/l/public/s22696330.jpg
    
            """
    print(i)

if __name__ == '__main__':
    sp5()