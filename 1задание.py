#Задание 1
#Напишите функцию, которая принимает текст лога (несколько строк) и возвращает количество записей ERROR, WARN и INFO и время первой и последней учтённой записи.
#Формат строки: ГГГГ-ММ-ДД ЧЧ:ММ:СС УРОВЕНЬ сообщение.
#Правила: учитываем только ERROR, WARN и INFO заглавными; строки с другими уровнями и без корректной даты/времени (2026-02-30, 25:61:00) пропускаем, функция не падает; пустой лог — нули и нет времени.
#Пример лога: «2026-10-13 14:23:05 INFO Service started» / «not a log line» / «2026-10-13 14:23:15 ERROR Connection refused» / «2026-10-13 14:23:20 WARN Retry attempt 1» / «2026-10-13 25:61:00 ERROR Bad time» / «2026-10-13 14:23:30 ERROR Giving up»
#Результат: ERROR: 2, WARN: 1, INFO: 1, первая: 2026-10-13 14:23:05, последняя: 2026-10-13 14:23:30
def analyze_logs(log_text):
    # Счетчики для каждого уровня
    error_count = 0
    warn_count = 0
    info_count = 0

    # Временные метки первой и последней записи
    first_time = None
    last_time = None

    # Разбиваем текст на строки
    lines = log_text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:  # Пустая строка
            continue

        # Разделяем строку на части (должно быть минимум 3 части: дата, время, уровень)
        parts = line.split()
        if len(parts) < 3:
            continue

        # Берем первые три части
        date_str = parts[0]  # ГГГГ-ММ-ДД
        time_str = parts[1]  # ЧЧ:ММ:СС
        level = parts[2]  # УРОВЕНЬ

        # Проверяем уровень (только ERROR, WARN, INFO)
        if level not in ['ERROR', 'WARN', 'INFO']:
            continue

        # Проверяем формат даты и времени
        try:
            # Проверяем дату (ГГГГ-ММ-ДД)
            date_parts = date_str.split('-')
            if len(date_parts) != 3:
                continue
            year, month, day = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])

            # Простая проверка месяца и дня
            if month < 1 or month > 12:
                continue
            if day < 1 or day > 31:
                continue

            # Проверяем время (ЧЧ:ММ:СС)
            time_parts = time_str.split(':')
            if len(time_parts) != 3:
                continue
            hour, minute, second = int(time_parts[0]), int(time_parts[1]), int(time_parts[2])

            # Проверка часов, минут, секунд
            if hour < 0 or hour > 23:
                continue
            if minute < 0 or minute > 59:
                continue
            if second < 0 or second > 59:
                continue

        except ValueError:
            # Если не удалось преобразовать в числа - пропускаем
            continue

        # Если дошли сюда - строка валидна
        full_time = f"{date_str} {time_str}"

        # Обновляем счетчики
        if level == 'ERROR':
            error_count += 1
        elif level == 'WARN':
            warn_count += 1
        elif level == 'INFO':
            info_count += 1

        # Обновляем первую и последнюю запись
        if first_time is None:
            first_time = full_time
        last_time = full_time

    # Формируем результат
    result = f"ERROR: {error_count}, WARN: {warn_count}, INFO: {info_count}"
    if first_time:
        result += f", первая: {first_time}, последняя: {last_time}"
    else:
        result += ", первая: нет, последняя: нет"

    return result


# Пример использования
log = """2026-10-13 14:23:05 INFO Service started
not a log line
2026-10-13 14:23:15 ERROR Connection refused
2026-10-13 14:23:20 WARN Retry attempt 1
2026-10-13 25:61:00 ERROR Bad time
2026-10-13 14:23:30 ERROR Giving up"""

print(analyze_logs(log))
# Вывод: ERROR: 2, WARN: 1, INFO: 1, первая: 2026-10-13 14:23:05, последняя: 2026-10-13 14:23:30

