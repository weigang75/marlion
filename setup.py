import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
   long_description = fh.read()

setuptools.setup(
   name="code_painter",
   version="1.0.0",
   # 与 pyproject.toml 一致：Author 单独字段，Author-email 只放邮箱
   author="weigang",
   author_email="gang.wei@qq.com",
   description="神笔码靓，意如其神笔般神奇，融合代码与艺术魅力，呈现靓丽精彩绘图效果。如神笔马良般，能使虚拟创作成实体物件，让作品跃然纸上，生动呈现世人眼前。",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://gitee.com/march3/code_painter",
   packages=setuptools.find_packages(),
   classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
   ],
   license_files=('LICENSE',),  # 指定license文件
)