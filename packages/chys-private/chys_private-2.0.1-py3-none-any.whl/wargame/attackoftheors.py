import random

from gameutils import *
from hut import Hut
from knight import Knight
from orcider import OrcRider


# 改写为 abstractClass


class AttackofTheOrcs:
    def __init__(self):
        self.huts = []
        self.player = None
        self.is_acquired_list = ['未知'] * 5

    @staticmethod
    def show_game_mission():
        print("阴阳二神互相杀伐，世界处于永劫之中。玩家需扮演一名英雄，在地图中收集各种资源，与其他玩家对抗，生存到最后。")

    def create_occupy_huts(self):
        # friend = Knight()
        # enemy = OrcRider()
        choice_list = ['友军', '敌军', None]
        for i in range(5):
            computer_choice = random.choice(choice_list)
            if computer_choice == '敌军':
                self.huts.append(Hut(i + 1, OrcRider()))
            elif computer_choice == '友军':

                self.huts.append(Hut(i + 1, Knight()))
            else:
                self.huts.append(Hut(i + 1, computer_choice))
            # print(self.huts[i])

    def check_occupant_all_acquired_enemy_death(self):
        a = 0
        e = 0
        z = 0
        for i in range(len(self.huts)):
            if self.huts[i].is_acquired:
                a += 1
                if self.huts[i].occupant is not None:
                    if self.huts[i].occupant.unit_type == '敌军':
                        e += 1
                        if self.huts[i].occupant.health_meter == 0:
                            print(self.huts[i].occupant.health_meter)
                            z += 1

        if a + z > len(self.huts) + e - 1:
            return True
        else:
            return False

    @staticmethod
    def user_choice():
        while True:
            try:
                idx = int(input('\n选择你前往的点...1~5 ') or 2)

            except ValueError:
                print('请输入数字')
                continue
            else:
                return idx

    #     raise AssertionError('随手报错')

    def enter_huts(self):

        all_is_acquired = self.check_occupant_all_acquired_enemy_death()

        self.is_acquired_list = ['未知'] * 5
        # print(self.is_acquired_list)

        while all_is_acquired is False:
            print(self.is_acquired_list)
            idx = self.user_choice()
            try:
                self.huts[idx - 1].is_acquired
            except IndexError:
                print('你输入的值太大了')
                continue

            else:

                if self.huts[idx - 1].is_acquired:

                    print('我来过这个地方')
                    if self.huts[idx - 1].occupant is not None and self.huts[idx - 1].occupant.unit_type == '敌军':
                        if self.huts[idx - 1].occupant.health_meter > 0:
                            self.player.attack(self.huts[idx - 1].occupant)
                elif self.huts[idx - 1].occupant is None:
                    print('此处空无一物！')
                    self.huts[idx - 1].is_acquired = True
                    self.is_acquired_list[idx - 1] = '空'
                else:
                    # idx = self.user_choice()
                    # print(self.huts[idx-1].occupant.name)
                    if self.huts[idx - 1].occupant.unit_type == '敌军':
                        print('是敌人')
                        # (self.huts[idx-1].__dict__.items())
                        self.player.attack(self.huts[idx - 1].occupant)
                        self.is_acquired_list[
                            idx - 1] = f"{self.huts[idx - 1].occupant.name}:{self.huts[idx - 1].occupant.health_meter}"
                        # self.is_acquired_list[idx - 1] = self.huts[idx - 1].occupant.name
                        self.huts[idx - 1].is_acquired = True
                        # all_is_acquired = self.check_occupant_is_acquired()
                    if self.player.health_meter <= 0:
                        print('没血了，重开！')
                        break
                    # self.huts[idx - 1].is_acquired = True

                    elif self.huts[idx - 1].occupant.unit_type == '友军':

                        print('是友军')
                        self.player.heal()

                        self.huts[idx - 1].is_acquired = True
                        self.is_acquired_list[idx - 1] = self.huts[idx - 1].occupant.name
                all_is_acquired = self.check_occupant_all_acquired_enemy_death()
                if self.player.health_meter <= 0:
                    print('没血了，重开！')
                    break
            finally:
                pass
                # print('finally')
        print(self.is_acquired_list)
        if all_is_acquired is True:
            self.player.show_health()
            print_bold('战斗结束,不朽面具！')
        # return idx

    # def

    def play(self):
        self.player = Knight()
        self.show_game_mission()
        self.create_occupy_huts()
        self.enter_huts()
        # self.
        # print(self.huts)
    # def OrcRider(self):
    #     pass


if __name__ == '__main__':
    game = AttackofTheOrcs()
    game.play()
