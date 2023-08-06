"""
(c) ZL-2020.
@author ZhaoLei (https://zlcnup.com)
@since 2020.10.29 22:20
"""
INFO = dict(
    name='aiei',
    version='1.0.0',
    author='Lei Zhao',
    author_email='zlchn@qq.com',
    url='https://zlcnup.com',
    project_urls={
        'home': 'https://zlcnup.com',
        'github': 'https://github.com/zlcnup',
    },
    description='A tiny framework for AI.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.6.0',
    license='Apache',
    keywords=['deep learning', 'pytorch', 'AI', 'EI'],
)

VERSION = tuple([int(i) for i in INFO['version'].split('.')])
