import os

import util


class CharAnnotationProcessor:
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
        self.word_list = list()
        self.pos_list = list()
        self.label_list = self.label_info['label_list']
        self.location_list = list()
        self.ann_list = list()

    def cut_words(self):
        words = self.word_info['word_list']
        pos = self.word_info['pos_list']
        for i in range(len(words)):
            word = words[i]
            flag = pos[i]

            if len(word) == 1:
                self.word_list.append(word)
                self.pos_list.append(flag)
                self.location_list.append('S')
            else:
                for i in range(0, len(word)):
                    if i == 0:
                        self.location_list.append('B')
                    else:
                        self.location_list.append('I')
                    self.word_list.append(word[i])
                    self.pos_list.append(flag)

    def generate_ann_list(self):
        for i in range(0, len(self.word_list)):
            # 若label_list为空或者不存在，单词为--”O“
            if self.label_list is None or self.label_list == []:
                self.ann_list.append('O')
                continue

            record = len(self.ann_list)
            for label in self.label_list:
                l_start = label['start']
                l_end = label['end']

                if i == l_start:
                    self.ann_list.append('B-' + self._LABELS[label['label']])
                elif l_end > i > l_start:
                    self.ann_list.append('I-' + self._LABELS[label['label']])

            if record == len(self.ann_list):
                self.ann_list.append('O')

    def process_file(self):
        self.cut_words()
        self.generate_ann_list()
        result_file = os.path.join(self.result_dir, 'format_' + self.result_fname + '.txt')
        util.write_to_file(result_file, self.word_list, self.pos_list, self.location_list, self.ann_list,
                           is_keep_space=True)
