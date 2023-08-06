
#  # 只使用distutils
# from distutils.core import setup
# setup(
# 	name='foo_dis',
# 	version='1.0',
# 	description='xxxxxx',
# 	author='TOM',
# 	author_email='xxxxxxxxxx@qq.com',
# 	url='http://xxxxxx/blog',
# 	py_modules=['foo']
# )



from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("foo",["foo.py"])]
setup(
    name = "engigu_foo",
   	version='1.0',
   	description='xxxxxx',
   	author='TOM',
   	author_email='xxxxxxxxxx@qq.com',
   	url='http://xxxxxx/blog',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)

