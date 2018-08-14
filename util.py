import os
import pickle
import re

import jieba.posseg as pseg
import pandas as pd


def is_sentence_ends(index, word_list):
    end_punctuation = ['。', '？', '！', '?', '!', '\n', '；', ';']

    possible_end_punctuation = ['\"', '”', '）', '」', ')', '\'']

    word = word_list[index]
    if word in end_punctuation + possible_end_punctuation and \
            0 < index < (len(word_list) - 1):
        next_word = word_list[index + 1]
        pre_word = word_list[index - 1]

        if word in possible_end_punctuation:
            if pre_word in end_punctuation and \
                    next_word not in end_punctuation + possible_end_punctuation:
                return True
        elif next_word in possible_end_punctuation:
            pass
        elif next_word not in end_punctuation:
            return True
    elif word in end_punctuation and index == len(word_list) - 1:
        return True

    return False


def init_data(data_dir, data_dict={}):
    dir_list = os.listdir(data_dir)
    dir_list.sort()
    for item in dir_list:
        file = data_dir + item
        if os.path.isdir(file):
            data_dict = init_data(file + '/', data_dict)
        elif os.path.isfile(file) and item[0] != '.':
            if item[-4:] == '.txt':
                word_info = generate_word_info(file)
                data_dict.setdefault(item[:-4], {'word_info': dict(),
                                                 'label_info': dict()})
                data_dict[item[9:-4]]['word_info'] = word_info
            elif item[-4:] == '.ann':
                label_info = generate_label_info(file)
                data_dict.setdefault(item[:-4], {'word_info': dict(),
                                                 'label_info': dict()})
                data_dict[item[7:-4]]['label_info'] = label_info
    return data_dict


def generate_word_info(file):
    word_list = list()
    pos_list = list()
    index_list = list()

    with open(file, 'r', encoding='utf-8-sig') as f:
        content = f.read()
        content = content.replace('\u3000', ' ')
        content = content.replace('\xa0', ' ')
        pos_words = pseg.cut(content)
        index = 0

        for word, flag in pos_words:
            word_list.append(word)
            pos_list.append(flag)
            start = index
            end = start + len(word)
            index = end
            index_list.append({'start': start,
                               'end': end})
    word_info = {'word_list': word_list,
                 'pos_list': pos_list,
                 'index_list': index_list}
    return word_info


def generate_label_info(file):
    label_list = list()
    with open(file, 'r', encoding='utf-8-sig') as f:
        for line in f.readlines():
            label = line.split()
            label_dict = {}
            label_dict['label'] = label[1]
            label_dict['start'] = int(label[2])
            label_dict['end'] = int(label[3])
            word = ''
            for s in label[4:]:
                word += s
            label_dict['word'] = word
            label_list.append(label_dict)

    label_info = {'label_list': label_list}
    return label_info


def update_data(data_dir):
    pkl_data = os.path.join(data_dir, 'data.pkl')
    data = init_data(data_dir)
    with open(pkl_data, 'wb') as f:
        pickle.dump(data, f)
    return data


def load_data(data_dir):
    pkl_data = os.path.join(data_dir, 'data.pkl')
    if not os.path.exists(pkl_data):
        data = update_data(data_dir)
    else:
        with open(pkl_data, 'rb') as f:
            data = pickle.load(f)
    return data


def find_begin_index(index, ann_list):
    while index >= 0 and ann_list[index][0] != 'B':
        index -= 1
    if index == 0 and ann_list[index][0] != 'B':
        print('ERROR! CAN"T FIND WHERE LABEL BEGINS')
        exit()
    return index


def is_empty_sentence(index_list, word_list):
    sentence = ''
    for index in index_list:
        word = word_list[index]
        sentence += word

    sentence = sentence.replace(' ', '')
    sentence = sentence.replace('\t', '')
    sentence = sentence.replace('\n', '')
    return True if sentence == '' else False


def is_diff_language(word1, word2):
    if (is_chinese_word(word1) and not is_chinese_word(word2)) or \
            (not is_chinese_word(word1) and is_chinese_word(word2)):
        return True
    else:
        return False


