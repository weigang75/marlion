import os
import zipfile


def unzip_and_delete(zip_dir):
    # 遍历指定目录
    for item in os.listdir(zip_dir):
        # 构造完整路径
        item_path = os.path.join(zip_dir, item)

        # 检查是否是 ZIP 文件
        if item.endswith('.zip') and os.path.isfile(item_path):
            # 创建以 ZIP 文件名称命名的目录
            folder_name = os.path.splitext(item)[0]  # 去掉 .zip 后缀
            extract_dir = os.path.join(zip_dir, folder_name)
            os.makedirs(extract_dir, exist_ok=True)  # 创建目录

            # 解压 ZIP 文件到指定目录
            with zipfile.ZipFile(item_path, 'r') as zip_ref:
                for zip_info in zip_ref.infolist():
                    # 尝试用 gbk 编码来处理中文文件名
                    try:
                        zip_info.filename = zip_info.filename.encode('cp437').decode('gbk')
                    except UnicodeDecodeError:
                        print(f"解码文件名时出错: {zip_info.filename}")
                        continue  # 跳过无法解码的文件名

                    # 提取文件
                    zip_ref.extract(zip_info, extract_dir)

            # 删除 ZIP 文件
            # os.remove(item_path)
            print(f"解压到目录: {extract_dir} 并删除了: {item_path}")

            # 删除解压目录中的 .png 和 .gif 文件
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    if file.endswith('.png') or file.endswith('.gif') or \
                            file.endswith('.url') or file.endswith('.txt') or file.endswith('.jpg'):
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                        # print(f"删除文件: {file_path}")


def unzip_and_delete(zip_dir):
    extract_dir = zip_dir
    # 遍历指定目录
    for item in os.listdir(zip_dir):
        # 构造完整路径
        item_path = os.path.join(zip_dir, item)

        # 检查是否是 ZIP 文件
        if item.endswith('.zip') and os.path.isfile(item_path):
            # 解压 ZIP 文件到指定目录
            with zipfile.ZipFile(item_path, 'r') as zip_ref:
                for zip_info in zip_ref.infolist():
                    # 尝试用 gbk 编码来处理中文文件名
                    try:
                        zip_info.filename = zip_info.filename.encode('cp437').decode('gbk')
                    except UnicodeDecodeError:
                        print(f"解码文件名时出错: {zip_info.filename}")
                        continue  # 跳过无法解码的文件名

                    # 提取文件
                    zip_ref.extract(zip_info, extract_dir)

            # 删除 ZIP 文件
            os.remove(item_path)
            print(f"解压并删除了: {item_path}")

            # 删除解压目录中的 .png 和 .gif 文件
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    if file.endswith('.png') or file.endswith('.gif') or \
                            file.endswith('.url') or file.endswith('.txt') or file.endswith('.jpg'):
                        file_path = os.path.join(root, file)
                        os.remove(file_path)


# 使用示例
zip_directory = r'H:\中国大陆无版权字体'  # 替换为你的目录路径
# unzip_and_delete(zip_directory)