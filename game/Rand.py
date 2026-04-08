import random
from nonebot.log import logger




def rand(a):

    if a <= 0:
        logger.info("Wrond rand -> a = " + str(a))
        return

    rnd = random.Random()
    ret = rnd.randint(1, a)

    return ret


def rand100(a, b=100):
    if a <= 0:
        logger.info('错误的rand值 -> a =' + str(a))
        return 0

    if b <= 0 or b >= 10000000:
        logger.info('错误的rand值 -> b =' + str(b))
        return 0

    rnd = random.Random()
    num = rnd.randint(1, b)

    if num <= a:
        return True

    return False