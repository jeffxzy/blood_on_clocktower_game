from .townsfolks.Washerwoman import *
from .townsfolks.Librarian import *
from .townsfolks.Investigator import *
from .townsfolks.Oracle import *
from .townsfolks.ClockMaker import *
from .townsfolks.FortuneTeller import *
from .townsfolks.Noble import *
from .townsfolks.Seamstress import *
from .townsfolks.Ravenkeeper import *
from .townsfolks.Chef import *
from .townsfolks.Philosopher import *
from .townsfolks.Dreamer import *
from .townsfolks.Undertaker import *
from .townsfolks.Artist import *
from .townsfolks.Empath import *
from .townsfolks.LionDancer import *
from .townsfolks.Stargazer import *
from .townsfolks.Steward import *
from .townsfolks.Blacksmith import *
from .townsfolks.Grandmother import *

from .outsiders.Sweetheart import *
from .outsiders.Drunk import *
from .outsiders.Recluse import *
from .outsiders.Tinker import *
from .outsiders.Bartender import *
from .outsiders.Cute import *

from .minions.Poisoner import *
from .minions.Godfather import *
from .minions.Assassin import *
from .minions.Widow import *
from .minions.Spy import *
from .minions.EvilTwin import *

from .demons.Imp import *
from .demons.NoDashii import *
from .demons.FangGu import *
from .demons.Leviathan import *
from .demons.Warden import *
from .demons.TaoWu import *
from .demons.Po import *

from .townsfolks._Nobody import *

import copy


def importAll(gameName):
    ret = {'townsfolk': [], 'outsider': [], 'minion': [], 'demon': [], 'nobody': []}
    if gameName == '实验1':
        ret['townsfolk'].append(Investigator())
        ret['townsfolk'].append(Librarian())
        ret['townsfolk'].append(Chef())
        ret['townsfolk'].append(ClockMaker())
        ret['townsfolk'].append(Oracle())
        ret['townsfolk'].append(FortuneTeller())
        ret['townsfolk'].append(Noble())
        ret['townsfolk'].append(Seamstress())
        ret['townsfolk'].append(Ravenkeeper())
        ret['townsfolk'].append(Philosopher())

        ret['outsider'].append(Sweetheart())
        ret['outsider'].append(Drunk())

        ret['minion'].append(Poisoner())
        ret['minion'].append(Godfather())

        ret['demon'].append(Imp())

    if gameName == '标准1':
        ret['townsfolk'].append(Investigator())
        ret['townsfolk'].append(Chef())
        ret['townsfolk'].append(ClockMaker())
        ret['townsfolk'].append(Oracle())
        ret['townsfolk'].append(FortuneTeller())
        ret['townsfolk'].append(Noble())
        ret['townsfolk'].append(Seamstress())
        ret['townsfolk'].append(Washerwoman())
        ret['townsfolk'].append(Philosopher())
        ret['townsfolk'].append(Dreamer())
        ret['townsfolk'].append(Undertaker())
        ret['townsfolk'].append(Artist())
        ret['townsfolk'].append(Empath())
        ret['townsfolk'].append(Blacksmith())
        ret['townsfolk'].append(Grandmother())

        ret['outsider'].append(Sweetheart())
        ret['outsider'].append(Drunk())
        ret['outsider'].append(Recluse())
        ret['outsider'].append(Tinker())

        # ret['minion'].append(Poisoner())
        ret['minion'].append(Godfather())
        ret['minion'].append(Assassin())
        ret['minion'].append(Widow())
        ret['minion'].append(Spy())

        ret['demon'].append(NoDashii())
        ret['demon'].append(FangGu())
        ret['demon'].append(Imp())
        ret['demon'].append(Leviathan())

    if gameName == '利维坦1':
        ret['townsfolk'].append(Investigator())
        ret['townsfolk'].append(ClockMaker())
        ret['townsfolk'].append(Philosopher())
        ret['townsfolk'].append(Dreamer())
        ret['townsfolk'].append(Undertaker())
        ret['townsfolk'].append(FortuneTeller())

        ret['outsider'].append(Drunk())
        ret['outsider'].append(Sweetheart())

        ret['minion'].append(Widow())
        ret['minion'].append(Godfather())

        ret['demon'].append(Leviathan())

    if gameName == '华灯1':
        ret['townsfolk'].append(Stargazer())
        ret['townsfolk'].append(LionDancer())
        ret['townsfolk'].append(Investigator())
        ret['townsfolk'].append(ClockMaker())
        ret['townsfolk'].append(Dreamer())
        ret['townsfolk'].append(Seamstress())
        ret['townsfolk'].append(Oracle())
        ret['townsfolk'].append(Philosopher())
        ret['townsfolk'].append(Empath())
        ret['townsfolk'].append(FortuneTeller())
        ret['townsfolk'].append(Grandmother())

        ret['outsider'].append(Drunk())
        ret['outsider'].append(Sweetheart())
        ret['outsider'].append(Bartender())

        ret['minion'].append(Widow())
        ret['minion'].append(Godfather())
        ret['minion'].append(Assassin())

        ret['demon'].append(Warden())
        ret['demon'].append(TaoWu())
        ret['demon'].append(FangGu())

    if gameName == '华灯2':
        ret['townsfolk'].append(Stargazer())
        ret['townsfolk'].append(LionDancer())
        ret['townsfolk'].append(Chef())
        ret['townsfolk'].append(ClockMaker())
        ret['townsfolk'].append(Dreamer())
        ret['townsfolk'].append(Seamstress())
        ret['townsfolk'].append(Oracle())
        ret['townsfolk'].append(Philosopher())
        ret['townsfolk'].append(Empath())
        ret['townsfolk'].append(FortuneTeller())
        ret['townsfolk'].append(Artist())
        ret['townsfolk'].append(Noble())
        ret['townsfolk'].append(Librarian())
        ret['townsfolk'].append(Grandmother())

        ret['outsider'].append(Drunk())
        ret['outsider'].append(Sweetheart())
        ret['outsider'].append(Bartender())
        ret['outsider'].append(Tinker())

        ret['minion'].append(Widow())
        ret['minion'].append(Godfather())
        ret['minion'].append(Assassin())
        ret['minion'].append(EvilTwin())

        ret['demon'].append(Warden())
        ret['demon'].append(TaoWu())
        ret['demon'].append(NoDashii())
        ret['demon'].append(Po())

    if gameName == '投毒1':
        ret['townsfolk'].append(Stargazer())
        ret['townsfolk'].append(ClockMaker())
        ret['townsfolk'].append(Dreamer())
        ret['townsfolk'].append(Seamstress())
        ret['townsfolk'].append(Oracle())
        ret['townsfolk'].append(Philosopher())
        ret['townsfolk'].append(FortuneTeller())
        ret['townsfolk'].append(Investigator())
        ret['townsfolk'].append(Librarian())
        ret['townsfolk'].append(Noble())
        ret['townsfolk'].append(Empath())
        ret['townsfolk'].append(Grandmother())

        ret['outsider'].append(Drunk())

        ret['minion'].append(Poisoner())

        ret['demon'].append(Imp())

    random.shuffle(ret['townsfolk'])
    random.shuffle(ret['outsider'])
    random.shuffle(ret['minion'])
    random.shuffle(ret['demon'])

    ret['nobody'].append(Nobody())

    if len(ret) == 0:
        logger.info('错误：ImportIdentities.py -> importAll -> 没有返回任何身份，板子 = ' + gameName)
        return ret

    return ret


