import os

import CharAnnotationProcessor
import ElementAnnotationProcessor
import WordAnnotationProcessor
import WordStat
import util

if __name__ == '__main__':
    DATA_DIR = 'data/'
    TEST_DATA_DIR = '测试集/'
    train_data = util.load_data(DATA_DIR)
    test_data = util.load_data(TEST_DATA_DIR)
    print('Loading Complete!')
    ELE_DIR = 'element_outputs/'
    WORD_DIR = 'word_outputs/'
    TEST_CHAR_DIR = 'test_char_outputs/'
    CHAR_DIR = 'char_outputs/'
    ele_dst_file = './ELEMENT_ANNOTATION_RESULT.txt'
    word_dst_file = './WORD_ANNOTATION_RESULT.txt'
    char_dst_file = './CHAR_ANNOTATION_RESULT.txt'
    test_char_dst_file = './TEST_CHAR_ANNOTATION_RESULT.txt'

    for item in train_data:
        element_ap = ElementAnnotationProcessor.ElementAnnotationProcessor(train_data[item], ELE_DIR, item)
        element_ap.process_file()

        char_ap = CharAnnotationProcessor.CharAnnotationProcessor(train_data[item], TEST_CHAR_DIR, item)
        char_ap.process_file()

        word_ap = WordAnnotationProcessor.WordAnnotationProcessor(train_data[item], WORD_DIR, item)
        word_ap.process_file()
        ws = WordStat.WordFormat(item, word_ap.ann_list, word_ap.word_list,
                                 word_ap.label_list, word_ap.index_list)

    # util.generate_annotation_file(ELE_DIR, ele_dst_file)
    # util.generate_annotation_file(WORD_DIR, word_dst_file)
    # util.generate_annotation_file(CHAR_DIR, char_dst_file)

    # 最初顺序
    # 共享财经
    dst_file = ''
    src_dir = ''

    for i in range(1, 1000):
        src_file = dst_file + '/format_sl_' + str(i) + '.txt'
        if os.path.isfile(src_file):
            with open(src_file, 'r', encoding='utf-8') as sf, open(dst_file, 'a+', encoding='utf-8') as df:
                for line in sf.readlines():
                    df.write(line)
    print('共享财经：DONE!')

    # 金色财经
    for i in range(1, 1000):
        src_file = dst_file + '/format_jinsecaijing_' + str(i) + '.txt'
        if os.path.isfile(src_file):
            with open(src_file, 'r', encoding='utf-8') as sf, open(dst_file, 'a+', encoding='utf-8') as df:
                for line in sf.readlines():
                    df.write(line)
    print('金色财经：DONE!')

    # 测试集
    test_dst_file = ''
    test_src_dir = ''
    for i in range(1, 1000):
        src_file = test_src_dir + '/format_jinsecaijing_' + str(i) + '.txt'
        if os.path.isfile(src_file):
            with open(src_file, 'r', encoding='utf-8') as sf, open(test_dst_file, 'a+', encoding='utf-8') as df:
                for line in sf.readlines():
                    df.write(line)
    print('共享财经：DONE!')

    for i in range(1, 1000):
        src_file = test_src_dir + '/format_jinsecaijing_' + str(i) + '_b.txt'
        if os.path.isfile(src_file):
            with open(src_file, 'r', encoding='utf-8') as sf, open(test_dst_file, 'a+', encoding='utf-8') as df:
                for line in sf.readlines():
                    df.write(line)
    print('金色财经：DONE!')
    print('Process Complete!')
