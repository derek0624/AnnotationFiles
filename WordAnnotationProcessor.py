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

    def cut_words(self):
        self.word_list = self.word_info['word_list']
        self.pos_list = self.word_info['pos_list']
        self.index_list = self.word_info['index_list']

    def generate_ann_list(self):
        for i in range(0, len(self.word_list)):
            # 若label_list为空或者不存在，单词为--”O“
            if self.label_list is None or self.label_list == []:
                self.ann_list.append('O')
                continue

            result = list()

            for label in self.label_list:
                l_start = label['start']
                l_end = label['end']
                w_start = self.index_list[i]['start']
                w_end = self.index_list[i]['end']

                if w_end <= l_start or w_start >= l_end:
                    pass
                elif w_start < l_start and w_end == l_end:
                    result.append('B-' + self._LABELS[label['label']])
                elif w_start < l_start and w_end > l_end:
                    result.append('B-' + self._LABELS[label['label']])
                elif w_start < l_start and w_end > l_start:
                    result.append('B-' + self._LABELS[label['label']])
                elif w_start == l_start and w_end <= l_end:
                    result.append('B-' + self._LABELS[label['label']])
                elif w_start == l_start and w_end > l_end:
                    result.append('B-' + self._LABELS[label['label']])
                elif w_start > l_start and w_end <= l_end:
                    result.append('I-' + self._LABELS[label['label']])
                elif w_start > l_start and w_start < l_end and w_end > l_end:
                    result.append('I-' + self._LABELS[label['label']])

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
