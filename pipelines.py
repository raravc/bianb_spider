# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter #暂时没用到

import os
# class BianbPipeline:
#     file_name = "bianb.md"  # 文件名称,实际上要用name命名，待修改
#     file = None  # 文件对象
#
#     def open_spider(self, spider):
#         # 以追加形式打开文件
#         self.file = open(self.file_name, "a", encoding="utf-8")
#
#     def process_item(self, item, spider):
#         my_string = '\n'.join(item["content"])
#         content_str = item['name']+"\n"+\
# 		item["time"]+"  "+\
# 		item["area"]+"\n"+\
# 		my_string+"\n"
#
#         self.file.write(content_str)
#
#         return item
#
#     def close_spider(self, spider):
#         # 关闭文件
#         self.file.close()
import html2text

class BianbPipeline:
    def process_item(self, item, spider):
        file_name = item['name'] + ".md"  # 使用item的'name'字段作为文件名
        file_path = os.path.join("/Users/raravc/Desktop/爬虫文件夹", file_name)  # 修改为实际的文件保存路径

        with open(file_path, "w", encoding="utf-8") as file:
            my_string = html2text.html2text(item['content'])
            file.write(my_string)
        with open(file_path,'a',encoding='utf-8') as f:
            f.write(item['time'])

        return item