from datetime import datetime, date, timedelta, timezone
# datetime — класс для работы с датой и временем (день, месяц, год, часы, минуты, секунды).
# date — только дата (без времени).
# timedelta — разница между датами или временем (например, +7 дней).
# timezone — позволяет работать с часовыми поясами.
x = datetime.datetime.now()
print(x)

import datetime
x = datetime.datetime.now()
print(x.year)
print(x.strftime("%A"))

# Первый datetime — модуль
# Второй datetime — класс внутри модуля
# 3️⃣ datetime.datetime.now() — это метод класса, который возвращает текущие дату и время.


now = datetime.now()
print(now)

# Formatting 
now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
print(now.strftime("%d.%m.%Y"))
# strftime — превращает дату в строку в нужном формате.
# %Y — год (4 цифры)
# %m — месяц (01–12)
# %d — день (01–31)
# %H — часы (00–23)
# %M — минуты
# %S — секунды

import datetime
x = datetime.datetime(2018, 6, 1)
print(x.strftime("%B"))
# strftime превращает дату в строку по заданному формату.
# %B — полное название месяца на английском.

# Time difference 
start = datetime(2026, 2, 1, 12, 0, 0) 
end = datetime(2026, 2, 16, 10, 0, 0) 
diff = end - start 
print(diff.days, diff.total_seconds())

# timedelta
print(now + timedelta(days=7))


# Timezones (UTC and UTC+5 like Almaty offset)
utc_now = datetime.now(timezone.utc) 
almaty_tz = timezone(timedelta(hours=5)) 
almaty_now = utc_now.astimezone(almaty_tz) 
print("UTC:", utc_now) 
print("Almaty:", almaty_now)
# timezone.utc — это всемирное координированное время (UTC+0).
# timedelta(hours=5) — создаём часовой пояс UTC+5 (например, Алматы).
# utc_now.astimezone(almaty_tz) — переводим время из UTC в Алматы.