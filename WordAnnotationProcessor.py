import os

import util


class WordAnnotationProcessor:
    _LABELS = {'项目名': 'PROJ',
               '高管名': 'EXEC',
               '币名': 'COIN',
               '人名': 'NAME',
               '公司名': 'COMP',
               '机构名': 'ORGA'}

    def __init__(self, data, result_dir, result_fname):
        if not os.path.exists(result_dir):
            os.mkdir(result_dir)
        self.data = data
        self.result_dir = result_dir
        self.result_fname = result_fname
        try:
            self.word_info = data['word_info']
            self.label_info = data['label_info']
        except:
            print('Wrong Data Format!')
            exit()
        self.label_list = self.label_info['label_list']
        self.word_list = self.word_info['word_list']
        self.pos_list = self.word_info['pos_list']
        self.index_list = self.word_info['index_list']
        self.ann_list = list()

    def generate_ann_list(self):
        for i in range(0, len(self.word_list)):
            # 若label_list为空或者不存在，单词为--”O“
            if self.label_list is None or self.label_list == []:
                self.ann_list.append('O')
                continue

            result = list()
            word = self.word_list[i]

            # 将下列注释掉的代卖恢复，可以打印出文章中broken case的情况
            for label in self.label_list:
                l_start = label['start']
                l_end = label['end']
                w_start = self.index_list[i]['start']
                w_end = self.index_list[i]['end']

                if w_end <= l_start or w_start >= l_end:
                    pass
                elif w_start < l_start and w_end == l_end:
                    # print('Mode A, Case No.1')
                    # print('word: %s\t\tlabel: %s' % (word, label))
                    result.append('B-' + self._LABELS[label['label']])
                elif w_start < l_start and w_end > l_end:
                    # print('Mode A, Case No.3')
                    # print('word: %s\t\tlabel: %s' % (word, label))
                    result.append('B-' + self._LABELS[label['label']])
                elif w_start < l_start and w_end > l_start:
                    # print('Mode B, Case No.4')
                    # print('word: %s\t\tlabel: %s' % (word, label))
                    result.append('B-' + self._LABELS[label['label']])
                elif w_start == l_start and w_end <= l_end:
                    result.append('B-' + self._LABELS[label['label']])
                elif w_start == l_start and w_end > l_end:
                    # print('Mode A, Case No.2')
                    # print('word: %s\t\tlabel: %s' % (word, label))
                    result.append('B-' + self._LABELS[label['label']])
                elif w_start > l_start and w_end <= l_end:
                    result.append('I-' + self._LABELS[label['label']])
                elif w_start > l_start and w_start < l_end and w_end > l_end:
                    result.append('I-' + self._LABELS[label['label']])
                    # index = util.find_begin_index(i - 1, self.ann_list)
                    # if self.index_list[index]['start'] < l_start:
                    #     print('---------\tMode B, Case No. 6\t---------')
                    #     print('word: %s\t\tlabel: %s' % (word, label))
                    # else:
                    #     print('Mode B, Case No.5')
                    #     print('word: %s\t\tlabel: %s' % (word, label))

            if len(result) == 0:
                self.ann_list.append('O')
            elif len(result) > 1:
                result.reverse()
                for r in result:
                    if r[0] == 'B':
                        self.ann_list.append(r)
                        break
            else:
                self.ann_list.append(result[0])

    def set_labels(self, label_dict):
        self._LABELS = label_dict

    def process_file(self):
        self.generate_ann_list()
        result_file = os.path.join(self.result_dir, 'format_' + self.result_fname + '.txt')
        util.write_to_file(result_file, self.word_list, self.pos_list, self.ann_list)