def importExpect(expect):
    ret = {'townsfolk': [], 'outsider': [], 'minion': [], 'demon': [], 'nobody': []}

    t = {
        101: Washerwoman(),
        102: Librarian(),
        103: Investigator(),
        104: Oracle(),
        105: ClockMaker(),
        106: FortuneTeller(),
        107: Noble(),
        108: Seamstress(),
        109: Ravenkeeper(),
        110: Chef(),
        111: Philosopher(),
        112: Dreamer(),
        113: Undertaker(),
        114: Artist(),
        115: Empath(),
        116: LionDancer(),
        117: Stargazer(),
        118: Steward(),
        119: Blacksmith(),
        120: Grandmother(),
    }
    o = {
        201: Sweetheart(),
        202: Drunk(),
        203: Recluse(),
        204: Tinker(),
        205: Bartender(),
    }

    m = {
        301: Poisoner(),
        302: Godfather(),
        303: Assassin(),
        304: Widow(),
        305: Spy(),
        306: EvilTwin(),
    }

    d = {
        401: Imp(),
        402: NoDashii(),
        403: FangGu(),
        404: Leviathan(),
        405: Warden(),
        406: TaoWu(),
        407: Po(),
    }

    for i in expect:
        if 100 <= i < 200:
            ret['townsfolk'].append(copy.deepcopy(t[i]))
        if 200 <= i < 300:
            ret['outsider'].append(copy.deepcopy(o[i]))
        if 300 <= i < 400:
            ret['minion'].append(copy.deepcopy(m[i]))
        if 400 <= i < 500:
            ret['demon'].append(copy.deepcopy(d[i]))

    random.shuffle(ret['townsfolk'])
    random.shuffle(ret['outsider'])
    random.shuffle(ret['minion'])
    random.shuffle(ret['demon'])
    ret['nobody'].append(Nobody())
    return ret
