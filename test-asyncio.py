import asyncio
import random
import signal
import functools

# Константы, минимальное и максимальное число
NUMBER_MIN = 1
NUMBER_MAX = 1_000_000


async def coroutine_1(queues):
    """
    Корутина 1 cо случайной периодичностью от 1 до 10 сек.
    генерирует случайное число от NUMBER_MIN до NUMBER_MAX.
    Посылает в 3 очреди сгенерированное число.
    """
    while True:
        await asyncio.sleep(random.randint(1, 10))
        number = random.randint(NUMBER_MIN, NUMBER_MAX)
        # print(f'Coroutine_1 {number} Put')
        for queue in queues:
            queue.put_nowait(number)


async def coroutine_2(queue):
    """
    Получает из очереди число.
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
    Получает из очереди число.
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
    Получает из очереди число.
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


def ask_exit(signame, loop):
    """
    Останавливает корутины
    """
    print(f'Got signal {signame}: exit')
    loop.stop()


# Создаются три очереди
queues = []
for i in range(3):
    queue = asyncio.Queue()
    queues.append(queue)

loop = asyncio.get_event_loop()
loop.create_task(coroutine_1(queues))
loop.create_task(coroutine_2(queues[0]))
loop.create_task(coroutine_3(queues[1]))
loop.create_task(coroutine_4(queues[2]))

# Обработчик сигналов SIGINT, SIGTERM
for signame in {'SIGINT', 'SIGTERM'}:
    loop.add_signal_handler(
        getattr(signal, signame),
        functools.partial(ask_exit, signame, loop)
    )

loop.run_forever()
