# Annotation Files
将txt格式的文本和人工标注完成的ann格式标注文件，整合成BIO2格式的文件用于之后深度学习的学习。
Example: 
![](ReadMe/%E6%9C%AA%E7%9F%A5.png)


## 特点
* 采用BIO格式：（⚠️：[LABEL]为任意的标签）
	* B-[LABEL] ==> 标签的开头
	* I -LABEL ==> 标签中间以及结尾部分
	* O  ==> 所有未被标签的词或者字

* 支持三种不同的分割文本方式
	* Word: 结巴分词分割
	* Char： 按照单个字符分割
	* Element： 定义英文单词、一组数字和中文单个字符为Element,以此来进行分割

## 导入数据
使用util.load\_data(‘DIR’)导入所有txt文本进行分词，记录词性以及单词的位置；对ann标注文件会储存其标注类型，标注词在文本中的位置，最后在DIR下生成一个pxl序列化文件以便以后读取。注意，DIR中的文本和标注需要一一对应。
```
import util
data = util.load_data('DIR')

# 如分割算法、格式或者数据有所变化可以使用util.update_data('DIR')进行更新。
data = util.updata_data('DIR')
```

## 使用方法
若需要按照Word格式来处理文本和标注文件，可以使用WordAnnotationProcessor.py。 具体使用方法如下。
```
import util
import WordAnnotationProcessor

# 定义data的路径位置
DATA_DIR = 'data/'
train_data = util.load_data(DATA_DIR)
WORD_DIR = 'word_outputs/'

# 遍历train_data里所有的item
for item in train_data:
    word_ap = WordAnnotationProcessor.WordAnnotationProcessor(train_data[item], WORD_DIR, item)
    word_ap.process_file()
```

WordAnnotationProcessor会在WORD_DIR下对于每个item都生成一个以word来切割文本并用\tab来分割词语，词语的词性和BIO格式的标注。并且句子与句子之间用\n来分割
```
原文：
CPChain物信链将基于QTUM量子链并行开发，聚焦底层协议和物联网技术研发

BIO-Word格式：
CPChain	eng	B-PROJ
物	ng	B-PROJ
信链	n	I-PROJ
将	d	O
基于	p	O
QTUM	eng	B-PROJ
量子	n	B-PROJ
链	n	I-PROJ
并行	v	O
开发	v	O
，	x	O
聚焦	v	O
底层	n	O
协议	n	O
和	c	O
物	n	O
联网	nz	O
技术	n	O
研发	j	O
```

同理，CharAnnotationProcessor.py和ElementAnnotationProcessor.py可以将文本和标注文件制作成基于Char分割和Element分割的BIO格式文本文件。只需将WordAnnotationProcessor替换。

## 整合
Util中提供了方法—util.generate\_annotation\_file(‘OUTPUT_DIR’)来将文件夹中所有的文件整合成一个文件。也可以自己定义顺序来进行整合。
```
# generate_annotation会根据文件夹中的文件名进行排序(字符串排序)，所以会不完全按照文本后的序号进行排序。
util.generate_annotation_file(WORD_DIR, word_dst_file)

#sl
for i in range(1, 1000):
    src_file = src_file + '/format_sl_' + str(i) + '.txt'
    if os.path.isfile(src_file):
        with open(src_file, 'r', encoding='utf-8') as sf, open(dst_file, 'a+', encoding='utf-8') as df:
            for line in sf.readlines():
                df.write(line)

# Jinsecaijing
for i in range(1, 1000):
    src_file = src_file + '/format_jinsecaijing_' + str(i) + '.txt'
    if os.path.isfile(src_file):
        with open(src_file, 'r', encoding='utf-8') as sf, open(dst_file, 'a+', encoding='utf-8') as df:
            for line in sf.readlines():
                df.write(line)
```
