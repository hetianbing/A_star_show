import pygame.font


class AS_BUTTON():
    """设置起点/终点/障碍，以及运行 - 按钮"""
    def __init__(self, as_setting, screen, msg = "SET_START"):
        self.bk_color = (10,50,100) # 边框颜色
        self.normal_color = (3, 168, 158) # 正常颜色
        self.pressed_color = (2, 84, 79) # 被按下去的颜色

        self.width = as_setting.button_width
        self.high = as_setting.windows_high // 10

        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 边框
        self.rect_bk = pygame.Rect(0, 0, self.width, self.high)
        self.rect_bk.right = self.screen_rect.right
        if msg == "SET_START":
            self.rect_bk.top = 0
        elif msg == "SET_END":
            self.rect_bk.top = self.high
        elif msg == "SET_BLOCK":
            self.rect_bk.top = self.high * 2
        elif msg == "SET_BLANK":
            self.rect_bk.top = self.high * 3
        elif msg == "STRAIGHT":
            self.rect_bk.top = self.high * 4
        elif msg == "CLEAR":
            self.rect_bk.bottom = self.screen_rect.bottom
        elif msg == "AUTO":
            self.rect_bk.bottom = self.screen_rect.bottom - self.high
        elif msg == "RUN":
            self.rect_bk.bottom = self.screen_rect.bottom - self.high * 2


        # 颜色
        self.rect_bg = pygame.Rect(0, 0, self.width - 1, self.high - 1)
        self.rect_bg.center = self.rect_bk.center

        # 是否被按下
        self.is_pressed = False
        # 是否被暂时按下（还没弹起鼠标
        self.is_tmp_pressed = False

        # 文字 - 格式
        self.font = pygame.font.SysFont(None, self.high // 3)
        # self.font = pygame.font.SysFont(u"C:\Windows\Fonts\simkia.ttf", 70)
        self.msg = msg
        self.text_color = (0, 0, 0)

        self.as_setting = as_setting
        return

    def change_msg(self):
        # 变换方式
        if self.msg == "STRAIGHT":
            self.msg = "SLANTED"
            self.as_setting.can_xzz = True
            self.as_setting.xzz_alpha = 1
            # print("as_setting.can_xzz = ", as_setting.can_xzz)
        elif self.msg == "SLANTED":
            self.msg = "SLANTED_E"
            self.as_setting.can_xzz = True
            self.as_setting.xzz_alpha = 1.4
        elif self.msg == "SLANTED_E":
            self.msg = "STRAIGHT"
            self.as_setting.can_xzz = False

    def draw_button(self):
        # 边框
        self.screen.fill(self.bk_color, self.rect_bk)
        if not self.is_pressed:
            button_color = self.normal_color
        else:
            button_color = self.pressed_color
        if self.msg == "CLEAR":
            if not self.is_pressed:
                button_color = (255, 0, 0)
            else:
                button_color = (230, 0, 0)

        self.screen.fill(button_color, self.rect_bg)
        msg_image = self.font.render(self.msg, True, self.text_color, button_color)
        # msg_image = self.font.render("测试", True, self.text_color, button_color)
        msg_image_rect = msg_image.get_rect()
        msg_image_rect.center = self.rect_bg.center
        self.screen.blit(msg_image, msg_image_rect)







