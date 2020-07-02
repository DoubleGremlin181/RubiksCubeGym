from gym.envs.registration import register

register(
    id='rubiks-cube-222-v0',
    entry_point='rubiks_cube_gym.envs:RubiksCube222Env',
    max_episode_steps=250,
)

register(
    id='rubiks-cube-222-lbl-v0',
    entry_point='rubiks_cube_gym.envs:RubiksCube222EnvLBL',
    max_episode_steps=250,
)

register(
    id='rubiks-cube-222-ortega-v0',
    entry_point='rubiks_cube_gym.envs:RubiksCube222EnvOrtega',
    max_episode_steps=250,
)

register(
    id='pyraminx-wo-tips-v0',
    entry_point='rubiks_cube_gym.envs:PyraminxWoTipsEnv',
    max_episode_steps=250,
)

register(
    id='pyraminx-wo-tips-lbl-v0',
    entry_point='rubiks_cube_gym.envs:PyraminxWoTipsEnvLBL',
    max_episode_steps=250,
)

register(
    id='skewb-v0',
    entry_point='rubiks_cube_gym.envs:SkewbEnv',
    max_episode_steps=250,
)

register(
    id='skewb-sarah-v0',
    entry_point='rubiks_cube_gym.envs:SkewbEnvSarah',
    max_episode_steps=250,
)