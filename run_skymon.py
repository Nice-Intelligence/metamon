### File used to run skymon in the metamon environment. Script does not work in the standalone metamon environment without modifications

from metamon.env import get_metamon_teams, BattleAgainstBaseline
from metamon.interface import DefaultObservationSpace, DefaultShapedReward, DefaultActionSpace
from metamon.baselines import get_baseline

team_set = get_metamon_teams("gen1ou", "competitive")
obs_space = DefaultObservationSpace()
reward_fn = DefaultShapedReward()
action_space = DefaultActionSpace()

env = BattleAgainstBaseline(
    battle_format="gen1ou",
    observation_space=obs_space,
    action_space=action_space,
    reward_function=reward_fn,
    team_set=team_set,
    opponent_type=get_baseline("Gen1BossAI"),
)

# standard `gymnasium` environment
obs, info = env.reset()
next_obs, reward, terminated, truncated, info = env.step(env.action_space.sample())