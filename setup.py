from distutils.core import setup

#
# Please see the License.txt file for more information.
# All other rights reserved.
#
"""
The Practitioners Guide to Graph Data
---------------------------------------
The code and examples to The Practitioners Guide to Graph Data is distributed under the MIT License.
"""

setup(
    name="graphdatabook",
    version="0.0.1",
    license="MIT",
    author="@DeniseKGosnell",
    author_email="denisekgosnell@gmail.com",
    url="http://shop.oreilly.com/product/0636920205746.do",
    download_url='TBD',
    description="Examples alongside The Practitioners Guide to Graph Data",
    long_description=__doc__,
    packages=["graphdatabook", "tests"],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=[
        "requests>=2.21.0",
        "oauthlib==2.1.0",
        "requests-oauthlib==1.0.0",
    ],
    test_suite='nose.collector',
    tests_require=["nose==1.3.7"],
    keywords=['graph', 'graph data', 'oreilly graph book', 'Practitioners Guide to Graph Data', 'datastax'],
    classifiers=[
        "Development Status :: Development",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)