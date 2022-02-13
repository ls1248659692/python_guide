# coding=utf-8

import nltk,os
from nltk.tokenize.stanford_segmenter import StanfordSegmenter
from nltk.tokenize import StanfordTokenizer
from nltk.tag import StanfordNERTagger
from nltk.tag import StanfordPOSTagger
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser

'''替换成自己的jar配置文件路径'''
java_path = r"C:\Program Files\Java\jdk1.8.0_111\bin\java.exe"
os.environ['JAVAHOME'] = java_path


'''1 StanfordSegmenter 中文分词'''
def ch_standseg(mystr):
    segmenter = StanfordSegmenter(path_to_jar=r"E:\tools\stanfordNLTK\jar\stanford-segmenter.jar",path_to_slf4j=r"E:\tools\stanfordNLTK\jar\slf4j-api.jar",path_to_sihan_corpora_dict=r"E:\tools\stanfordNLTK\jar\data",path_to_model=r"E:\tools\stanfordNLTK\jar\data\pku.gz",path_to_dict=r"E:\tools\stanfordNLTK\jar\data\dict-chris6.ser.gz")
    result = segmenter.segment(mystr)
    print(result)
    # return result


'''2 StanfordTokenizer 英文分词'''
def en_standseg(sent):
    tokenizer = StanfordTokenizer(path_to_jar=r"E:\tools\stanfordNLTK\jar\stanford-parser.jar")
    print(tokenizer.tokenize(sent))


'''3 StanfordNERTagger 英文命名实体识别'''
def en_nertagger(str):
     eng_tagger = StanfordNERTagger(model_filename=r'E:\tools\stanfordNLTK\jar\classifiers\english.all.3class.distsim.crf.ser.gz',path_to_jar=r'E:\tools\stanfordNLTK\jar\stanford-ner.jar')
     print(eng_tagger.tag(str))


'''4 StanfordNERTagger 中文命名实体识别'''
def ch_nertagger(str):
    chi_tagger = StanfordNERTagger(model_filename=r'E:\tools\stanfordNLTK\jar\classifiers\chinese.misc.distsim.crf.ser.gz',path_to_jar=r'E:\tools\stanfordNLTK\jar\stanford-ner.jar')
    for word, tag in chi_tagger.tag(str.split()):
        print(word,tag)


'''5 StanfordPOSTagger 英文词性标注：'''
def en_posttag(str):
    eng_tagger = StanfordPOSTagger(model_filename=r'E:\tools\stanfordNLTK\jar\models\english-bidirectional-distsim.tagger',path_to_jar=r'E:\tools\stanfordNLTK\jar\stanford-postagger.jar')
    print(eng_tagger.tag(str.split()))


'''6 StanfordPOSTagger 中文词性标注'''
def ch_posttag(str):
    chi_tagger = StanfordPOSTagger(model_filename=r'E:\tools\stanfordNLTK\jar\models\chinese-distsim.tagger',path_to_jar=r'E:\tools\stanfordNLTK\jar\stanford-postagger.jar')
    print(chi_tagger.tag(str.split()))


'''7 StanfordParser 英文句法分析'''
def en_parser(str): # 待处理
    eng_parser = StanfordParser(r"E:\tools\stanfordNLTK\jar\stanford-parser.jar",r"E:\tools\stanfordNLTK\jar\stanford-parser-3.9.1-models.jar",r"E:\tools\stanfordNLTK\jar\classifiers\englishPCFG.ser.gz")
    print(list(eng_parser.parse(str.split())))


'''8 StanfordParser 中文句法分析'''
def ch_parser(sent):
    chi_parser = StanfordParser(r"E:\tools\stanfordNLTK\jar\stanford-parser.jar",r"E:\tools\stanfordNLTK\jar\stanford-parser-3.9.1-models.jar",r"E:\tools\stanfordNLTK\jar\classifiers\chinesePCFG.ser.gz")
    print(list(chi_parser.parse(sent.split())))


'''9 StanfordDependencyParser 英文依存句法分析'''
def en_depenpaeser(str): # 待处理
    eng_parser = StanfordDependencyParser(r"E:\tools\stanfordNLTK\jar\stanford-parser.jar",r"E:\tools\stanfordNLTK\jar\stanford-parser-3.9.1-models.jar",r"E:\tools\stanfordNLTK\jar\classifiers\englishPCFG.ser.gz")
    res = list(eng_parser.parse(str.split()))
    for row in res[0].triples():
        print(row)

'''10 StanfordDependencyParser 中文依存句法分析'''
def ch_depenpaeser(str):
    chi_parser = StanfordDependencyParser(r"E:\tools\stanfordNLTK\jar\stanford-parser.jar",r"E:\tools\stanfordNLTK\jar\stanford-parser-3.9.1-models.jar",r"E:\tools\stanfordNLTK\jar\classifiers\chinesePCFG.ser.gz")
    res = list(chi_parser.parse(str.split()))
    for row in res[0].triples():
        print(row)



if __name__ == "__main__":
    '''1 StanfordSegmenter 中文分词'''
    ch_standseg(r"我在博客园开了一个博客，我的博客名叫伏草惟存，写了一些自然语言处理的文章。")

    '''2 StanfordTokenizer 英文分词'''
    # en_standseg(r"Good muffins cost $3.88\nin New York. Please buy me\ntwo of them.\nThanks.")

    '''3 StanfordNERTagger 英文命名实体识别'''
    # en_nertagger('Rami Eid is studying at Stony Brook University in NY'.split())

    '''4 StanfordNERTagger 中文命名实体识别'''
    # ch_nertagger(u'四川省 成都 信息 工程 大学 我 在 博客 园 开 了 一个 博客 ， 我 的 博客 名叫 伏草惟存 ， 写 了 一些 自然语言 处理 的 文章 。 \r\n')

    '''5 StanfordPOSTagger 英文词性标注：'''
    # en_posttag(r'What is the airspeed of an unladen swallow ?')

    '''6 StanfordPOSTagger 中文词性标注'''
    # ch_posttag(r'四川省 成都 信息 工程 大学 我 在 博客 园 开 了 一个 博客 ， 我 的 博客 名叫 伏 草 惟 存 ， 写 了 一些 自然语言 处理 的 文章 。 \r\n')

    '''7 StanfordParser 英文句法分析'''
    # en_parser(r"the quick brown fox jumps over the lazy dog")

    '''8 StanfordParser 中文句法分析'''
    # ch_parser(u'北海 已 成为 中国 对外开放 中 升起 的 一 颗 明星')

    '''9 StanfordDependencyParser 英文依存句法分析'''
    # en_depenpaeser(r"the quick brown fox jumps over the lazy dog")

    '''10 StanfordDependencyParser 中文依存句法分析'''
    # ch_depenpaeser(u'四川 已 成为 中国 西部 对外开放 中 升 起 的 一 颗 明星')


