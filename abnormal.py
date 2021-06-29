import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image


FONTPATH = "fonts/simsun.ttc"
FONTSIZE = 30
font = ImageFont.truetype(FONTPATH,FONTSIZE)

FONTPATH1 = "fonts/msyhbd.ttc"
FONTSIZE1 = 60
font1 = ImageFont.truetype(FONTPATH1,FONTSIZE1)


def put_text(img, x, y, text, font, fontcolor = (0,0,0)):
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    r,g,b = fontcolor
    a = 0
    draw.text((x, y ),  text, fill = (r,g,b,a), font = font)
    img = np.array(img_pil)
    return img

def make_white(h,w,c):
    white = 255 * np.ones((h,w,c))
    white = white.astype(np.uint8)
    return white

def make_bottom(img, ratio = 0.75):
    h,w,c = img.shape
    gray_y = int(ratio * h)
    background = cv2.rectangle(img, (0, gray_y),(w, h), color = (220,220,220), thickness = -1)
    background = cv2.rectangle(background, (0, 0),(w, h), color = (220,220,220), thickness = 3)
    return background


def random_title():
    abnormals = [
        "这是一个异常", 
        "Abnormal behavior",
        "Can not open file",
        "XXX sortware NOT INSTALL",
        "DISK FULL",
        "Memory Error",
        "Java.lang.exception..",
        "TraceBack..",
        "InternetError",
        "FileInUse",
        "文件损坏",
        "无法发送邮件",
        "访问权限受限",
        "连接丢失",
        "网络超时"
    ]
    return np.random.choice(abnormals)

def random_info():
    abnormals = [
        "您的系统存在巨大的漏洞，实在不好修复了，可咋办啊", 
        "Reboot system to check whether it works",
        "System not compatible, please refer to admin",
        "请检查abcde.dll文件是否存在,不存在你就去下载",
        "系统即将重启，请保存您手头的所有工作",
        "I am a super AI, rm -rf /",
        "JVM is broken, java is no longer running",
        "垃圾回收失败，内存里面全是临时的图片数据",
        "磁盘已经满了，你可以选择倾倒垃圾桶",
        "BIOS配置错误，开机按着F12，去改吧",
        "中关村有硬盘修复服务，你去看看啊",
        "SMTP服务器无法帮你发送超大附件，那个东西还得你自己发送",
        "飞机已经起飞，请您购买下一趟的航班",
        "文件路径包含了各种中文的字符，所以报错",
        "未知ERROR，无法检测系统种存在的问题"
    ]
    return np.random.choice(abnormals)

def random_button():
    abnormals = [
        "确认",
        "重启",
        "打开",
        "关闭",
        "继续",
        "下一步",
        "上一步",
        "浏览"
    ]
    return np.random.choice(abnormals, size = 2, replace = False)




def make_window():
    white = make_white(500,800,3)
    bg = make_bottom(white)
    bg = put_text(bg, 35,50,random_title(),font)
    tmpcolor = (255,0,0) if np.random.random()< 0.5 else (255,np.random.randint(1,255),0) 
    bg = cv2.circle(bg,(150,200),50,tmpcolor, thickness = -1)
    bg = put_text(bg, 130,160,"X",font1, fontcolor = (255,255,255))
    bg = put_text(bg, 220,160,random_info(),font, fontcolor = (0,0,0))

    if np.random.random() < 0.5:
        bg = put_text(bg, 220,200,random_info(),font, fontcolor = (0,0,0))


    bt1, bt2 = random_button()

    startx, starty = 400,400
    endx, endy = startx + 170, starty + 80
    bg = cv2.rectangle(bg,(startx,starty),(endx,endy),color = (170,170,170),thickness = -1)
    bg = put_text(bg, startx + 50, starty + 30,bt1,font)


    if np.random.random() < 0.8:
        startx, starty = 600,400
        endx, endy = startx + 170, starty + 80
        bg = cv2.rectangle(bg,(startx,starty),(endx,endy),color = (170,170,170),thickness = -1)
        bg = put_text(bg, startx + 50, starty + 30,bt2,font)
    return bg

if __name__ == '__main__':
    plt.imshow(make_window())
    plt.show()