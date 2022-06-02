import pygame

class Setting():
    """A星寻路的相关设置"""
    def __init__(self, width = 1024, high = 768):
        # 屏幕大小
        self.screen_width = width
        self.screen_high = high

        # 窗口大小
        self.windows_width = max(self.screen_width - 200, self.screen_width // 2)
        self.windows_high = max(self.screen_high - 200, self.screen_high // 2)

        # 模式
        self.model = 'set'
        # self.model = 'run'
        self.set_which = "None"

        # 行列格子数
        self.row_cnt = 12
        self.col_cnt = 12

        # 侧边栏宽度
        self.button_width = self.windows_width // 8

        # 格子大小
        self.cell_width = (self.windows_width - self.button_width) // self.col_cnt
        self.cell_high = self.windows_high // self.row_cnt

        # 修正格子数
        if self.cell_width < self.cell_high:
            # 缩小 self.cell_high
            self.cell_high = self.cell_width
            self.row_cnt = self.windows_high // self.cell_high
        elif self.cell_width > self.cell_high:
            # 缩小 self.cell_width
            self.cell_width = self.cell_high
            self.col_cnt = self.windows_width // self.cell_width

        # 修正窗口大小
        self.windows_high = self.cell_high * self.row_cnt
        self.windows_width = self.cell_width * self.col_cnt + self.button_width

        # 背景颜色
        self.bg_color = (255, 255, 255)

        # 自动运行
        self.is_auto_run = False
        self.last_time = 0
        self.delay_time = 0.01

        # 能否斜着走
        self.can_xzz = False
        self.xzz_alpha = 1


    def show_settings(self):
        print("self.screen_width, self.screen_high = ", self.screen_width, self.screen_high)
        print("self.windows_width, self.windows_high = ", self.windows_width, self.windows_high)
        print("self.cell_width, self.cell_high = ", self.cell_width, self.cell_high)
        print("self.row_cnt, self.col_cnt = ", self.row_cnt, self.col_cnt)





    


    