# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause

"""
Example training script for the grid world and continuous versions of Tag.
"""

import argparse
import os

import torch
import yaml

from example_envs.tag_continuous.tag_continuous import TagContinuous
from example_envs.tag_gridworld.tag_gridworld import CUDATagGridWorld
from warp_drive.env_wrapper import EnvWrapper
from warp_drive.training.trainer import Trainer
from warp_drive.utils.common import get_project_root

pytorch_cuda_init_success = torch.cuda.FloatTensor(8)

_ROOT_DIR = get_project_root()

_TAG_CONTINUOUS = "tag_continuous"
_TAG_GRIDWORLD = "tag_gridworld"

# Example usage (from the root folder):
# >> python warp_drive/training/example_training_script.py --env tag_gridworld
# >> python warp_drive/training/example_training_script.py --env tag_continuous


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--env", "-e", type=str, help="Environment to train.")

    args = parser.parse_args()

    # Read the run configurations specific to each environment.
    # Note: The run config yaml(s) can be edited at warp_drive/training/run_configs
    # ---------------------------------------------------------------------------
    assert args.env in [
        _TAG_CONTINUOUS,
        _TAG_GRIDWORLD,
    ], (
        f"Currently, the environment arguments supported "
        f"are ["
        f"{_TAG_GRIDWORLD}, "
        f"{_TAG_CONTINUOUS}"
        f"]"
    )

    config_path = os.path.join(
        _ROOT_DIR, "warp_drive", "training", "run_configs", f"{args.env}.yaml"
    )
    with open(config_path, "r", encoding="utf8") as fp:
        run_config = yaml.safe_load(fp)

    num_envs = run_config["trainer"]["num_envs"]

    # Create a wrapped environment object via the EnvWrapper
    # Ensure that use_cuda is set to True (in order to run on the GPU)
    # ----------------------------------------------------------------
    if run_config["name"] == _TAG_GRIDWORLD:
        env_wrapper = EnvWrapper(
            CUDATagGridWorld(**run_config["env"]), num_envs=num_envs, use_cuda=True
        )
    elif run_config["name"] == _TAG_CONTINUOUS:
        env_wrapper = EnvWrapper(
            TagContinuous(**run_config["env"]), num_envs=num_envs, use_cuda=True
        )
    else:
        raise NotImplementedError(
            f"Currently, the environments supported are ["
            f"{_TAG_GRIDWORLD}, "
            f"{_TAG_CONTINUOUS}"
            f"]",
        )

    # Initialize shared constants for action index to sampled_actions_placeholder
    # ---------------------------------------------------------------------------
    if run_config["name"] == _TAG_GRIDWORLD:
        kIndexToActionArr = env_wrapper.env.step_actions
        env_wrapper.env.cuda_data_manager.add_shared_constants(
            {"kIndexToActionArr": kIndexToActionArr}
        )
        env_wrapper.env.cuda_function_manager.initialize_shared_constants(
            env_wrapper.env.cuda_data_manager, constant_names=["kIndexToActionArr"]
        )

    # Policy mapping to agent ids: agents can share models
    # The policy_tag_to_agent_id_map dictionary maps
    # policy model names to agent ids.
    # ----------------------------------------------------
    if len(run_config["policy"].keys()) == 1:
        # Using a single (or shared policy) across all agents
        policy_name = list(run_config["policy"])[0]
        policy_tag_to_agent_id_map = {
            policy_name: list(env_wrapper.env.taggers) + list(env_wrapper.env.runners)
        }
    else:
        # Using different policies for different(sets) of agents
        policy_tag_to_agent_id_map = {
            "tagger": list(env_wrapper.env.taggers),
            "runner": list(env_wrapper.env.runners),
        }

    # Assert that all the valid policies are mapped to at least one agent
    assert set(run_config["policy"].keys()) == set(policy_tag_to_agent_id_map.keys())

    # Trainer object
    # --------------
    trainer = Trainer(
        env_wrapper=env_wrapper,
        config=run_config,
        policy_tag_to_agent_id_map=policy_tag_to_agent_id_map,
    )

    # Perform training
    # ----------------
    trainer.train()
    trainer.graceful_close()
