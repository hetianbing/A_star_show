import pygame
import sys
from pygame.sprite import Group


import gamefunction as gf
from setting import Setting
from node_data import Node_Data

from time import sleep
from time import time

from Button import AS_BUTTON

def main():
    pygame.init()

    # 设置
    as_setting = Setting(pygame.display.Info().current_w, pygame.display.Info().current_h)
    print('-------------------- setting --------------------')
    as_setting.show_settings()
    print('-------------------------------------------------')

    #显示屏幕
    screen = pygame.display.set_mode((as_setting.windows_width, as_setting.windows_high))
    pygame.display.set_caption("A_star")

    # 节点数据
    node_arr = Node_Data(as_setting, screen)

    #按钮列表
    button_list = [AS_BUTTON(as_setting, screen, msg) for msg in ["SET_START", "SET_END", "SET_BLOCK", "SET_BLANK"]]

    step_run = AS_BUTTON(as_setting, screen, "RUN")
    auto_run = AS_BUTTON(as_setting, screen, "AUTO")
    clear_all = AS_BUTTON(as_setting, screen, "CLEAR")
    change_type= AS_BUTTON(as_setting, screen, "STRAIGHT") # slanted


    while True:

        # node_arr.draw_nodes()
        #更新结果
        gf.update_screen(as_setting, screen, node_arr, button_list, step_run, auto_run, clear_all, change_type)

        #响应行为
        while not gf.check_event(as_setting, screen, node_arr, button_list, step_run, auto_run, clear_all, change_type):
            if as_setting.is_auto_run and not node_arr.is_find_way and time() >= as_setting.last_time + as_setting.delay_time:
                node_arr.run_once()
                as_setting.last_time = time()
                break
            sleep(0.005)





main()