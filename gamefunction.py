import sys
import pygame



def check_event(as_setting, screen, node_arr, button_list, step_run, auto_run, clear_all, change_type):
    """检查事件（鼠标键盘）"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #退出
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # print("mouse_x, mouse_y = ", mouse_x, mouse_y)
            if check_nodes(mouse_x, mouse_y, as_setting, screen, node_arr, button_list):
                return True

            if check_buttons(mouse_x, mouse_y, as_setting, screen, node_arr, button_list):
                return True
            if check_step_run(mouse_x, mouse_y, as_setting, screen, node_arr, button_list, step_run):
                return True

            if check_auto_run(mouse_x, mouse_y, as_setting, screen, node_arr, button_list, auto_run):
                return True

            if check_clear_all(mouse_x, mouse_y, as_setting, screen, node_arr, button_list, clear_all):
                return True

            return check_change_type(mouse_x, mouse_y, as_setting, screen, node_arr, button_list, change_type)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if step_run.rect_bk.collidepoint(mouse_x, mouse_y):
                step_run.is_pressed = True
            if auto_run.rect_bk.collidepoint(mouse_x, mouse_y):
                auto_run.is_pressed = True
            if clear_all.rect_bk.collidepoint(mouse_x, mouse_y):
                clear_all.is_pressed = True
            if change_type.rect_bk.collidepoint(mouse_x, mouse_y):
                change_type.is_pressed = True

            return True
    return False


def check_change_type(mouse_x, mouse_y, as_setting, screen, node_arr, button_list, change_type):
    if not change_type.is_pressed:
        return False
    if change_type.rect_bk.collidepoint(mouse_x, mouse_y):
        change_type.is_pressed = False
        node_arr.clear_A_star_data()
        # as_setting.can_xzz = not as_setting.can_xzz
        # print("as_setting.can_xzz = ", as_setting.can_xzz)
        as_setting.is_auto_run = False # 关闭自动寻路
        # 弹起设置键
        change_type.change_msg()
        for button_ in button_list:
            button_.is_pressed= False
        as_setting.model = "set"
        as_setting.set_which = "None"
    return True



def check_clear_all(mouse_x, mouse_y, as_setting, screen, node_arr, button_list, clear_all):
    if not clear_all.is_pressed:
        return False
    if clear_all.rect_bk.collidepoint(mouse_x, mouse_y):
        clear_all.is_pressed = False
        node_arr.clear_all_data()
        as_setting.is_auto_run = False # 自动也给关了
        # 弹起设置键
        for button_ in button_list:
            button_.is_pressed= False
        as_setting.model = "set"
        as_setting.set_which = "None"
    return True


def check_auto_run(mouse_x, mouse_y, as_setting, screen, node_arr, button_list, auto_run):
    if not auto_run.is_pressed:
        return False
    if auto_run.rect_bk.collidepoint(mouse_x, mouse_y):
        auto_run.is_pressed = False
        as_setting.is_auto_run = True
        # 弹起设置键
        for button_ in button_list:
            button_.is_pressed= False
        as_setting.model = "run"
        as_setting.set_which = "None"
    return True

def check_step_run(mouse_x, mouse_y, as_setting, screen, node_arr, button_list, step_run):
    if not step_run.is_pressed:
        return False
    if step_run.rect_bk.collidepoint(mouse_x, mouse_y):
        step_run.is_pressed = False
        node_arr.run_once()
        as_setting.is_auto_run = False # 单步运行，关闭自动运行
        # 弹起设置键
        for button_ in button_list:
            button_.is_pressed= False
        as_setting.model = "run"
        as_setting.set_which = "None"
    return True

def check_nodes(mouse_x, mouse_y, as_setting, screen, node_arr, button_list):
    if as_setting.model != "set" or as_setting.set_which == "None":
        # set 的时候才检测节点
        return False
    for lines in node_arr.node_arr:
        for node in lines:
            if node.rect_bk.collidepoint(mouse_x, mouse_y):
                # 这个节点被选中
                origin_cell_type = node.cell_type
                if origin_cell_type == "start" or origin_cell_type == "end":
                    node_arr.node_info[origin_cell_type] = [-1, -1] # 取消该点的记录
                node.cell_type = as_setting.set_which
                if as_setting.set_which == "start" or as_setting.set_which == "end":
                    # 设置起点/终点的记录
                    if node_arr.node_info[as_setting.set_which] != [-1, -1]:
                        # 别的节点
                        r, c = node_arr.node_info[as_setting.set_which]
                        node_arr.node_arr[r][c].cell_type = "blank"
                    node_arr.node_info[as_setting.set_which] = [node.row, node.col]
                node_arr.clear_A_star_data()
                as_setting.is_auto_run = False # 重新开始，关闭自动
                return True
    return False

def check_buttons(mouse_x, mouse_y, as_setting, screen, node_arr, button_list):
    is_change_set = False
    for button_ in button_list:
        if button_.rect_bk.collidepoint(mouse_x, mouse_y):
            is_change_set = True
    if is_change_set:
        as_setting.is_auto_run = False # 关自动
        for button_ in button_list:
            button_.is_pressed = False
            if button_.rect_bk.collidepoint(mouse_x, mouse_y):
                button_.is_pressed = True
                as_setting.model = "set"

                if button_.msg == "SET_START":
                    as_setting.set_which = "start"
                elif button_.msg == "SET_END":
                    as_setting.set_which = "end"
                elif button_.msg == "SET_BLOCK":
                    as_setting.set_which = "block"
                elif button_.msg == "SET_BLANK":
                    as_setting.set_which = "blank"
                else:
                    print("ERROR: unexpected button msg:",button_.msg)


        return True
    return False





def update_screen(as_setting, screen, node_arr, button_list, step_run, auto_run, clear_all, change_type):
    """更新屏幕"""

    #背景
    screen.fill(as_setting.bg_color)

    node_arr.draw_nodes()
    for button_ in button_list:
        button_.draw_button()
    step_run.draw_button()
    auto_run.draw_button()
    clear_all.draw_button()
    change_type.draw_button()

    pygame.display.flip()


