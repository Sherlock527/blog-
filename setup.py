from distutils.core import setup
import glob


setup(
    name="blog",
    version="0.1.1",
    author="SherLocK",
    author_email="sherlock@qq.com",
    description="react django blog project test",
    url="http://www.magedu.com",
    packages=["blog", "post", "user"],
    data_files=glob.glob("templates/*.html") + ["requirements", "manage.py"]  # 可以不打包manage.py
)
