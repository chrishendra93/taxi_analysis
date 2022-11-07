"""Setup for the m6anet package."""

from setuptools import setup,find_packages

__pkg_name__ = 'taxi_analysis'


with open('README.md') as f:
    README = f.read()

setup(
    author="Christopher Hendra",
    maintainer_email="chrishendra93@gmail.com",
    name=__pkg_name__,
    license="MIT",
    description='taxi_analysis is a collection of scripts and notebooks performing simple modelling and data analysis on the chicago taxi dataset.',
    version='v1.0.0',
    long_description=README,
    url='https://github.com/chrishendra93/taxi_analysis',
    packages=find_packages(),
    package_data={'': ['model/nn_model.pth', 'model/scaler.joblib', 'model/xgb_clf.joblib']},
    python_requires=">=3.7",
    install_requires=[
            'pyproj==3.2.1',
            'torch>=1.6.0',
            'Shapely==1.8.5.post1',
            'Rtree==1.0.1',
            'numpy==1.21.5',
            'pandas==1.3.5',
            'scikit-learn==0.24.1',
            'mapclassify==2.4.3',
            'scipy==1.7.3',
            'xgboost==1.6.2',
            'statsmodels==0.13.2',
            'joblib',
            'jupyter',
            'geopandas==0.10.2',
            'matplotlib==3.5.2',
            ],
    entry_points={'console_scripts': ["clean_data={}.scripts.clean_taxi_data:main".format(__pkg_name__),
                                      "run_inference={}.scripts.run_inference:main".format(__pkg_name__)]},
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Intended Audience :: Science/Research',
    ],
)
