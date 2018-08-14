import os

import util


class ElementAnnotationProcessor:
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
        self.index_list = list()
        self.label_list = self.label_info['label_list']
        self.location_list = list()
        self.ann_list = list()

    def cut_words(self):
        words = self.word_info['word_list']
        pos = self.word_info['pos_list']
        index = 0

        for i in range(len(words)):
            word = words[i]
            flag = pos[i]

            if len(word) == 1 or not util.is_chinese_word(word):
                self.word_list.append(word)
                self.pos_list.append(flag)
                self.location_list.append('S')
                start = index
                index = start + len(word)
                end = index
                self.index_list.append({'start': start,
                                        'end': end})
            else:
                for i in range(0, len(word)):
                    if i == 0:
                        self.location_list.append('B')
                    else:
                        self.location_list.append('I')
                    self.word_list.append(word[i])
                    self.pos_list.append(flag)

                    start = index
                    end = start + 1
                    index = end
                    self.index_list.append({'start': start,
                                            'end': end})

    def generate_ann_list(self):
        for i in range(0, len(self.word_list)):
            if self.label_list is None or self.label_list == []:
                self.ann_list.append('O')
                continue

            # 用于记录所有可能的答案，若为空则标记为'O'；若有多个答案，取最后一个Begin标签
            result = list()

            for label in self.label_list:
                l_start = label['start']
                l_end = label['end']
                w_start = self.index_list[i]['start']
                w_end = self.index_list[i]['end']

                if w_start <= l_start < w_end < l_end:
                    result.append('B-' + self._LABELS[label['label']])
                elif l_end > w_start > l_start:
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

    def process_file(self):
        self.cut_words()
        self.generate_ann_list()
        result_file = os.path.join(self.result_dir, 'format_' + self.result_fname + '.txt')
        util.write_to_file(result_file, self.word_list, self.pos_list, self.location_list, self.ann_list,
                           is_keep_space=True)

    def set_labels(self, label_dict):
        self._LABELS = label_dict
