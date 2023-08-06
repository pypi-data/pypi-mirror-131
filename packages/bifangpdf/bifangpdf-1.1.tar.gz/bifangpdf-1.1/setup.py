import setuptools
from pathlib import Path

setuptools.setup(
    name="bifangpdf",  # 需要设置一个独一无二的名字避免和pypi存储库的其他包冲突
    version=1.1,
    long_description=Path("README.md").read_text(),  # 与README文件里的内容关联
    packages=setuptools.find_packages(
        exclude=["test", "data"]),  # 这个method会查看我们的程序，自动发现已定义的包；
    # 然而我们需要告诉它排除test、data这两个文件夹，因为它们不包含源代码
)
