import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from copy import deepcopy
import os
import pandas as pd

def pil_draw_rect(img, point1, point2, object_name):
    draw = ImageDraw.Draw(img)
    draw.rectangle((point1, point2), outline=(0, 255, 0), width=1)
    font = ImageFont.truetype("arial.ttf", 5)
    draw.text((point1[0]-5, point1[1]-10),f'{object_name}', fill="black", font=font)
    return img


def annotate(img, label_info):
    fimg = deepcopy(img)
    for index, info in label_info.iterrows():
        point1 = (info['x'], info['y'])
        point2 = (info['x']+info['width'], info['y']+info['height'])
        object_name = info['cat_name']
        fimg = pil_draw_rect(img, point1, point2, object_name)
    return fimg
    
    
if __name__ == "__main__":
    st.set_page_config(page_title='app', page_icon="random", layout="wide")
    meta = pd.read_csv('data/dataset/meta_df.csv')
    with st.sidebar.expander("menu", expanded=True):
        img_name = st.text_input('파일명을 입력하세요')
        img_bpath = os.path.join('data', 'dataset', 'data')
    if img_name:
        label_info = meta[meta['img_file'] == img_name]
        img_path = os.path.join(img_bpath, img_name.split('/')[0])
        name = img_name.split('/')[-1]
        img = Image.open(os.path.join(img_path, name))
        fimg = annotate(img, label_info)
        fimg = fimg.resize((900,700))
        st.image(fimg)