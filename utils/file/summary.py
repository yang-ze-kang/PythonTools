import os

def summary_file_count(path, types=None):
    """
    总结各类型文件数目
    """
    def count_file(local_path, type_dict):
        all_file_num = 0
        file_list = os.listdir(local_path)
        for file_name in file_list:
            if os.path.isdir(os.path.join(local_path, file_name)):
                type_dict.setdefault("文件夹", 0)
                type_dict["文件夹"] += 1
                p_local_path = os.path.join(local_path, file_name)
                all_file_num += count_file(p_local_path, type_dict)
            else:
                ext = os.path.splitext(file_name)[1]
                type_dict.setdefault(ext, 0)
                type_dict[ext] += 1
                all_file_num += 1
        return all_file_num
    type_dict = dict()
    file_count = count_file(path, type_dict)
    if types:
        for type in types:
            print(f"文件类型为【{type}】的数量有：{type_dict[type]} 个")
    else:
        for each_type in type_dict:
            print(f"文件类型为【{each_type}】的数量有：{type_dict[each_type]} 个")
        print(f"总文件数量为:{file_count}")
