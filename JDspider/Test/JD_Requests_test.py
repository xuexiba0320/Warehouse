from lxml import etree

with open('doc.txt', 'r+', encoding='utf-8') as f:
    data = f.read()

# 问题：使用正则如何操作切分
data_list = []
# response = data.split('</script>', 1)[1].split('<script>')[0]
# print(response)
doc = etree.HTML(data)
dataset = doc.xpath('//div[@class="gl-i-wrap"]')
print(len(dataset))
for data in dataset:
    data_dict = {}
    title = data.xpath('./div[@class="p-name p-name-type-2"]/a/em/text()')
    price = data.xpath('./div[@class="p-price"]//i/text()')
    shop = data.xpath('./div[@class="p-shop"]//a/@title')
    link = data.xpath('./div[@class="p-name p-name-type-2"]/a/@href')[0]
    data_dict['标题'] = title
    data_dict['价格'] = price
    data_dict['店铺'] = shop
    data_dict['链接'] = 'https:' + link
    data_list.append(data_dict)

print(data_list)