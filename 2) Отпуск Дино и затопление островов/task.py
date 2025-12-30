from collections import deque

def main():
    with open("input.txt", 'r') as input_file, open("output.txt", 'w') as output_file: # открываем файлы для чтения и записи
        lines = input_file.read().splitlines()
        # идея: добить в очередь потопа изначально затопленные клетки (и те, что стоят на границе поля) с временем их затопления ранвым их высоте, 
        # после чего брать по одной клетке из начала очереди и проверять её соседей на допустимость и на "внесение значимого изменения" в затопление (затопить ещё не рассмотренную клетку или улучшить её старый показатель времени затопления)
        # если соседняя клетка прошла проверки, то добавляем её в конец очереди потопа с соответствующим временем на затопление

        # берём значения из строк через split (получая list) и приводим их к типу int через map функции
        n, m = map(int, lines[0].split())
        height = []
        for i in range(1, n+1):
            height.append(list(map(int, lines[i].split())))

        # формируем точки начала затопления
        time_to_flood = [[-1] * m for i in range(n)] # финальная таблица времени затопления клеток
        flood_source = deque() # очередь итерации по клеткам
        for i in range(n):
            for j in range(m):
                if height[i][j] == 0: # если клетка изначально затоплена
                    time_to_flood[i][j] = 0 # время её затопления равно нулю
                    flood_source.append((i, j, 0)) # запоминаем позиции старта затопления (0 отвечает за шаг, на котором будет затоплена ячейка [i][j])

        # дополнительный точки старта потопа по краям поля (так как острова в море)
        for i in range(n): 
            time_to_flood[i][0] = height[i][0]
            flood_source.append((i, 0, height[i][0]))
        for i in range(n): 
            time_to_flood[i][m-1] = height[i][m-1]
            flood_source.append((i, m-1, height[i][m-1]))
        for j in range(1, m-1): 
            time_to_flood[0][j] = height[0][j]
            flood_source.append((0, j, height[0][j]))
        for j in range(1, m-1): 
            time_to_flood[n-1][j] = height[n-1][j]
            flood_source.append((n-1, j, height[n-1][j]))


        while flood_source: # BFS обход поля, пока есть нерассмотренные источники воды
            i, j, time = flood_source.popleft() # берём первое значение из очереди

            for moving in ((1, 0), (-1, 0), (0, 1), (0, -1)): # возможные пути затопления
                next_i, next_j = i + moving[0], j + moving[1] # смотрим соседнюю клетку

                if 0 <= next_i < n and 0 <= next_j < m: # проверка допустимости ячейки
                    time_to_flood_height = max(height[next_i][next_j], time) # время, за которое потоп накроет данную ячейку с учётом необходимого времени для её достижения водой (max на случай, когда низкая территория была окружена высокой)
                    
                    if time_to_flood[next_i][next_j] == -1: # если ещё не топили ячейку — сразу топим её и добавляем как новый источник потопа
                        time_to_flood[next_i][next_j] = time_to_flood_height
                        flood_source.append((next_i, next_j, time_to_flood_height))
                    elif time_to_flood_height < time_to_flood[next_i][next_j]: # если ячейка уже была ранее затоплена, но текущий путь воды до неё оптимальнее — обновляем время её затопления и снова добавляем как источник потопа
                        time_to_flood[next_i][next_j] = time_to_flood_height
                        flood_source.append((next_i, next_j, time_to_flood_height))

        # записываем строки в файл
        for row in time_to_flood:
            print(*row, file=output_file) 


if __name__ == '__main__': # запускаем выполнение при прямом вызове скрипта (игнорируем при импорте этого файла в другой модуль)
    main()