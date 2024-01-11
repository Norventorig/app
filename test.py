import random


def main_choice(words, special_words):
    print()
    print('Остановить программу (0)')
    print('60 слов (1)')
    print('Вперемешку 60 слов (2)')
    print('Введение новых слов (3)')

    variant = input('Выбор:')

    if variant == '1':
        list_keys = [x for x in words.keys()]
        list_keys = list_keys[-1:-31:-1] + list_keys[0:30:1]
        random.shuffle(list_keys)
        standard_test(list_keys, words)
        print("\n" * 2)

    elif variant == '2':
        list_keys = [x for x in words.keys()]
        list_keys = list_keys[-31:-211:-1]
        random.shuffle(list_keys)
        list_keys = list_keys[-1:-61:-1]
        standard_test(list_keys, words)
        print("\n" * 2)

    elif variant == '3':
        list_values = [input("Английское слово ({}): ".format(i_count + 1)) for i_count in range(5)]
        print("\n" * 10)
        list_keys = [input("Перевод {}: ".format(key)) for key in list_values]

        dict_add = dict(zip(list_keys, list_values))
        words.update(dict_add)
        special_words.update(dict_add)

        random.shuffle(list_keys)
        standard_test(list_keys, dict_add)

        for _ in range(5):
            words.pop(next(iter(words)))

        new_dictionary = "{\n"
        for i_key, i_value in words.items():
            new_dictionary += '"{}": "{}",\n'.format(i_key, i_value)
        new_dictionary += '}'
        print('\n' * 10)

        file_opener = open("dict.txt", 'w', encoding="windows-1251")
        file_opener.write(new_dictionary)
        file_opener.close()
        print("\n" * 2)

        new_dictionary = "{\n"
        for i_key, i_value in special_words.items():
            new_dictionary += '"{}": "{}",\n'.format(i_key, i_value)
        new_dictionary += '}'
        print('\n' * 10)

        file_opener = open("Резервный файл.txt", 'w', encoding="windows-1251")
        file_opener.write(new_dictionary)
        file_opener.close()
        print("\n" * 2)

    else:
        file_opener = open('statistics.txt', 'r', encoding="windows-1251")
        text = file_opener.read()
        stat_res = text
        text = file_opener.close()

        file_opener = open('counter.txt', 'r', encoding="windows-1251")
        text = file_opener.read()
        count = text
        text = file_opener.close()

        print()
        print("Статистика за последние {} использований:".format(count))
        print(stat_res)

        answer = input("Хотите очистить статистику (1 - да, enter - нет)? ")
        if answer == '1':

            file_opener = open('statistics.txt', 'w', encoding="windows-1251")
            file_opener.write('')
            file_opener.close()

            file_opener = open('errors.txt', 'w', encoding="windows-1251")
            file_opener.write('{}')
            file_opener.close()

            file_opener = open('counter.txt', 'w', encoding="windows-1251")
            file_opener.write('0')
            file_opener.close()

        return

    main_choice(words, special_words)


def standard_test(keys, dictionary):
    errors = []

    for count, word in enumerate(keys):
        print('\n'"Слово НОМЕР {0}, ОСТАЛОСЬ {1}".format(count + 1, len(keys) - count - 1))
        answer = input("{} -- ".format(word))
        count += 1

        if answer != dictionary[word]:
            errors.append((dictionary[word], word, answer))

    errors_analysis(errors)


def errors_analysis(all_errors):
    true_errors = []
    print("\n" * 100)
    for i_error in all_errors:
        print("{} -- {} !- {}".format(i_error[0], i_error[1], i_error[2]), end=' ')
        control_result = input("Действительная ошибка? (пробел - да, enter - нет): ")

        if control_result == ' ':
            true_errors.append(i_error[0])

    errors_stats(true_errors)


def errors_stats(info):
    file_opener = open("errors.txt", 'r', encoding="windows-1251")
    dictionary = file_opener.read()
    text = eval(dictionary)
    dictionary = file_opener.close()

    for i_word in info:
        if i_word in text:
            text[i_word] += 1
        else:
            text[i_word] = 1

    file_opener = open("errors.txt", 'w', encoding="windows-1251")
    file_opener.write(str(text))
    file_opener.close()

    stats(text)


def stats(info, count=1):
    error_counter = 0
    statistic = ''

    for i_count in info.values():
        error_counter += i_count

    unprepared_stats = [[i_word, round(i_count / error_counter * 100, 2)] for i_word, i_count in info.items()]
    unprepared_stats.sort()

    for i_stat in unprepared_stats:
        statistic += '"{}" - {}%\n'.format(i_stat[0], i_stat[1])

    file_opener = open('statistics.txt', 'w', encoding="windows-1251")
    file_opener.write(statistic)
    file_opener.close()

    file_opener = open("counter.txt", 'r', encoding="windows-1251")
    text = file_opener.read()
    previous_count = int(text)
    text = file_opener.close()

    file_opener = open('counter.txt', 'w', encoding="windows-1251")
    file_opener.write(str(previous_count + count))
    file_opener.close()


file_opener = open("dict.txt", 'r', encoding="windows-1251")
dictionary = eval(file_opener.read())
file_opener.close()

file_opener = open("Резервный файл.txt", 'r', encoding="windows-1251")
special_dictionary = eval(file_opener.read())
file_opener.close()

main_choice(dictionary, special_dictionary)
