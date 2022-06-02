# A_star_show
show the process of the A star program

```bash
python main.py
```
It will show you a Graphical interface based on pygame. The program will not succcess without pygame.

```bash
packge.bat
```
It will package the program into an executable file.(./dist/main.exe)


# 说明
全项目使用pygame作为图形化显示和设置。
可以通过运行 packge.bat脚本打包文件成为main.exe，这样就可以迁移到其他没有安装pygame的电脑上运行了。
打包文件需要有PyInstaller库。

# 开始运行
执行callme.bat， 或者运行main.py启动。
启动后，图中会随机初始化一个地图。
右边的按钮含义分别为：
```bash
SET_START :按下设置路径的起始点， 红色为起始点
SET_END   :按下设置路径的终点， 淡蓝色为终点
SET_BLOCK :按下设置障碍物， 黑色为障碍物
SET_BLANK :按下设置空白路径（用于删除起点、终点和障碍物）
STRAIGHT  :模式，按下转变模式。分为STRAIGHT（横向与纵向），SLANTED（包含对角线，并且对角线的时间和横竖时间相同），SLANTED_E（包含对角线，并且对角线的时间是横竖时间的1.4倍）  

RUN       :运行（单步寻路）
AUTO      :自动寻路，结束或者找不到路径结束
CLEAR     :清除所有设置的起点、终点和障碍物以及路径。
```
每个格子中：
正中间的最大的数值，是A星算法里面的fx（gx+hx）
左下角黑色数字：gx（已经走过的）
右下角橙色数字：hx（预估距离）
格子红色边框：当前的节点
格子绿色底色：已经搜索过的节点
格子亮蓝底色：最终路径
格子红色底色：起点
格子淡蓝色底色：终点
格子白色底色：空白或者探寻过的点


