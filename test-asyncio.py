import asyncio
import random

# Константы, минимальное и максимальное число
NUMBER_MIN = 1
NUMBER_MAX = 1_000_000


async def coroutine_1(queue_2, queue_3, queue_4):
    """
    Корутина 1 cо случайной периодичностью от 1 до 10 сек.
    генерирует случайное число от NUMBER_MIN до NUMBER_MAX.
    Посылает в 3 очреди сгенерированное число.
    """
    while True:
        await asyncio.sleep(random.randint(1, 10))
        number = random.randint(NUMBER_MIN, NUMBER_MAX)
        # print(f'Coroutine_1 {number} Put')
        queue_2.put_nowait(number)
        queue_3.put_nowait(number)
        queue_4.put_nowait(number)


async def coroutine_2(queue):
    """
    Получает из очереди-2 число.
    Вычисляет максимальное число, если максимальное число изменилось,
    выводит его на консоль.
    """
    max_number = NUMBER_MIN
    while True:
        number = await queue.get()
        if number > max_number:
            max_number = number
            print(f'Maximum = {max_number}')


async def coroutine_3(queue):
    """
    Получает из очереди-3 число.
    Вычисляет минимальное число, если минимальное число изменилось,
    выводит его на консоль.
    """
    min_number = NUMBER_MAX
    while True:
        number = await queue.get()
        if number < min_number:
            min_number = number
            print(f'Minimum = {min_number}')


async def coroutine_4(queue):
    """
    Получает из очереди-4 число.
    Вычисляет среднее число, если среднее число изменилось,
    выводит его на консоль.
    """
    average_number = 0
    sum_number = 0
    n = 0
    while True:
        number = await queue.get()
        sum_number += number
        n += 1
        if average_number != sum_number/n:
            average_number = sum_number/n
            print(f'Average = {average_number}')


# Создаются три очереди
queue_2 = asyncio.Queue()
queue_3 = asyncio.Queue()
queue_4 = asyncio.Queue()

loop = asyncio.get_event_loop()
tasks = [
    loop.create_task(coroutine_1(queue_2, queue_3, queue_4)),
    loop.create_task(coroutine_2(queue_2)),
    loop.create_task(coroutine_3(queue_3)),
    loop.create_task(coroutine_4(queue_4))
]
loop.run_forever()
