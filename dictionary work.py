with open('Резервный файл.txt', 'r', encoding="windows-1251") as file_reader:
    dictionary = eval(file_reader.read())

with open('Резервный файл.txt', 'w', encoding="windows-1251") as file_adder:
    list_values = [input("Английское слово ({}): ".format(i_count + 1)) for i_count in range(15)]
    print("\n" * 10)
    list_keys = [input("Перевод {}: ".format(key)) for key in list_values]

    dict_add = dict(zip(list_keys, list_values))
    dict_add.update(dictionary)

    new_dictionary = "{\n"
    for i_key, i_value in dict_add.items():
        new_dictionary += '"{}": "{}",\n'.format(i_key, i_value)
    new_dictionary += '}'
    print('\n' * 10)

    file_adder.write(new_dictionary)