def format_space(index_list, word_list, keep_space=False):
    start = index_list[0]
    end = index_list[-1]
    tmp_list = list()
    while start < index_list[-1] and (word_list[start] == ' ' or word_list[start] == '\t'):
        start += 1

    while end > start and (word_list[end] == ' ' or word_list[end] == '\t'):
        end -= 1

    for index in index_list:
        if end >= index >= start:
            tmp_list.append(index)

    if keep_space:
        index_list = tmp_list
        tmp_list = list()
        for index in index_list:
            if word_list[index] == ' ' and is_diff_language(word_list[index + 1], word_list[index - 1]):
                pass
            else:
                tmp_list.append(index)

    return tmp_list


def write_to_file(dst_file, word_list, *lst, is_keep_space=False):
    # 初始化句子index列表
    sentence = list()
    with open(dst_file, 'w', encoding='utf-8') as f:
        for i in range(len(word_list)):
            word = word_list[i]
            if is_sentence_ends(i, word_list):
                sentence = format_space(sentence, word_list, keep_space=is_keep_space)
                if is_empty_sentence(sentence, word_list):
                    continue
                for index in sentence:
                    if word_list[index] == '\n':
                        pass
                    else:
                        line = word_list[index] + '\t'
                        for l in lst[:-1]:
                            line += l[index] + '\t'
                        line += lst[-1][index]
                        line += '\n'
                        f.write(line)
                f.write('\n')
                sentence = list()
            else:
                if word == ' ' and (word_list[i + 1] == ' ' or word_list[i + 1] == '\t'):
                    continue
                elif word == '\t' or word == '|':
                    continue
                else:
                    sentence.append(i)


def is_chinese_word(word):
    """
    检查是都是中文单词
    :param content_raw:
    :return:
    """
    pattern_string = r"(^[\u4e00-\u9fa5]+$)"  # 20902字 基本汉字
    chinese_pattern = re.compile(pattern_string)
    result = chinese_pattern.match(word)
    return True if result else False


def generate_segmented_sequences(input_file, output_dir="./"):
    """
        获取训练词向量的文本
        :param input_file:
        :return:
        """
    out_fh1 = open(os.path.join(output_dir, 'sent_text_ICO.txt'), 'w')
    with open(input_file) as fh:
        sentence_text = []

        for line in fh:
            line = line.rstrip()
            if not line:
                out_fh1.write(''.join(sentence_text) + '\n')
                sentence_text = []
            else:
                word = line.split('\t')[0]
                sentence_text.append(word)
    out_fh1.close()


def generate_sentence_word_count(input_file='./sent_text_ICO.txt', output_dir="./"):
    sentence_list = list()
    word_count = list()
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            sentence_list.append(line[:-1])
            count = len(line[:-1])
            word_count.append(count)

        pd.DataFrame({"index": list(range(1, len(word_count) + 1)),
                      "sentence": sentence_list,
                      "word_count": word_count}).to_csv(os.path.join(output_dir, 'Char_SentenceCharCount.csv'),
                                                        index=False, header=True)


def generate_annotation_file(src_dir, dst_file):
    fpath, fname = os.path.split(dst_file)
    if not os.path.exists(fpath):
        os.mkdir(fpath)

    # 建立或清空目标文件
    if not os.path.exists(dst_file):
        f = open(dst_file, 'w')
        f.close()

    dir_list = os.listdir(src_dir)
    dir_list.sort()
    for item in dir_list:
        file_name = os.path.join(src_dir, item)
        if os.path.isdir(file_name):
            generate_annotation_file(file_name, dst_file)
        elif os.path.isfile(file_name) and item[0] != '.':
            with open(file_name, 'r', encoding='utf-8') as sf, open(dst_file, 'a+', encoding='utf-8') as df:
                for line in sf.readlines():
                    df.write(line)

# Old Version
# def write_to_file(dst_file, word_list, *lst):
#     with open(dst_file, 'w', encoding='utf-8') as f:
#         for i in range(len(word_list)):
#             word = word_list[i]
#             # 空行不写入文件
#             if word == '\n':
#                 pass
#             elif word == ' ' and word_list[i + 1] == ' ':
#                 continue
#             elif word == '\t' or word == '\|' or word == '|':
#                 continue
#             else:
#                 line = word_list[i] + '\t'
#                 for l in lst:
#                     line += l[i] + '\t'
#                 line += '\n'
#                 f.write(line)
#
#             # 判断分句
#             if is_sentence_ends(i, word_list):
#                 f.write('\n')
