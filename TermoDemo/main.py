import joblib

import pandas as pd
from transformers import BertTokenizer
from scipy.sparse import csr_matrix


from pymorphy3 import MorphAnalyzer
import nltk
from nltk.corpus import stopwords

an = MorphAnalyzer(lang='ru')
stops = stopwords.words('russian')

def main():
    model_choice = 0
    while (model_choice != 8):
        model_choice = 0
        print(choose_model_message)

        next_available = model_choice >= 1 and model_choice <= 8

        while (not next_available):
            try:
                model_choice = int(input(your_choice_message))
                next_available = model_choice >= 1 and model_choice <= 8
                if (not next_available):
                    print(error_message_try_again)
                else:
                    print()
                    print()
            except:
                print(error_message_try_again)
        
        if (model_choice != 8):
            vectorizer_choice = 1
            
            if (model_choice != 7):
                print(choose_vectorization_message)
                try:
                    vectorizer_choice = int(input(your_choice_message))
                    print()
                    print()
                except:
                    pass

            message = input(give_us_message_message)
            
            getResult(model_choice, vectorizer_choice, message)
        else:
            print("Всего доброго!")

def getResult(model_choice, vectorizer_choice, message):
    filename = ""

    if (model_choice == 1):
        filename += "gradient"
    elif (model_choice == 2):
        filename += "random"
    elif (model_choice == 3):
        filename += "svc"
    elif (model_choice == 4):
        filename += "knn"
    elif (model_choice == 5):
        filename += "logistic"
    elif (model_choice == 6):
        filename += "perceptron"
    else:
        for i in range(1, 7):
            getResult(i, 1, message)
            getResult(i, 2, message)
        
        return
    
    if (vectorizer_choice == 1):
        filename += "Bag"
    else:
        filename += "Bert"

    filename += ".sav"

    print("\033[96m" + "Загрузка модели..." + "\033[0m")
    model = joblib.load("models/" + filename)

    try:
        print("\033[96m" + "В процессе анализ с использованием модели: " + getModelName(model_choice) + " (" + getVectorizationName(vectorizer_choice) + ")..." + "\033[0m")
        if (vectorizer_choice == 1):
            vectorizer = joblib.load("vectorizers/bagVectorizer.sav")
            vectorized_message = vectorizer.transform([getClearSentences(message)])
        else:
            vectorized_message = getBertVectorizedMessage(message) 

        if (model.predict(vectorized_message)[0]):
            print("\033[91m" + "Сообщение суицидальное" + "\033[0m")
        else:
            print("\033[92m" + "Сообщение не относится к суицидальным" + "\033[0m")
    except:
        print("\033[93m" + "Произошла ошибка во время исполнения. Вероятно, сообщение включает в себя неизвестные слова и его требуется внести в датасет." + "\033[0m")


    print()

def getModelName(model_choice):
    name = ""

    if (model_choice == 1):
        name += "Градиентный бустинг"
    elif (model_choice == 2):
        name += "Случайный лес"
    elif (model_choice == 3):
        name += "Метод опорных векторов"
    elif (model_choice == 4):
        name += "k-ближайших соседей"
    elif (model_choice == 5):
        name += "Логистическая регрессия"
    elif (model_choice == 6):
        name += "Перцептрон"

    return name

def getVectorizationName(choice):
    name = ""

    if (choice == 1):
        name += "Мешок слов"
    else:
        name += "BERT"

    return name
    

def getClearSentences(sentences):
    return " ".join(str(s) + "" for s in (an.normal_forms(y)[0] for y in filter(lambda x: x not in stops, nltk.word_tokenize(str(sentences)))))

def getBertVectorizedMessage(message):
    data = pd.read_csv("PreparedDatasets/shuffled.csv")
    corpus = pd.concat([data['text'].apply(lambda x: getClearSentences(x)), pd.Series([getClearSentences(message)])])

    tokenizer = BertTokenizer.from_pretrained('cointegrated/rubert-tiny2')

    bert_tokenized = corpus.apply(lambda ser: tokenizer.convert_tokens_to_ids(tokenizer.tokenize(ser)))
    bert_list = bert_tokenized.tolist()

    nRows = len(bert_list)
    nCols = max(max(row) if (len(row) > 0) else 0 for row in bert_list) + 1

    dataIn = []
    indices = []
    indptr = [0]

    for row in bert_list:
        indices.extend(row)
        dataIn.extend([1] * len(row))
        indptr.append(len(indices))

    return csr_matrix((dataIn, indices, indptr), shape=(nRows, nCols))[-1:]

choose_model_message = '''Выберите модель, которой хотите воспользоваться.
    1. Градиентный бустинг
    2. Случайный лес
    3. Метод опорных векторов
    4. К-ближайших соседей
    5. Логистическая регрессия
    6. Перцептрон

    7. Демонстрационный режим

    8. Выход

'''

your_choice_message = "Ваш выбор: "

choose_vectorization_message = '''Какую векторизацию использовать?
    1. Bag of words (Default)
    2. BERT

'''

give_us_message_message = "Введите сообщение, которое требуется проанализировать: "

error_message_try_again = "Такой вариант отсутствует. Попробуйте снова."

main()
