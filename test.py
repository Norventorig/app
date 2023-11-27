import random


def input_preparation(chief_dict):
    correct_answers = {}
    true_values = [x for x in chief_dict.keys()][-1:-61:-1]
    false_values = [x for x in chief_dict.keys()][-61:-241:-1]
    random.shuffle(false_values)
    user_keys = [chief_dict[x] for x in true_values]

    for key, value in chief_dict.items():
        correct_answers[value] = key

    return correct_answers, true_values, false_values, user_keys


def blocks_creation(true_values, false_values, user_keys):
    mini_blocks = []
    blocks = {}

    for i_index in range(60):
        mini_blocks.append(
            [true_values[i_index], false_values[i_index], false_values[i_index + 1], false_values[i_index + 2]])
        random.shuffle(mini_blocks[i_index])
        mini_blocks[i_index].insert(0, user_keys[i_index])
    random.shuffle(mini_blocks)

    for i_list in mini_blocks:
        blocks[i_list[0]] = (i_list[1], i_list[2], i_list[3], i_list[4])

    return blocks


def new_test(blocks, chief_dict, correct_answers):
    errors = []
    count = 0
    for key, value in blocks.items():
        count += 1
        print("\t" * 14, key, "СЛОВО НОМЕР {}".format(count))
        print("1){0}".format(value[0]))
        print("2){0}".format(value[1]))
        print("3){0}".format(value[2]))
        print("4){0}".format(value[3]))
        answer = input("Вариант: ")
        print("\n" * 2)

        if answer != '1' or answer != '2' or answer != '3' or answer != '4':
            errors.append((key, correct_answers[key], ''))

        elif chief_dict[value[int(answer) - 1]] != key:
            errors.append((key, correct_answers[key], value[int(answer) - 1]))

    print("\n" * 100)
    print("+{:-^60}+{:-^60}+{:-^60}+".format('-', '-', '-'))
    print("|{: ^60}|{: ^60}|{: ^60}|".format("Слово", "Перевод", 'Ошибка'))
    print("+{:-^60}+{:-^60}+{:-^60}+".format('-', '-', '-'))
    for i_error in errors:
        print("|{: ^60}|{: ^60}|{: ^60}|".format(i_error[0], i_error[1], i_error[2]))
    print("+{:-^60}+{:-^60}+{:-^60}+".format('-', '-', '-'))


def standard_test(keys, dictionary):
    errors = []

    for count, word in enumerate(keys):
        print('\n'"Слово НОМЕР {0}, ОСТАЛОСЬ {1}".format(count + 1, len(keys) - count - 1))
        answer = input("{} -- ".format(word))
        count += 1

        if answer != dictionary[word]:
            errors.append((word, dictionary[word], answer))

    print("\n" * 100)
    print("+{:-^60}+{:-^60}+{:-^60}+".format('-', '-', '-'))
    print("|{: ^60}|{: ^60}|{: ^60}|".format("Слово", "Перевод", 'Ошибка'))
    print("+{:-^60}+{:-^60}+{:-^60}+".format('-', '-', '-'))
    for i_error in errors:
        print("|{: ^60}|{: ^60}|{: ^60}|".format(i_error[0], i_error[1], i_error[2]))
    print("+{:-^60}+{:-^60}+{:-^60}+".format('-', '-', '-'))


file_opener = open("dict.txt", 'r', encoding="windows-1251")
dictionary = file_opener.read()
words = eval(dictionary)
dictionary = file_opener.close()

while True:
    print()
    print('Остановить программу (0)')
    print('120 слов (1)')
    print('Вперемешку 60 слов (2)')
    print('Режим наоборот(3)')
    print('Введение новых слов (4)')

    variant = int(input('Выбор:'))

    if variant == 1:
        list_keys = [x for x in words.keys()]
        list_keys = list_keys[-1:-61:-1] + list_keys[0:60:1]
        random.shuffle(list_keys)
        standard_test(list_keys, words)
        print("\n" * 2)

    elif variant == 2:
        list_keys = [x for x in words.keys()]
        list_keys = list_keys[-61:-181:-1]
        random.shuffle(list_keys)
        list_keys = list_keys[-1:-61:-1]
        standard_test(list_keys, words)
        print("\n" * 2)

    elif variant == 3:
        answers, tru_val, fal_val, keys = input_preparation(words)
        user_blocks = blocks_creation(tru_val, fal_val, keys)
        new_test(user_blocks, words, answers)
        print("\n" * 2)

    elif variant == 4:
        new_dictionary = "{\n"
        list_values = [input("Английское слово ({}): ".format(i_count + 1)) for i_count in range(15)]
        print("\n" * 10)
        list_keys = [input("Перевод {}: ".format(key)) for key in list_values]

        dict_add = dict(zip(list_keys, list_values))
        words.update(dict_add)

        for _ in range(15):
            words.pop(next(iter(words)))

        for i_key, i_value in words.items():
            new_dictionary += '"{}": "{}",\n'.format(i_key, i_value)
        new_dictionary += '}'
        print('\n' * 10)

        random.shuffle(list_keys)
        standard_test(list_keys, dict_add)

        file_opener = open("dict.txt", 'w', encoding="windows-1251")
        file_opener.write(new_dictionary)
        print("\n" * 2)

    else:
        break

# Добавить режим отслеживания и составления статистики ошибок.
# Добавить режим распознавания опечаток и настоящих ошибок.
