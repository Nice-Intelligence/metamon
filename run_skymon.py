### File used to run skymon in the metamon environment. Script does not work in the standalone metamon environment without modifications
import argparse
import json

from metamon.env import get_metamon_teams, BattleAgainstBaseline
from metamon.interface import DefaultObservationSpace, DefaultShapedReward, DefaultActionSpace
from metamon.baselines import get_baseline


def BattleBaseline(format, set, opponent):
    team_set = get_metamon_teams(format, set)
    obs_space = DefaultObservationSpace()
    reward_fn = DefaultShapedReward()
    action_space = DefaultActionSpace()

    env = BattleAgainstBaseline(
        battle_format=format,
        observation_space=obs_space,
        action_space=action_space,
        reward_function=reward_fn,
        team_set=team_set,
        opponent_type=get_baseline(opponent),
    )

    # standard `gymnasium` environment
    obs, info = env.reset()
    next_obs, reward, terminated, truncated, info = env.step(env.action_space.sample())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Skymon in Metamon Environment")
    parser.add_argument("-c", "--config", default="../config.json", type=str, help="Path to config file")
    parser.add_argument("-o", "--opponent", default=None, help="Opponent to battle against if None then use Opponent in config file")
    args = parser.parse_args()

    config_file = args.config

    with open(config_file, encoding = "utf8") as f:
        config_dict = json.load(f)

    if args.opponent is not None:
        config_dict['opponent'] = args.opponent

    if config_dict['opponent'] in config_dict['opponents_info'].keys():
        opp_info = config_dict['opponents_info'][config_dict['opponent']]

        if config_dict['battle_format'] not in opp_info['battle_formats']:
            print(f"Error: Battle format {config_dict['battle_format']} not supported by opponent {config_dict['opponent']}")
            exit()

        if opp_info['isBaseline']:
            BattleBaseline(config_dict['battle_format'], config_dict['set'], config_dict['opponent'])

    else:
        print(f"Error: Opponent {config_dict['opponent']} info not found")
