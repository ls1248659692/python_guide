#!/usr/bin/python
# coding=utf8
from collections import Counter

import jieba

__author__ = 'Jam'
__date__ = '2019/7/11 14:53'


class JiebaUtil:

    @staticmethod
    def get_cut_words(sentence, userdict_path):
        if userdict_path is not None:
            jieba.load_userdict(userdict_path)
        seg_list = jieba.cut(sentence)

        return Counter(seg_list).most_common(10)

    @staticmethod
    def get_words(content, topk=10):
        seg_list = jieba.cut(content)

        c = Counter()
        for x in seg_list:
            if len(x) > 1 and x != '\r\n':
                c[x] += 1
        print('常用词频度统计结果')
        for (k, v) in c.most_common(topk):
            print(k)
            print('*' * int(v / 3), v)


if __name__ == '__main__':
    sentence = "朱宇清，女，主任医师，副教授，现任国际医疗部二病区主任，国际医疗部门诊主任，内科学及急诊医学硕士，硕士研究生导师。兼任中华中医药学会急诊分会及中西医结合试验医学专业委员会委员、北京朝阳区医学鉴定委员会和全军医学鉴定委员会专家，世界急危重症医学杂志编委。学习工作经历：1985-1990年就读于河北医科大学并获得临床医学学士学位，1995-1998年就读于首都医科大学，获得内科学硕士学位，2005-2006年在法国巴黎第六大学急诊医学专业学习并获得急诊医学硕士学位。1990-2001年在北京同仁医院急诊科从事急诊临床工作，并于1997年起担任急诊科副主任，负责急诊科的医疗和科研教学工作。2001-2009年在中日友好医院急诊科先后担任副主任医师、主任医师，主管过EICU和抢救区的医疗工作，并于1994年起担任急诊科副主任，负责科室的医疗、教学和科研工作。2009年以来担任中日友好医院国际医疗部二病区主任，负责二病区的全面工作。专业特长：从事急诊临床工作19年，熟练掌握内科各专科疾病急、危重期的救治原则，具有全面扎实的抢救技术水平和丰富的危重症治疗经验，同时在老年多科病的综合治疗上具有一定的优势。先后管理重症监护病房8年，熟练掌握循环支持监测、机械通气治疗与监测、营养支持等危重症治疗监测技术，在急性呼吸衰竭、心功能衰竭，脓毒症，多脏器功能衰竭等危重症救治上具有较丰富的临床经验。曾承担和参与了临床科研课题研究4项，目前在首发基金资助的一项关于脓毒症的综合救治联合攻关课题中担任子课题负责人。培养、指导硕士研究生6人，在国内、外医学杂志发表医学论文20余篇，参与编写医学著作3部。"
    seg_weight = JiebaUtil.get_cut_words(sentence, r'./data/society_name.txt')
    JiebaUtil.get_words(sentence)
    for word,weight in seg_weight:
        print(word,weight)
