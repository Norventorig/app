import random


def main_choice(words, special_words):
    print()
    print('Остановить программу (0)')
    print('60 слов (1)')
    print('Вперемешку 60 слов (2)')
    print('Введение новых слов (3)')

    variant = input('Выбор:')
    print('\n'*2)

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

        file_opener = open("dict.txt", 'w', encoding="windows-1251")
        file_opener.write(new_dictionary)
        file_opener.close()

        new_dictionary = "{\n"
        for i_key, i_value in special_words.items():
            new_dictionary += '"{}": "{}",\n'.format(i_key, i_value)
        new_dictionary += '}'

        file_opener = open("Резервный файл.txt", 'w', encoding="windows-1251")
        file_opener.write(new_dictionary)
        file_opener.close()

    else:
        with open('counter.txt', 'r', encoding='windows-1251') as counter_reader:
            count = counter_reader.read()

        with open('statistics.txt', 'r', encoding="windows-1251") as statistic_reader:
            stat_res = eval(statistic_reader.read())

        print("Статистика за последние {} использований:\n".format(count))

        for i_key, i_value in stat_res.items():
            print("{word} - ({stat})".format(word=i_key, stat_res=i_value))

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

    if not errors:
        print('\n', ' ' * 81, 'Нет ошибок:', ' ' * 81, '\n')

    else:
        print('\n', ' '*83, 'ОШИБКИ:', ' '*83, '\n')
        for i_error in errors:
            print("{} == {} !=! {}".format(i_error[1], i_error[0], i_error[2]))

    with open('counter.txt', 'r', encoding='UTF-8') as counter_reader:
        count = int(counter_reader.read())
        count += 1

    with open('counter.txt', 'w', encoding='UTF-8') as counter_adder:
        counter_adder.write(str(count))

    errors_stats(errors)

    if count == 11:
        errors_work(dictionary)


def errors_work(dictionary):
    with open("errors.txt", 'r', encoding='UTF-8') as errors_reader:
        errors_values = (eval(errors_reader.read())).keys()
        errors_keys = []

    for i_key, i_value in dictionary.items():

        if i_value in errors_values:
            errors_keys.append(i_key)

    with open('statistics.txt', 'w', encoding="UTF-8") as statistic_reset:
        statistic_reset.write('')

    with open('errors.txt', 'w', encoding="UTF-8") as errors_reset:
        errors_reset.write('{}')

    with open('counter.txt', 'w', encoding="UTF-8") as counter_reset:
        counter_reset.write("0")

    standard_test(errors_keys, dictionary)


def errors_stats(errors_list):
    with open('errors.txt', 'r', encoding='UTF-8') as errors_reader:
        dict_errors = eval(errors_reader.read())

    for i in errors_list:

        if i[0] in dict_errors.keys():
            dict_errors[i[0]] += 1

        else:
            dict_errors[i[0]] = 1

    stats(dict_errors)


def stats(errors_amount):
    errors_counter = 0
    statistic = {}

    for i_amount in errors_amount.values():
        errors_counter += i_amount

    for i_error, i_amount in errors_amount.items():
        statistic[i_error] = '{}%'.format(round((i_amount / errors_counter) * 100, 1))

    with open("statistics.txt", 'w', encoding="UTF-8") as statistic_writer:
        statistic_writer.write(str(statistic))

    with open('errors.txt', 'w', encoding="UTF-8") as errors_writer:
        errors_writer.write(str(errors_amount))


with open("dict.txt", 'r', encoding="windows-1251") as file_reader:
    main_dictionary = eval(file_reader.read())

with open("Резервный файл.txt", 'r', encoding="windows-1251") as file_reader:
    special_dictionary = eval(file_reader.read())

main_choice(main_dictionary, special_dictionary)
