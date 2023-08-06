### [中](README_ZH.md)|En
<p align="center">
  <a href="https://openhownet.thunlp.org/">
    <img src="openhownet-logo.png" width = "300"  alt="OpenHowNet Logo" align=center />
  </a>
</p>

<p align="center">
  <a href="https://openhownet.readthedocs.io/" target="_blank">
    <img src="https://readthedocs.org/projects/openhownet/badge/?version=latest" alt="ReadTheDoc Status">
  </a>
  <a  href="https://pypi.org/project/OpenHowNet/"  target="_blank">
    <img src="https://img.shields.io/pypi/v/OpenHowNet?label=pypi" alt="PyPI version">
  </a>
  <a  href="https://github.com/thunlp/OpenHowNet/releases"  target="_blank">
    <img src="https://img.shields.io/github/v/release/thunlp/OpenHowNet" alt="GitHub release (latest by date)">  
  </a>
  <a target="_blank">
    <img alt="GitHub" src="https://img.shields.io/github/license/thunlp/OpenHowNet">
  </a>
   <a target="_blank">
    <img src="https://img.shields.io/badge/PRs-Welcome-red" alt="PRs are Welcome">
  </a>
</p>

OpenHowNet API is developed by [THUNLP](http://thunlp.org/), which provides a convenient way to search information in HowNet, display sememe trees, calculate word similarity via sememes, etc. You can also visit our [website](https://openhownet.thunlp.org) to enjoy searching and exhibiting sememes of words online.


If you use any data or API provided by OpenHowNet in your research, please cite the following paper:

```
@article{qi2019openhownet,
    title={OpenHowNet: An Open Sememe-based Lexical Knowledge Base},
    author={Qi, Fanchao and Yang, Chenghao and Liu, Zhiyuan and Dong, Qiang and Sun, Maosong and Dong, Zhendong},
    journal={arXiv preprint arXiv:1901.09957},
    year={2019},
}
```

## Introduction to HowNet

HowNet is the most typical *sememe* knowledge base. A sememe is defined as the minimum semantic unit in linguistics, and some linguists believe that the meanings of all words in any language can be represented by a limited set of sememes. Mr Zhendong Dong and his son Qiang Dong put this idea into practice, and spent almost 30 years building HowNet, which predefines about 2,000 sememes and uses them to annotate over 200,000 senses of English and Chinese words.

Since HowNet was constructed, it has been widely utilized in various NLP tasks. You can refer to [this paper list](https://github.com/thunlp/SCPapers) to take a look at all the HowNet-related studies.

## HowNet Dictionary

HowNet core data file (namely HowNet dictionary that can be downloaded [here](https://openhownet.thunlp.org/download)) consists of 237,973 concepts (or senses) represented by Chinese & English words and phrases. Each concept in HowNet is annotated with a sememe-based definition, the POS tag, sentiment orientation, example sentences, etc. Here is an example of how concepts are annotated in HowNet:


```
NO.=000000026417 	# Concept ID
W_C=不惜 	# Chinese word
G_C=verb 	# POS tag of the Chinese word
S_C=PlusFeeling|正面情感 	# Sentiment orientation
E_C=~牺牲业余时间，~付出全部精力，~出卖自己的灵魂 	# Example sentences of the Chinese word
W_E=do not hesitate to 	# English word 
G_E=verb 	# POS tag of the English word
S_E=PlusFeeling|正面情感 	# Sentiment orientation
E_E=               	# Example sentences of the English word
DEF={willing|愿意} 	# Sememe-based definition
RMK=
```


## OpenHowNet API

### Installation

You can choose either of the following two methods to install OpenHowNet API.

1. **Installation via pip** (recommended)

```bash
pip install OpenHowNet
```

2. **Installation via Github**


```bash
git clone https://github.com/thunlp/OpenHowNet/
cd OpenHowNet
python setup.py install
```

##### Requirements


* Python>=3.6
* anytree>=2.4.3
* tqdm>=4.31.1
* requests>=2.22.0

### Core Data Type

* **HowNetDict**：HowNet dictionary class, which encapsulates the core functions such as HowNet core data retrieval, presentation, similarity calculation, etc.
* **Sense**：The class that encapsulates the information of concepts in HowNet, mainly including Chinese and English words, POS, sememe-based definition, etc.
* **Sememe**：The class that encapsulates the information of sememes in HowNet, including Chinese and English words describing a sememe, frequency of a sememe in HowNet, and the relationship between sememes.

### Basic Usage

The following code snippets illustrate some basic functions of OpenHowNet API. You can also download this [Jupyter Notebook](OpenHowNet_demo.ipynb) to run the code. For more functions and detailed information, please turn to our [documentation](https://openhownet.readthedocs.io/).


#### Initialization


```python
import OpenHowNet
hownet_dict = OpenHowNet.HowNetDict()
```

An error will occur if you haven't downloaded the HowNet data. In this case you need to run `OpenHowNet.download()` first.


#### Get Concepts Represented by a Word

By default, the api will search HowNet for all the concepts (senses) represented by the given word (in English or Chinese) and return a list of instances in the Sense class. You can also set the language to reduce search time. If the given word does not exist in HowNet, this api will return an empty list.

```python
>>> # Get all the senses represented by the word "苹果".
>>> result_list = hownet_dict.get_sense("苹果")
>>> print("The number of retrievals: ", len(result_list))
The number of retrievals:  8
 
>>> print("An example of retrievals: ", result_list)
An example of retrievals:  [No.244401|apple|苹果, No.244402|malus pumila|苹果, No.244403|orchard apple tree|苹果, No.244396|apple|苹果, No.244397|apple|苹果, No.244398|IPHONE|苹果, No.244399|apple|苹果, No.244400|iphone|苹果]
```

You can get the detailed information of a sense by the Sense instance.

```python
>>> sense_example = result_list[0]
>>> print("Sense example:", sense_example)
Sense example: No.244401|apple|苹果
>>> print("Sense id: ",sense_example.No)
Sense id:  000000244401
>>> print("English word in the sense: ", sense_example.en_word)
English word in the sense:  apple
>>> print("Chinese word in the sense: ", sense_example.zh_word)
Chinese word in the sense:  苹果
>>> print("HowNet Def of the sense: ", sense_example.Def)
HowNet Def of the sense:  {tree|树:{reproduce|生殖:PatientProduct={fruit|水果},agent={~}}}
>>> print("Sememe list of the sense: ", sense_example.get_sememe_list())
Sememe list of the sense:  {fruit|水果, tree|树, reproduce|生殖}
```

You can visualize the structured sememe-based definition of a sense  (namely the "sememe tree") 


```python
>>> sense_example.visualize_sememe_tree()
[sense]No.244401|apple|苹果
└── [None]tree|树
    └── [agent]reproduce|生殖
        └── [PatientProduct]fruit|水果
```

#### Get All Words and Sememes in HowNet

The package provides api to get all the senses, words and sememes in HowNet.


```python
>>> all_senses = hownet_dict.get_all_senses()
>>> print("The number of all senses: {}".format(len(all_senses)))
The number of all senses: 237974
  
>>> zh_word_list = hownet_dict.get_zh_words()
>>> print("Chinese words in HowNet: ",zh_word_list[:30])
Chinese words in HowNet:  ['', '"', '#', '#号标签', '$', '$.J.', '$A.', '$NZ.', '%', "'", '(', ')', '*', '+', ',', '-', '--', '.', '...', '...为止', '...也同样使然', '...以上', '...以内', '...以来', '...何如', '...内', '...出什么问题', '...发生了什么', '...发生故障', '...家里有几口人']

>>> en_word_list = hownet_dict.get_en_words()
>>> print("English words in HowNet: ",en_word_list[:30])
English words in HowNet:  ['A', 'An', 'Frenchmen', 'Frenchwomen', 'Ottomans', 'a', 'aardwolves', 'abaci', 'abandoned', 'abbreviated', 'abode', 'aboideaux', 'aboiteaux', 'abscissae', 'absorbed', 'acanthi', 'acari', 'accepted', 'acciaccature', 'acclaimed', 'accommodating', 'accompanied', 'accounting', 'accused', 'acetabula', 'acetified', 'aching', 'acicula', 'acini', 'acquired']

>>> all_sememes = hownet_dict.get_all_sememes()
>>> print('There are {} sememes in HowNet'.format(len(all_sememes)))
There are 2540 sememes in HowNet
```

#### Get Sememes of a Word

You can retrieve sememe-based definitions of the senses represented by the given word. By default, the package will retrieve all the senses represented by the word and return their sememe list separately.


```python
>>> hownet_dict.get_sememes_by_word(word = '苹果', display='list', merge=False, expanded_layer=-1, K=None)
[{'sense': No.244396|apple|苹果,
  'sememes': {PatternValue|样式值, SpeBrand|特定牌子, able|能, bring|携带, computer|电脑}},
 {'sense': No.244397|apple|苹果, 
  'sememes': {fruit|水果}},
 {'sense': No.244398|IPHONE|苹果,
  'sememes': {PatternValue|样式值, SpeBrand|特定牌子, able|能, bring|携带, communicate|交流, tool|用具}},
 {'sense': No.244399|apple|苹果,
  'sememes': {PatternValue|样式值, SpeBrand|特定牌子, able|能, bring|携带, communicate|交流, tool|用具}},
 {'sense': No.244400|iphone|苹果,
  'sememes': {PatternValue|样式值, SpeBrand|特定牌子, able|能, bring|携带, communicate|交流, tool|用具}},
 {'sense': No.244401|apple|苹果, 
  'sememes': {fruit|水果, reproduce|生殖, tree|树}},
 {'sense': No.244402|malus pumila|苹果,
  'sememes': {fruit|水果, reproduce|生殖, tree|树}},
 {'sense': No.244403|orchard apple tree|苹果,
  'sememes': {fruit|水果, reproduce|生殖, tree|树}}]
```

By changing  `display` , the sememes of a sense can be displayed in list form(`list`), dictionary form(`dict`), tree node form(`tree`) and visualization form(`visual`).
```python
# Get the sememes in the form of dictionary
>>> hownet_dict.get_sememes_by_word(word='苹果',display='dict')[0]
{'sense': No.244396|apple|苹果, 'sememes': {'role': 'sense', 'name': No.244396|apple|苹果, 'children': [{'role': 'None', 'name': computer|电脑, 'children': [{'role': 'modifier', 'name': PatternValue|样式值, 'children': [{'role': 'CoEvent', 'name': able|能, 'children': [{'role': 'scope', 'name': bring|携带, 'children': [{'role': 'patient', 'name': '$'}]}]}]}, {'role': 'patient', 'name': SpeBrand|特定牌子}]}]}}

# Get the sememes in the form of tree node (get the root node of the sememe tree)
>>> d.get_sememes_by_word(word='苹果',display='tree')[0]
{'sense': No.244396|apple|苹果, 'sememes': Node('/No.244396|apple|苹果', role='sense')}

# Visualize the sememes (Set K to control the num of visualized tree to print)
>>> d.get_sememes_by_word(word='苹果',display='visual',K=2)
Find 8 result(s)
Display #0 sememe tree
[sense]No.244396|apple|苹果
└── [None]computer|电脑
    ├── [modifier]PatternValue|样式值
    │   └── [CoEvent]able|能
    │       └── [scope]bring|携带
    │           └── [patient]$
    └── [patient]SpeBrand|特定牌子

Display #1 sememe tree
[sense]No.244397|apple|苹果
└── [None]fruit|水果
```

Besides, when `display=='list'` , you can choose to merge all the sememe lists into one and limit the expand layer of the sememe trees by changing the parameter `expanded_layer`(-1 means expanding all layers).


```python
>>> hownet_dict.get_sememes_by_word(word = '苹果', display='list', merge=True, expanded_layer=-1, K=None)
{PatternValue|样式值, SpeBrand|特定牌子, able|能, bring|携带, communicate|交流, computer|电脑, fruit|水果,
 reproduce|生殖, tool|用具, tree|树}
```


#### Get Relationship Between Two Sememes 

You can get the relationship between two sememes by inputting the words (English or Chinese) that represent the sememes. You can choose to show the triplets of (sememe1, relation, sememe2).


```python
>>> relations = hownet_dict.get_sememe_relation('FormValue','圆', return_triples=False)
>>> print(relations)
'hyponym'

>>> triples = hownet_dict.get_sememe_relation('FormValue','圆', return_triples=True)
>>> print(triples)
[(FormValue|形状值, 'hyponym', round|圆)]
```


#### Get Related Sememes with a Sememe

You can search all the sememes that have a certain relation with a sememe. Similarly, a sememe should be represented by a word (English or Chinese), but the relation must be in lowercase English. 


```python
>>> triples = hownet_dict.get_related_sememes('FormValue', relation = 'hyponym',return_triples=True)
>>> print(triples)
[(FormValue|形状值, 'hyponym', round|圆), (FormValue|形状值, 'hyponym', unformed|不成形), (AppearanceValue|外观值, 'hyponym', FormValue|形状值), (FormValue|形状值, 'hyponym', angular|角), (FormValue|形状值, 'hyponym', square|方), (FormValue|形状值, 'hyponym', netlike|网), (FormValue|形状值, 'hyponym', formed|成形)]
```

### Advanced Features

#### 1: Sememe-based Word Similarity and Similar Words


The implementation is based on the paper:


> Jiangming Liu, Jinan Xu, Yujie Zhang. An Approach of Hybrid Hierarchical Structure for Word Similarity Computing by HowNet. In Proceedings of IJCNLP 2013. [[pdf](https://www.aclweb.org/anthology/I13-1120.pdf)]


##### Extra Initialization

Because there are some files required to be loaded for similarity calculation, the initialization overhead will be larger than before.

 To begin with, you can initialize the `hownet_dict` object as follows:


```python
>>> hownet_dict_advanced = OpenHowNet.HowNetDict(init_sim=True)
Initializing OpenHowNet succeeded!
Initializing similarity calculation succeeded!
```


You can also postpone the initialization of similarity calculation until use.


```python
>>> hownet_dict.initialize_similarity_calculation()
Initializing similarity calculation succeeded!
```

##### Get senses that have exactly the same sememes

You can get senses that have the same sememe-based definition with a sense.

```python
>>> s = hownet_dict_advanced.get_sense('苹果')[0]
>>> hownet_dict_advanced.get_sense_synonyns(s)[:10]
[No.110999|pear|山梨, No.111007|hawthorn|山楂, No.111009|haw|山楂树, No.111010|hawthorn|山楂树, No.111268|Chinese hawthorn|山里红, No.122955|Pistacia vera|开心果树, No.122956|pistachio|开心果树, No.122957|pistachio tree|开心果树, No.135467|almond tree|扁桃, No.154699|fig|无花果]
```

##### Get top-K nearest words for a word

The package search for senses that are represented by the given word,  obtains the nearest top-K senses, and returns the corresponding words. Note that the language of the given word should be set. 

You can also set the POS of words, choose to output the similarity, and merge all words belonging to difference senses into a single list, etc. Please see the [documentation](https://openhownet.readthedocs.io/) for more information. 

If the input word is not in HowNet, the api returns an empty list.


```python
>>> hownet_dict_advanced.get_nearest_words('苹果', language='zh',K=5)
{No.244396|apple|苹果: ['IBM', '东芝', '华为', '戴尔', '索尼'],
 No.244397|apple|苹果: ['丑橘', '乌梅', '五敛子', '凤梨', '刺梨'],
 No.244398|IPHONE|苹果: ['OPPO', '华为', '苹果', '智能手机', '彩笔'],
 No.244399|apple|苹果: ['OPPO', '华为', '苹果', '智能手机', '彩笔'],
 No.244400|iphone|苹果: ['OPPO', '华为', '苹果', '智能手机', '彩笔'],
 No.244401|apple|苹果: ['山梨', '山楂', '山楂树', '山里红', '开心果树'],
 No.244402|malus pumila|苹果: ['山梨', '山楂', '山楂树', '山里红', '开心果树'],
 No.244403|orchard apple tree|苹果: ['山梨', '山楂', '山楂树', '山里红', '开心果树']}
>>> hownet_dict_advanced.get_nearest_words('苹果', language='zh',K=5, merge=True)
['IBM', '东芝', '华为', '戴尔', '索尼']
```


##### Calculate the similarity between two words


If either of the two given words does not exist in HowNet,  it will return `-1`.


```python
>>> print('The similarity of 苹果 and 梨 is {}.'.format(hownet_dict_advanced.calculate_word_similarity('苹果','梨')))
The similarity of 苹果 and 梨 is 1.0.
```

#### 2: BabelNet Synset Dictionary

This package integrates query function for information of synsets in BabelNet (BabelNet synset). [BabelNet](https://babelnet.org/) is a multilingual encyclopedia dictionary composed of BabelNet synsets, each of which contains some multilingual synonyms that have the same meaning. The following work annotates sememes for some BabelNet synsets, and the function in this part is based on its annotation results.

> **Towards Building a Multilingual Sememe Knowledge Base: Predicting Sememes for BabelNet Synsets**. *Fanchao Qi, Liang Chang, Maosong Sun, Sicong Ouyang and Zhiyuan Liu*. AAAI-20. [[pdf](https://arxiv.org/pdf/1912.01795.pdf)] [[code](https://github.com/thunlp/BabelNet-Sememe-Prediction)]

##### Extra Initialization
To begin with, you should initialize the BabelNet synset dictionary:

```python
>>> hownet_dict.initialize_babelnet_dict()
Initializing BabelNet synset Dict succeeded!
# Or you can initialize when create the HowNetDict instance
>>> hownet_dict_advanced = HowNetDict(init_babel=True)
Initializing OpenHowNet succeeded!
Initializing BabelNet synset Dict succeeded!
```

##### BabelNet synset information
The following API allows you to query the rich information in a BabelNet synset (Chinese and English synonyms, definitions, picture urls, etc.).

```python
>>> syn_list = hownet_dict_advanced.get_synset('黄色')
>>> print("{} results are retrieved and take the first one as an example".format(len(syn_list)))
3 results are retrieved and take the first one as an example

>>> syn_example = syn_list[0]
>>> print("Synset: {}".format(syn_example))
Synset: bn:00113968a|yellow|黄

>>> print("English synonyms: {}".format(syn_example.en_synonyms))
English synonyms: ['yellow', 'yellowish', 'xanthous']

>>> print("Chinese synonyms: {}".format(syn_example.zh_synonyms))
Chinese synonyms: ['黄', '黄色', '淡黄色+的', '黄色+的', '微黄色', '微黄色+的', '黄+的', '淡黄色']

>>> print("English glosses: {}".format(syn_example.en_glosses))
English glosses: ['Of the color intermediate between green and orange in the color spectrum; of something resembling the color of an egg yolk', 'Having the colour of a yolk, a lemon or gold.']

>>> print("Chinese glosses: {}".format(syn_example.zh_glosses))
Chinese glosses: ['像丝瓜花或向日葵花的颜色。']
```

##### BabelNet synset relations
You can get the related BabelNet synsets with a given synset.

```python
>>> related_synsets = syn_example.get_related_synsets()
>>>print("There are {} synsets that have relation with the {}, they are: ".format(len(related_synsets), syn_example))
There are 6 synsets that have relation with the bn:00113968a|yellow|黄, they are: 

>>>print(related_synsets)
[bn:00099663a|chromatic|彩色, bn:00029925n|egg_yolk|蛋黄, bn:00092876v|resemble|相似, bn:00020726n|color|颜色, bn:00020748n|visible_spectrum|可见光, bn:00081866n|yellow|黄色]
```

##### Get sememe annotations of a BabelNet synset
You can get the sememes of BabelNet synsets by inputting the word in the BabelNet synsets:

```python
>>> print(hownet_dict_advanced.get_sememes_by_word_in_BabelNet('黄色'))
[{'synset': bn:00113968a|yellow|黄, 'sememes': [yellow|黄]}, {'synset': bn:00101430a|dirty|淫秽的, 'sememes': [lascivious|淫, dirty|龊, despicable|卑劣, BadSocial|坏风气]}, {'synset': bn:00081866n|yellow|黄色, 'sememes': [yellow|黄]}]

>>> print(hownet_dict_advanced.get_sememes_by_word_in_BabelNet('黄色',merge=True))
[lascivious|淫, despicable|卑劣, BadSocial|坏风气, dirty|龊, yellow|黄]
```

For more detailed instructions, please refer to the [documentation](https://openhownet.readthedocs.io/).

## Citation

If the code or data help you, please cite the following paper:

```
@article{qi2019openhownet,
  title={Openhownet: An open sememe-based lexical knowledge base},
  author={Qi, Fanchao and Yang, Chenghao and Liu, Zhiyuan and Dong, Qiang and Sun, Maosong and Dong, Zhendong},
  journal={arXiv preprint arXiv:1901.09957},
  year={2019}
}
```
