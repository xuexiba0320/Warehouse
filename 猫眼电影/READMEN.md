猫眼的字体文件是`动态加载`的，每次刷新都会变，虽然字体中定义的只有 0-9 这9个数字，但是编码和顺序都是会变的。

就是说，这个字体文件中“EA0B”代表“9”，在别的文件中就不是了。但是`字的形状不变`，即描绘字体的参数点（坐标）。

下载一个字体文件，命名为 base.woff，然后利用 fontstore 网站查看编码和实际值的对应关系，手工做成字典并保存下来。爬虫爬取的时候，下载字体文件，根据网页源码中的编码，在字体文件中找到“字形”，再循环跟 base.woff 文件中的“字形”做比较，“字形”一样那就说明是同一个字了。在 base.woff 中找到“字形”后，获取“字形”的编码，而之前我们已经手工做好了编码跟值的映射表，由此就可以得到我们实际想要的值了。

