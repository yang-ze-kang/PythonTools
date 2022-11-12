import random


def subset(l, indexs):
    """
    从list l中选出序号为indexs的子list
    """
    sub_list = []
    for index in indexs:
        sub_list.append(l[index])
    return sub_list


def split_list(l, group_num, shuffle=False, left='append'):
    """
    left: 'append' 多余的随机补充在前几个list里
          'remove' 删除多余的
          'alone'  多余的单独作为一个list
    """
    index = list(range(len(l)))
    if shuffle:
        random.shuffle(index)
    elem_num = len(l)//group_num
    splited = []
    for i in range(group_num):
        splited.append(subset(l, index[i*elem_num:(i+1)*elem_num]))
    if group_num*elem_num != len(index):
        if left == 'append':
            for i, ind in enumerate(index[group_num*elem_num:]):
                splited[i].append(l[ind])
        elif left == 'alone':
            splited.append(subset(l, index[group_num*elem_num:]))
    return splited


def split2folds(annos, fold_num, shuffle=False, annos2type=None, bytype=True):
    """
    将list annos划分为多折, 可选按type划分
    """
    if bytype:
        assert annos2type is not None
        ids = list(range(len(annos)))
        type2annos = {}
        for id in ids:
            type = annos2type[annos[id]]
            if type not in type2annos:
                type2annos[type] = []
            type2annos[type].append(id)
        for type in type2annos:
            type2annos[type] = split_list(type2annos[type], fold_num, shuffle)
        folds = []
        for i in range(fold_num):
            fold = []
            for type in type2annos:
                fold.extend(type2annos[type][i])
            if shuffle:
                random.shuffle(fold)
            folds.append(subset(annos, fold))
        return folds
    else:
        return split_list(annos, fold_num, shuffle)
