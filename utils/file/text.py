from ..data.list import split_list_by_type, subset
import os

def txt2folds(in_path,out_dir,fold_num):
    """
    txt文件注释划分fold_num折
    txt注释每行样式: anno type
    """
    assert os.path.exists(in_path)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    annos = []
    anno2type = {}
    with open(in_path,'r') as f:
        ls = f.readlines()
        for l in ls:
            annos.append(l)
            its = l.strip('\n').split(' ')
            anno2type[l] = its[1]
    folds = split_list_by_type(annos,annos2type=anno2type,fold_num=fold_num)
    for i in range(fold_num):
        path = os.path.join(out_dir,str(i)+'.txt')
        with open(path,'w') as f:
            for fo in folds[i]:
                f.write(fo)
        dir = os.path.join(out_dir,str(i))
        if not os.path.exists(dir):
            os.makedirs(dir)
        test = folds[i]
        train = []
        for j,fold in enumerate(folds):
            train.extend(fold)
        with open(os.path.join(dir,'train.txt'),'w') as f:
            for t in train:
                f.write(t)
        with open(os.path.join(dir,'test.txt'),'w') as f:
            for t in test:
                f.write(t)
