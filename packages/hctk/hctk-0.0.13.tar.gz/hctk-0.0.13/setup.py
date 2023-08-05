from setuptools import setup
from itertools import chain

with open("README.md", encoding="utf-8") as f:
      long_description = f.read().strip()


with open("VERSION") as f:
      v = int(f.read().strip())

EXTRAS_REQUIRE = {
      'sense': ['transformers', 'torch', 'opencc', 'umap-learn', 'yellowbrick>=1.3'],
      'colab': ['datashader', 'bokeh', 'holoviews', 'scikit-image', 'colorcet'],
}
EXTRAS_REQUIRE['all'] = list(set(chain(*EXTRAS_REQUIRE.values())))

setup(name='hctk',
      version=f'0.0.{v}',
      description="Hanzi Corpus toolkit",
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/liao961120/hctk',
      author='Yongfu Liao',
      author_email='liao961120@github.com',
      license='MIT',
      packages=['hctk'],
      package_data={
            "": ["../data/radical_semantic_tag.json"],
      },
      install_requires=['scikit-learn', 'scipy', 'gdown>=3.10.2', 'pyyaml>=5.1', 'cqls', 'tqdm', 'CompoTree', 'hanziPhon', 'pickle5; python_version < "3.8.0"'],
      # dependency_links=[
      #       'https://github.com/liao961120/CompoTree/tarball/main',
      # ],
      extras_require=EXTRAS_REQUIRE,
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      python_requires='>=3.7',
      # tests_require=['deepdiff'],
      zip_safe=False)
