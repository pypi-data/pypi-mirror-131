
from setuptools import setup, find_packages
 
setup(
    name="deepwonder",
    version="0.2",
    license="MIT Licence",
 
    url="https://github.com/yuanlong-o/Deep_widefield_cal_inferece",
    author="YuanlongZhang&GuoxunZhang",
    author_email="zhanggx19@mails.tsinghua.edu.cn",
 
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['opencv-python==4.1.2.30',
    'tifffile  ==2021.3.5',
    'scikit-image==0.17.2',
    'scikit-learn==0.24.1',
    'scipy==1.5.2',
    'numpy==1.19.2',
    'torch==1.7.1',
    'torchvision==0.8.2',
    'sklearn==0.0',]
)
