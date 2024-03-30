
choose_model_message = '''Выберите модель, которой хотите воспользоваться.
    1. Градиентный бустинг
    2. Случайный лес
    3. Метод опорных векторов
    4. К-ближайших соседей
    5. Логистическая регрессия
    6. Перцептрон

    7. Выход

'''

your_choice_message = "Ваш выбор: "

choose_vectorization_message = '''Какую векторизацию использовать?
    1. Bag of words (Default)
    2. BERT

'''

give_us_message_message = "Введите сообщение, которое требуется проанализировать: "

error_message_try_again = "Такой вариант отсутствует. Попробуйте снова."

def main():
    print("Запуск средства распознавания суицидальных сообщений...")

    model_choice = 0
    while (model_choice != 7):
        model_choice = 0
        print(choose_model_message)

        next_available = model_choice >= 1 and model_choice <= 7

        while (not next_available):
            try:
                model_choice = int(input(your_choice_message))
                next_available = model_choice >= 1 and model_choice <= 7
                if (not next_available):
                    print(error_message_try_again)
            except:
                print(error_message_try_again)
        
        if (model_choice != 7):
            print(choose_vectorization_message)

            vectorizer_choice = 1
            try:
                vectorizer_choice = int(input(your_choice_message))
            except:
                pass

            message = input(give_us_message_message)
            
            getResult(model_choice, vectorizer_choice, message)
        else:
            print("Всего доброго!")

def getResult(model_choice, vectorizer_choice, message):
    print("Анализ выполняется...")

    # вот тут вся эта жесть...

main()