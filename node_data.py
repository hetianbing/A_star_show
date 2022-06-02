import pygame
from heapq import *
from random import randint

class One_Node():
    def __init__(self, row, col, cell_length, screen):
        self.row = row
        self.col = col

        self.gx = -1
        self.hx = -1
        self.fx = -1
        self.formal_node = [-1, -1]

        self.status = 'blank'

        self.cell_length = cell_length

        self.top = self.row * cell_length
        self.left = self.col * cell_length

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.bk_color = (180, 180, 180) #边框颜色 ： 灰
        self.rect_bk = pygame.Rect(0, 0, self.cell_length, self.cell_length)
        self.rect_bk.left = self.left
        self.rect_bk.top = self.top

        self.bg_color_blank = (255, 255, 255) # 格子颜色 ： 白
        self.bg_color_start = (210, 0, 0) # 格子颜色 ： 红色 - 开始
        self.bg_color_end = (176, 224, 230) # 格子颜色 ： 蓝色 - 结束
        self.bg_color_block = (0, 0, 0) # 格子颜色： 黑色 - 障碍
        self.rect_bg = pygame.Rect(0,0, self.cell_length - 4, self.cell_length - 4)
        self.rect_bg.center = self.rect_bk.center

        self.text_color = (255, 0, 0) #文字颜色 ： 红
        self.font = pygame.font.SysFont(None, 12)

        self.cell_type = 'blank'
        # self.cell_type = 'start'
        # self.cell_type = 'end'
        # self.cell_type = 'block'

        self.is_now_find = False
        self.is_finded = False
        self.is_in_final_way = False

    def draw_button(self):
        # 绘制一个用颜色填充的 边框bk， 再绘制格子中心 bg
        if self.is_now_find:
            bk_color = (255, 0, 0)  # 当前寻找的节点，红色框
            self.screen.fill(bk_color, self.rect_bk)
        else:
            self.screen.fill(self.bk_color, self.rect_bk)
        if self.cell_type == 'blank':
            bg_color = self.bg_color_blank
        elif self.cell_type == "start":
            bg_color = self.bg_color_start
        elif self.cell_type == "end":
            bg_color = self.bg_color_end
        elif self.cell_type == "block":
            bg_color = self.bg_color_block
        else:
            print("ERROR: self.cell_type = ", self.cell_type)
            bg_color = self.bg_color_blank

        if self.is_finded and self.cell_type != "start" and self.cell_type != "end":
            bg_color = (127, 255, 0)
            if self.is_in_final_way:
                bg_color = (0, 255, 255)
        self.screen.fill(bg_color, self.rect_bg)

        if self.fx != -1:
            # fx 的颜色
            text_color = (0, 0, 0)
            font = pygame.font.SysFont(None, self.cell_length // 2)
            msg_image = font.render(str(round(self.fx, 1)), True, text_color, bg_color)
            msg_image_rect = msg_image.get_rect()
            msg_image_rect.top = self.rect_bg.top
            msg_image_rect.centerx = self.rect_bg.centerx
            self.screen.blit(msg_image, msg_image_rect)
        if self.gx != -1:
            # gx 的颜色
            text_color = (30, 30, 30)
            font = pygame.font.SysFont(None, self.cell_length * 2 // 5)
            msg_image = font.render(str(round(self.gx, 1)), True, text_color, bg_color)
            msg_image_rect = msg_image.get_rect()
            msg_image_rect.bottom = self.rect_bg.bottom
            msg_image_rect.left = self.rect_bg.left
            self.screen.blit(msg_image, msg_image_rect)
        if self.hx != -1:
            # hx 的颜色
            text_color = (250, 153, 18)
            font = pygame.font.SysFont(None, self.cell_length * 2 // 5)
            msg_image = font.render(str(round(self.hx, 1)), True, text_color, bg_color)
            msg_image_rect = msg_image.get_rect()
            msg_image_rect.bottom = self.rect_bg.bottom
            msg_image_rect.right = self.rect_bg.right
            self.screen.blit(msg_image, msg_image_rect)

        if self.formal_node != [-1, -1]:
            show_str = str(self.formal_node)
            # formal 的颜色
            text_color = (0, 0, 18)
            font = pygame.font.SysFont(None, self.cell_length // 3)
            msg_image = font.render(show_str, True, text_color, bg_color)
            msg_image_rect = msg_image.get_rect()
            msg_image_rect.center = self.rect_bg.center
            self.screen.blit(msg_image, msg_image_rect)


class Node_Data():
    def __init__(self, as_setting, screen):
        self.row_cnt , self.col_cnt, self.cell_length = as_setting.row_cnt ,as_setting.col_cnt, as_setting.cell_width
        self.node_arr = [[One_Node(i, j, self.cell_length, screen) for j in range(self.col_cnt)] for i in range(self.col_cnt)]

        # 起点和终点信息
        self.node_info = {"start":[-1,-1], "end":[-1,-1]}

        self.as_setting = as_setting

        # 以下是寻路信息
        self.min_Fx = []
        self.buffer = None
        self.fx_new = [[-1 for i in range(self.col_cnt)] for j in range(self.row_cnt)]
        self.is_find_way = False
        self.is_start = False

        self.set_rand_start_end_block()

    def set_rand_start_end_block(self):
        beta = 0.2
        cnt = 0
        rand_list = [[val // self.col_cnt, val % self.col_cnt] for val in range(self.row_cnt * self.col_cnt)]
        while cnt < self.row_cnt * self.col_cnt * beta:
            cnt += 1
            rand_index = randint(0, len(rand_list) - 1)
            i, j = rand_list.pop(rand_index)
            self.node_arr[i][j].cell_type = "block"

        rand_index = randint(0, len(rand_list) - 1)
        i, j = rand_list.pop(rand_index)
        self.node_arr[i][j].cell_type = "start"
        self.node_info["start"] = [i, j]

        rand_index = randint(0, len(rand_list) - 1)
        i, j = rand_list.pop(rand_index)
        self.node_arr[i][j].cell_type = "end"
        self.node_info["end"] = [i, j]




    def run_once(self):
        print("run once")
        if self.node_info["start"] == [-1, -1] or self.node_info["end"] == [-1, -1]:
            # 缺少起点 或 终点
            self.is_find_way = True # 没有路，直接结束
            return
        if self.is_find_way:
            return
        if self.buffer != None:
            qz, fx, r, c = self.buffer
            self.node_arr[r][c].is_now_find = False
            self.node_arr[r][c].is_finded = True

            self.buffer = None
            if (r, c) == (self.node_info["end"][0], self.node_info["end"][1]):
                # 找到终点了
                self.is_find_way = True
                self.as_setting.is_auto_run = False  # 已经找到路径了
                f_r, f_c = self.node_arr[r][c].formal_node
                while [f_r, f_c] != [-1, -1]:
                    self.node_arr[f_r][f_c].is_in_final_way = True
                    f_r, f_c = self.node_arr[f_r][f_c].formal_node
                return
            # 开始 找 r,c 附近的点
            now_gx = self.node_arr[r][c].gx
            e_r, e_c = self.node_info["end"]
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    next_r, next_c = r + dr, c + dc
                    if next_r < 0 or next_r >= self.row_cnt or next_c < 0 or next_c >= self.col_cnt:
                        continue
                    if dr == 0 and dc == 0:
                        continue
                    if not self.as_setting.can_xzz:
                        if abs(dr + dc) != 1:
                            # 删了这句，可以斜着
                            continue
                    if self.node_arr[next_r][next_c].cell_type == "block":
                        continue
                    if not self.as_setting.can_xzz or abs(dr + dc) == 1:
                        new_gx = now_gx + 1
                    else:
                        new_gx = now_gx + self.as_setting.xzz_alpha
                    if new_gx < self.node_arr[next_r][next_c].gx - 0.000001 or self.node_arr[next_r][next_c].gx == -1:
                        self.node_arr[next_r][next_c].gx = new_gx
                        if self.node_arr[next_r][next_c].hx == -1:
                            if not self.as_setting.can_xzz:
                                self.node_arr[next_r][next_c].hx = abs(next_r - e_r) + abs(next_c - e_c)
                            else:
                                # 可以斜着走
                                max_, min_ = max(abs(next_r - e_r), abs(next_c - e_c)), min(abs(next_r - e_r), abs(next_c - e_c))
                                self.node_arr[next_r][next_c].hx = min_ * self.as_setting.xzz_alpha + max_ - min_
                        self.node_arr[next_r][next_c].fx = self.node_arr[next_r][next_c].gx + self.node_arr[next_r][next_c].hx
                        self.node_arr[next_r][next_c].formal_node = [r, c]

                        self.fx_new[next_r][next_c] = self.node_arr[next_r][next_c].fx # 更新
                        heappush(self.min_Fx, [self.fx_new[next_r][next_c] + self.node_arr[next_r][next_c].hx * 0.00001,self.fx_new[next_r][next_c], next_r, next_c])
            return
        if len(self.min_Fx) == 0:
            if self.is_start:
                # 已经开始了，但是又空了
                self.is_start = False
                self.is_find_way = True # 没有路可以找了，结束
                print("can not find a way")
                return
            self.is_start = True
            s_r, s_c = self.node_info["start"]
            e_r, e_c = self.node_info["end"]
            self.node_arr[s_r][s_c].gx = 0
            if not self.as_setting.can_xzz:
                self.node_arr[s_r][s_c].hx = abs(s_r - e_r) + abs(s_c - e_c)
            else:
                max_, min_ = max(abs(s_r - e_r), abs(s_c - e_c)), min(abs(s_r - e_r), abs(s_c - e_c))
                self.node_arr[s_r][s_c].hx = min_ * self.as_setting.xzz_alpha + max_ - min_
                # self.node_arr[s_r][s_c].hx = max(abs(s_r - e_r), abs(s_c - e_c))
            self.node_arr[s_r][s_c].fx = self.node_arr[s_r][s_c].gx + self.node_arr[s_r][s_c].hx
            tmp_ = [self.node_arr[s_r][s_c].fx + self.node_arr[s_r][s_c].hx * 0.00001, self.node_arr[s_r][s_c].fx, s_r, s_c]
            heappush(self.min_Fx, tmp_)
            self.fx_new[s_r][s_c] = self.node_arr[s_r][s_c].fx
        else:
            print("here")
            self.buffer = heappop(self.min_Fx)
            qz, fx, r, c = self.buffer
            while fx > self.fx_new[r][c] + 0.000001:
                if len(self.min_Fx) == 0:
                    return
                self.buffer = heappop(self.min_Fx)
                qz, fx, r, c = self.buffer
            self.node_arr[r][c].is_now_find = True # 当前选到这个节点




    def clear_A_star_data(self):
        print("re find way")
        for lines in self.node_arr:
            for node in lines:
                node.gx, node.fx, node.hx, node.formal_node = -1, -1, -1, [-1, -1]
                node.is_now_find = False
                node.is_finded = False
                node.is_in_final_way = False
        self.min_Fx = []
        self.fx_new = [[-1 for i in range(self.col_cnt)] for j in range(self.row_cnt)]
        self.buffer = None
        self.is_find_way = False
        self.is_start = False
        return

    def clear_all_data(self):
        self.clear_A_star_data()
        self.node_info = {"start": [-1, -1], "end": [-1, -1]}
        for lines in self.node_arr:
            for node in lines:
                node.cell_type = "blank"


    def draw_nodes(self):
        for lines in self.node_arr:
            for node in lines:
                node.draw_button()