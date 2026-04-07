from src.plugins.game.identities.townsfolks.Washerwoman import *
from src.plugins.game.identities.townsfolks.Librarian import *
from src.plugins.game.identities.townsfolks.Investigator import *
from src.plugins.game.identities.townsfolks.Oracle import *
from src.plugins.game.identities.townsfolks.ClockMaker import *
from src.plugins.game.identities.townsfolks.FortuneTeller import *
from src.plugins.game.identities.townsfolks.Noble import *
from src.plugins.game.identities.townsfolks.Seamstress import *
from src.plugins.game.identities.townsfolks.Ravenkeeper import *
from src.plugins.game.identities.townsfolks.Chef import *
from src.plugins.game.identities.townsfolks.Philosopher import *
from src.plugins.game.identities.townsfolks.Dreamer import *
from src.plugins.game.identities.townsfolks.Undertaker import *
from src.plugins.game.identities.townsfolks.Artist import *
from src.plugins.game.identities.townsfolks.Empath import *
from src.plugins.game.identities.townsfolks.LionDancer import *
from src.plugins.game.identities.townsfolks.Stargazer import *
from src.plugins.game.identities.townsfolks.Steward import *
from src.plugins.game.identities.townsfolks.Blacksmith import *
from src.plugins.game.identities.townsfolks.Grandmother import *

from src.plugins.game.identities.outsiders.Sweetheart import *
from src.plugins.game.identities.outsiders.Drunk import *
from src.plugins.game.identities.outsiders.Recluse import *
from src.plugins.game.identities.outsiders.Tinker import *
from src.plugins.game.identities.outsiders.Bartender import *
from src.plugins.game.identities.outsiders.Cute import *

from src.plugins.game.identities.minions.Poisoner import *
from src.plugins.game.identities.minions.Godfather import *
from src.plugins.game.identities.minions.Assassin import *
from src.plugins.game.identities.minions.Widow import *
from src.plugins.game.identities.minions.Spy import *
from src.plugins.game.identities.minions.EvilTwin import *

from src.plugins.game.identities.demons.Imp import *
from src.plugins.game.identities.demons.NoDashii import *
from src.plugins.game.identities.demons.FangGu import *
from src.plugins.game.identities.demons.Leviathan import *
from src.plugins.game.identities.demons.Warden import *
from src.plugins.game.identities.demons.TaoWu import *
from src.plugins.game.identities.demons.Po import *

from src.plugins.game.identities.townsfolks._Nobody import *

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
