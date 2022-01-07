import os

def unzipfile():
    '''unzip'''
    path_to_zip_file = 'drinking-waste-classification.zip'
    import zipfile
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall('data')

def move_files(src, dest, files):
    ''' 폴더 내 파일 이동 '''
    for file in files:
        os.replace(os.path.join(src, file), os.path.join(dest, file))

def create_path():
    '''기본 데이터 path 만들기'''
    if not os.path.exists(bpath):
        os.mkdir(bpath)
        os.mkdir(os.path.join(bpath, 'images'))
        os.mkdir(os.path.join(bpath, 'labels'))
        os.mkdir(os.path.join(bpath, 'val'))
        os.mkdir(os.path.join(bpath, 'test'))
    else:
        import shutil
        shutil.rmtree(bpath)
        create_path()

def create_yaml():
    '''yaml 생성'''
    with open(f'data/dataset2.yaml', 'w') as f:
        f.write(f'path: {bpath}\n')
        f.write(f'train: images\n')
        f.write(f'val: val\n')
        f.write(f'test: test\n')
        f.write(f'names: {["AluCan", "Glass", "HDPEM", "PET"]}\n')
        f.write(f'nc: {4}')

def split_files(files):
    ''' 폴더 내 파일 비율대로 나누기 / 현재 비율(7:2:1) '''
    import numpy as np
    import math
    np.random.seed(0)
    np.random.shuffle(files)
    val_files, test_files, train_files = np.split(np.array(files), [math.ceil(len(files)*0.2), math.ceil(len(files)*0.3)])
    return train_files, val_files, test_files

if __name__ == "__main__":
    bpath = os.path.join('data', 'dataset2')
    unzipfile()
    src = os.path.join('data', 'Images_of_Waste', 'YOLO_imgs')
    img_path = os.path.join(bpath, 'images')
    lbl_path = os.path.join(bpath, 'labels')
    val_path = os.path.join(bpath, 'val')
    test_path = os.path.join(bpath, 'test')
    img_files = [x for x in os.listdir(src) if x.endswith('jpg') and os.path.exists(os.path.join(src, x.replace('jpg', 'txt')))]
    lbl_files = [x for x in os.listdir(src) if x.endswith('txt')]
    
    create_path()
    move_files(src, os.path.join(bpath, 'images'), img_files)
    move_files(src, os.path.join(bpath, 'labels'), lbl_files)
    create_yaml()
    train_images, val_images, test_images = split_files(os.listdir(img_path))
    train_labels, val_labels, test_labels = split_files(os.listdir(lbl_path))
    move_files(img_path, val_path, val_images)
    move_files(lbl_path, val_path, val_labels)
    move_files(img_path, test_path, test_images)
    move_files(lbl_path, test_path, test_labels)