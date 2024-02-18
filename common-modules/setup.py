import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="common_modules",
    version="0.0.1",
    author="Mentorlink",
    author_email="rkasralikar@gmail.com",
    description="Common modules for mentorlink development",
    url="https://github.com/rkasralikar/mentorlink/common-modules",
    packages=setuptools.find_packages(),
    python_requires='>=2.7',
)
