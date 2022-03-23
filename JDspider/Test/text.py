a=" \rzha ng\n\t "
print(a)
print(len(a))
b=a.strip()
print(b)
print(len(b))

res = 'https://item.jd.com/100030603242.html'
goods_id = res.rsplit('/', 1)[1].split('.')[0]
print(goods_id)