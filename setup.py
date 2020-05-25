from setuptools import setup

setup(name='rubiks_cube_gym',
      version='0.0.2',
      url="https://github.com/DoubleGremlin181/RubiksCubeGym/",
      description="OpenAI Gym environments for various twisty puzzles",
      keywords='environment, agent, rl, rubiks, cube, openai-gym, gym',
      author="Kavish Hukmani",
      author_email="khukmani@gmail.com",
      license="MIT",
      install_requires=['gym', 'numpy', 'opencv-python', 'wget']
)
