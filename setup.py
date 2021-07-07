from setuptools import setup

setup(name='gpumeter',
      version='1.0.3',
      description='Power Meter for NVIDIA GPUs',
      author='Xiaozhe Yao',
      author_email='xiaozhe.yaoi@gmail.com',
      url='https://github.com/autoai-incubator/powermeter',
      packages=['gpumeter'],      
      install_requires=[
          'py3nvml',
      ],
)
