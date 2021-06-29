import faker
import numpy as np
import pandas as pd
import cv2
from PIL import ImageFont, ImageDraw, Image
import os
import uuid 
from config import *

if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

def gen_flight_number():
    c1, c2 = np.random.choice(list(range(ord('A'), ord('Z'))),2)
    num = np.random.choice(np.arange(1000,9999))
    return chr(c1) + chr(c2) + str(num)


def gen_screen_data(n = 30, language = 'CN'):
    header = ['航班号','始发站','终点站','起飞时间','航班状态'] if language == "CN" else ["FlightNo","From","To","Time","Status"]
    status = ['正点','晚点'] if language == "CN" else ["Normal","Delay"]
    fake = faker.Faker('zh_CN') if language == "CN" else faker.Faker()
    data = [[gen_flight_number(),
             fake.city(), 
             fake.city(),
             fake.date_time().strftime('%H:%M:%S'),
             np.random.choice(status)
     ] for _ in range(n)]
    data.insert(0,header)

    data = pd.DataFrame(data, columns = header)
    return data


def make_black(h, w, c = 3):
    """Make a black background"""
    return np.zeros((h,w,c), dtype = np.uint8)


def allocate_rows(img, n_rows = 20):
    """Divide an image into many rows, get the top left and bottom right corner of each row"""
    h,w,c = img.shape
    box_height = h // n_rows
    
    return [[(0, i*box_height), (w, (i+1) * box_height)] 
            for i in range(n_rows)]


def allocate_columns(img, col_proportion = [1,3,3,1,1]):
    w = img.shape[1]
    width = np.array(col_proportion) / np.array(col_proportion).sum()
    col_locs = (w * np.cumsum(width)).astype(int).tolist()
    col_locs = [0] + col_locs[:-1]
    return col_locs   


def make_grid(rows, cols):
    return [[(c, r[0][1])for c in cols] for r in rows ]


def make_backgroupd(img, rows, color1 = (255,0,0), color2 = (0,0,0)):
    """Draw rows in img - Change color by line id"""
    
    i = 0
    
    for (x0, y0), (x1, y1) in rows:
        
        if i % 2 == 1:
            img = cv2.rectangle(img, 
                                (x0, y0), 
                                (x1, y1), 
                                color = color2, 
                                thickness = -1)
        else:
            img = cv2.rectangle(img, 
                                (x0, y0), 
                                (x1, y1),
                                color = color1, 
                                thickness = -1)
        i += 1
    return img


def make_font(fontpath = FONTPATH, fontsize = FONTSIZE):
    return ImageFont.truetype(fontpath, fontsize)


def put_text(img, 
             x, 
             y, 
             text, 
             font,
             fontcolor = (255,255,255), 
             xmargin = 10, 
             ymargin = 10):
    
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    r,g,b = fontcolor
    a = 0
    draw.text((x + xmargin, y + ymargin),  text, fill = (r,g,b,a), font = font)
    img = np.array(img_pil)
    return img


def make_image(data, 
               background, 
               grid, 
               font,
               fontcolor = (255,255,255),
               xmargin = 10, 
               ymargin = 10):
    
    raw = data.values.tolist()
    img = background
    for r, row in enumerate(raw):
        for c, col in enumerate(row):
            x,y = grid[r][c]
            img = put_text(img,
                           x,
                           y,
                           raw[r][c], 
                           font,
                           fontcolor = fontcolor,
                           xmargin = xmargin, 
                           ymargin = ymargin)
    return img


FONT = ImageFont.truetype(FONTPATH,FONTSIZE)

def nameit():
    return uuid.uuid4().hex[:12].upper() + '.jpg'


if __name__ == "__main__":

    for _ in range(N_IMAGES):
        data = gen_screen_data(n = N_RECORDS - 1, language= LANGUAGE)
        black = make_black(*IMAGE_SHAPE)
        rows = allocate_rows(black, N_RECORDS)
        cols = allocate_columns(black,COLUMN_PROPORTION)
        grid = make_grid(rows, cols)

        back = make_backgroupd(black, 
                            rows, 
                            color1 = ROW_COLOR1, 
                            color2 = ROW_COLOR2)

        img = make_image(data, 
                        back, 
                        grid, 
                        font = FONT,
                        fontcolor = FONTCOLOR,
                        xmargin = CELL_XMARGIN, 
                        ymargin = CELL_YMARGIN)
        
        cv2.imwrite(os.path.join(IMAGE_FOLDER, nameit()),cv2.cvtColor(img, cv2.COLOR_RGB2BGR))