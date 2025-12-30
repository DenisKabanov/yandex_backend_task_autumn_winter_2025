def main():
    with open("input.txt", 'r') as input_file, open("output.txt", 'w') as output_file: # открываем файлы для чтения и записи
        lines = input_file.read().splitlines() # берём весь текст из input_file и разбиваем на строки (splitlines по \n)

        # берём значения из строк через split (получая list) и приводим их к типу int через map функции
        n, m = map(int, lines[0].split())
        values = list(map(int, lines[1].split()))
        adj_list = {i: set() for i in range(0, n)} # список смежности (нумерация с 0, а не с 1)
        for row in lines[2:]: # идём по оставшимся строкам
            island_from, island_to = map(int, row.split())
            adj_list[island_from-1].add(island_to-1)
            adj_list[island_to-1].add(island_from-1)
        max_treasure = 0 # максимальное сокровище, что можно собрать


        def DFS(current_island: int, current_treasure: int, seen_island) -> None: # DFS обход островов
            """
            DFS обход всех возможных путей между островами с обновлением максимальной суммы сокровищ.
            Parameters:
                current_island (int) : Номер текущего острова.
                current_treasure (int) : Сумма сокровищ до текущего шага.
                seen_island (set) : set уже рассмотренных островов на ветке вычисления.
            Returns:
                None: Обновляет максимальную сумму сокровищ.
            """
            nonlocal max_treasure # обновляемая переменная с уровнем видимости выше функции
            current_treasure += values[current_island] # добавляем сокровище с текущего острова

            checked_islands = 0 # количество проверенных островов, чтобы обновление делать только тогда, когда мы никуда не продвинулись (зашли в тупик)
            for island in adj_list[current_island]: # идём по смежным островам
                if island not in seen_island: # если остров ещё не посещён
                    checked_islands += 1 # увеличиваем счётчик сделанных переходов
                    seen_island.add(island) # добавляем в set остров, на который переходим
                    DFS(island, current_treasure, seen_island) # рекурсивно вызываем DFS с нового острова
                    seen_island.remove(island) # удаляем остров из рассмотренных для корректного прохода по веткам

            if checked_islands == 0 and current_treasure > max_treasure: # если мы никуда не продвинулись и текущая сумма лучше максимальной, то обновляем достижимый максимум
                max_treasure = current_treasure


        DFS(current_island=0, current_treasure=0, seen_island=set([0])) # запускаем DFS с первого (нулевого острова)

        print(max_treasure, file=output_file) # делаем запись в файл


if __name__ == '__main__': # запускаем выполнение при прямом вызове скрипта (игнорируем при импорте этого файла в другой модуль)
    main()