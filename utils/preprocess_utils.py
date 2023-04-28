import jieba
import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer



# 定义一个函数，用于对中文文本进行预处理
def preprocess_chinese(text):
    # 分词
    tokens = jieba.cut(text)
    # 去除停用词
    stop_words = set(['的', '了', '是', '和', '在', '就', '也', '都', '与', '等'])
    filtered_tokens = [token for token in tokens if token not in stop_words]
    # 返回处理后的文本
    return ' '.join(filtered_tokens)

# 定义一个函数，用于对英文文本进行预处理
def preprocess_english(text):
    # 分词
    tokens = word_tokenize(text)
    # 去除停用词
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
    # 词形还原
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    # 返回处理后的文本
    return ' '.join(lemmatized_tokens)

# 定义一个函数，用于对中英文文本进行预处理
def preprocess(text):
    # 分离中英文文本
    chinese_text = text.split(' ')[0]
    english_text = ' '.join(text.split(' ')[1:])
    # 对中英文分别进行预处理
    processed_chinese_text = preprocess_chinese(chinese_text)
    processed_english_text = preprocess_english(english_text)
    # 将处理后的结果合并起来
    processed_text = processed_chinese_text + ' ' + processed_english_text
    # 返回处理后的文本
    return processed_text
