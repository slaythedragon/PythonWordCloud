import pandas as  pd
import re
import collections
import jieba

from pyecharts.charts import WordCloud
from pyecharts import options as opts

'''
找出喜欢的岗位做岗位描述的分析，并做出词云图
'''

# 读取数据
data = pd.read_excel('work_all.xlsx')
# 为了不影响原数据，所以拷贝一份
data_cy = data.copy()
# 提取指定岗位的数据
# 注意：岗位类别需要处理空字符问题，岗位类别后都有一个空格，要去除空格才能读出来
# 去除空格
A = data_cy['岗位类别'].str.strip()
# 把去除空格后的数据更改到原数据中
data_cy['岗位类别'] = A

'''
把属于数据运营、机器学习、数据科学、数据分析师、数据产品经理、商业数据分析的数据筛选出来，
并把其'岗位类别'列中的值全部替换为'数据科学'。
'''
# 把属于这些类别的提取出来放到B中
B = A.isin(['数据运营', '机器学习', '数据科学', '数据分析师', '数据产品经理', '商业数据分析'])
# 把这些岗位的类别都替换为数据科学
data_cy.loc[B, '岗位类别'] = '数据科学'

# 提取岗位类别为数据科学的数据
res = data_cy[data_cy['岗位类别'] == '数据科学']
# 更改到原数据中
data_cy = res


# 拼接所有岗位类别为数据科学的岗位描述
string_data = ''
for i in data_cy['岗位描述']:
    string_data += str(i)


# 文本预处理，去除各种标点符号，不然统计词频时会统计进去
# 定义正则表达式匹配模式，其中的|代表或
pattern = re.compile(u'\t|\n| |；|\.|。|：|：\.|-|:|\d|;|、|，|\)|\(|\?|"')
# 将符合模式的字符去除，re.sub代表替换，把符合pattern的替换为空
string_data = re.sub(pattern, '', string_data)

# 文本分词
seg_list_exact = jieba.cut(string_data, cut_all=False)  # 精确模式分词
# object_list  = list(seg_list_exact) # list()函数可以把可迭代对象转为列表

# 运用过滤词表优化掉常用词，比如“的”这些词，不然统计词频时会统计进去
object_list = []

# 读取过滤词表
with open('./remove_words.txt', 'r', encoding="utf-8") as fp:
    remove_words = fp.read().split()

# 循环读出每个分词
for word in seg_list_exact:
    #看每个分词是否在常用词表中或结果是否为空或\xa0不间断空白符，如果不是再追加
    if word not in remove_words and word != ' ' and word != '\xa0':
        object_list.append(word)  # 分词追加到列表


# 词频统计
word_counts = collections.Counter(object_list)  # 对分词做词频统计
word_counts_top = word_counts.most_common(100)  # 获取前100最高频的词

# 绘图
# https://gallery.pyecharts.org/#/WordCloud/wordcloud_custom_mask_image
# 去pyecharts官网找模板代码复制出来修改
c = (
    WordCloud()
    .add("", word_counts_top)#根据词频最高的词
    .render("wordcloud.html")#生成页面
)
