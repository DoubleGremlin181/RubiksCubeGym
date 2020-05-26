from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='rubiks_cube_gym',
      version='0.0.3',
      url="https://github.com/DoubleGremlin181/RubiksCubeGym/",
      description="OpenAI Gym environments for various twisty puzzles",
      long_description=long_description,
      long_description_content_type='text/markdown',
      keywords='environment, agent, rl, rubiks, cube, openai-gym, gym',
      author="Kavish Hukmani",
      author_email="khukmani@gmail.com",
      license="MIT",
      install_requires=['gym', 'numpy', 'opencv-python', 'wget']
)
