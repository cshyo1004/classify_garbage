import os

def create_path():
    '''기본 데이터 path 만들기'''
    if not os.path.exists(bpath):
        os.mkdir(bpath)
        os.mkdir(os.path.join(bpath, 'images'))
        os.mkdir(os.path.join(bpath, 'labels'))
        os.mkdir(os.path.join(bpath, 'val'))
        os.mkdir(os.path.join(bpath, 'test'))

def unzipfile():
    '''unzip'''
    path_to_zip_file = 'tacotrashdataset.zip'
    directory_to_extract_to = bpath
    import zipfile
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)

def rename(work_path, save_path):
    '''파일명 변경'''
    import natsort
    lst = natsort.natsorted([x for x in os.listdir(work_path) if os.path.isdir(os.path.join(work_path, x))])
    for folder in lst:
        for file in os.listdir(os.path.join(work_path, folder)):
            os.rename(os.path.join(work_path, folder, file), os.path.join(save_path, f'{folder}_{file}'))
    
def create_txt(lbl_path):
    import pandas as pd
    df = pd.read_csv(os.path.join(bpath, 'meta_df.csv'))
    create_yaml(df)
    grouped = df.groupby('img_file')
    for filename, grouped_data in grouped:
        front = filename.split('/')[0].replace('_','')
        with open(f'{lbl_path}/{front}_{filename.split("/")[1].replace("jpg", "txt")}', 'w') as f:
            for index, value in grouped_data.iterrows():
                img_size = (value["img_width"], value["img_height"])
                bbox = (value["x"], value["y"], value["width"], value["height"])
                x,y,w,h = convert(img_size, bbox)
                f.write(f'{value["cat_id"]} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n')
            
def create_yaml(df):
    '''yaml 생성'''
    with open(f'data/dataset.yaml', 'w') as f:
        f.write(f'path: {bpath}\n')
        f.write(f'train: images\n')
        f.write(f'val: val\n')
        f.write(f'test: test\n')
        f.write(f'names: {list(df["cat_name"].unique())}\n')
        f.write(f'nc: {len(list(df["cat_name"].unique()))}\n')

def convert(img_size, bbox):
    '''annotation 정보 YOLO format으로 변환'''
    x = (bbox[0] + bbox[2] / 2) / img_size[0]
    y = (bbox[1] + bbox[3] / 2) / img_size[1]
    w = bbox[2]/img_size[0]
    h = bbox[3]/img_size[1]
    return x,y,w,h

def order_files(path):
    for findex, file in enumerate(os.listdir(path)):
        os.rename(os.path.join(path, file), os.path.join(path, f'{findex:06d}.{file.split(".")[-1]}'))

def move_files(src, dest, files):
    ''' 폴더 내 파일 이동 '''
    for file in files:
        os.replace(os.path.join(src, file), os.path.join(dest, file))

def split_files(files):
    ''' 폴더 내 파일 비율대로 나누기 / 현재 비율(7:2:1) '''
    import numpy as np
    import math
    np.random.seed(0)
    np.random.shuffle(files)
    val_files, test_files, train_files = np.split(np.array(files), [math.ceil(len(files)*0.2), math.ceil(len(files)*0.3)])
    return train_files, val_files, test_files

def check_folder(folder):
    ''' 폴더가 없을 경우 생성 '''
    if not os.path.exists(folder):
        os.makedirs(folder)

def organize_data(bpath):
    '''데이터 정제 및 분류'''
    wpath = os.path.join(bpath, 'data')
    img_path = os.path.join(bpath, 'images')
    lbl_path = os.path.join(bpath, 'labels')
    test_path = os.path.join(bpath, 'test')
    val_path = os.path.join(bpath, 'val')
    
    create_path()
    unzipfile()
    rename(wpath, img_path)
    create_txt(lbl_path)
    order_files(img_path)
    order_files(lbl_path)
    train_images, val_images, test_images = split_files(os.listdir(img_path))
    train_labels, val_labels, test_labels = split_files(os.listdir(lbl_path))
    check_folder(test_path)
    check_folder(val_path)
    move_files(img_path, val_path, val_images)
    move_files(lbl_path, val_path, val_labels)
    move_files(img_path, test_path, test_images)
    move_files(lbl_path, test_path, test_labels)


if __name__ == "__main__":
    bpath = os.path.join('data', 'dataset')
    organize_data(bpath)

# category_map = dict(sorted({x:y for x,y in zip(df['cat_name'],df['cat_id'])}.items(), key=(lambda i:i[1])))
# scategory_map = {x:i for i, x in enumerate(df['supercategory'].unique())}
# df['scat_id'] = [scategory_map[x] for x in df['supercategory']]

# {x:y for x,y in df['cat_id'].value_counts().items()}
# {x:y for x,y in df['scat_id'].value_counts().items()}
# len(df)
