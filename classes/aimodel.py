# aimodel.py
import os
import argparse
import bittensor as bt
import sys
import asyncio
import traceback
from datasets import load_dataset
import torch
import random
import csv
import pandas as pd
import torchaudio
from tabulate import tabulate
# Import your module
import lib.utils
import lib
import traceback
import platform
import psutil
import GPUtil
import subprocess
from huggingface_hub import hf_hub_download

class AIModelService:
    _scores = None

    def __init__(self):
        self.config = self.get_config()
        self.sys_info = self.get_system_info()
        self.setup_paths()
        self.setup_logging()
        self.setup_wallet()
        self.setup_subtensor()
        self.setup_dendrite()
        self.setup_metagraph()
        self.vcdnp = self.config.vcdnp
        self.max_mse = self.config.max_mse
        self.pt_file = hf_hub_download(repo_id="lukewys/laion_clap", filename="630k-best.pt")
        if AIModelService._scores is None:
            AIModelService._scores = self.metagraph.E.clone().detach()
        self.scores = AIModelService._scores
        self.uid = self.metagraph.hotkeys.index(self.wallet.hotkey.ss58_address)


    def get_config(self):
        parser = argparse.ArgumentParser()

        # Add arguments as per your original script
        parser.add_argument("--alpha", default=0.3, type=float, help="The weight moving average scoring.")
        parser.add_argument("--custom", default="my_custom_value", help="Adds a custom value to the parser.")
        parser.add_argument("--netuid", type=int, default=16, help="The chain subnet uid.")
        parser.add_argument("--vcdnp", type=int, default=10, help="Number of miners to query for each forward call.")
        parser.add_argument("--max_mse", type=float, default=1000.0, help="Maximum Mean Squared Error for Voice cloning.")
        parser.add_argument("--auto_update", type=str, default='no', help="Auto update option for github repository updates.")

        # Add Bittensor specific arguments
        bt.subtensor.add_args(parser)
        bt.logging.add_args(parser)
        bt.wallet.add_args(parser)

        # Parse and return the config
        config = bt.config(parser)
        return config

    def get_system_info(self):
        system_info = {
            "OS -v": platform.platform(),
            "CPU ": os.cpu_count(),
            "RAM": f"{psutil.virtual_memory().total / (1024**3):.2f} GB", 
        }

        gpus = GPUtil.getGPUs()
        if gpus:
            system_info["GPU"] = gpus[0].name 

        # Convert dictionary to list of strings
        tags = [f"{key}: {value}" for key, value in system_info.items()]
        tags.append(lib.__version__)
        return tags

    def setup_paths(self):
        # Set the project root path
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        # Set the 'AudioSubnet' directory path
        audio_subnet_path = os.path.abspath(project_root)

        # Add the project root and 'AudioSubnet' directories to sys.path
        sys.path.insert(0, project_root)
        sys.path.insert(0, audio_subnet_path)

    def setup_logging(self):
        # Set up logging with the provided configuration and directory
        self.config.full_path = os.path.expanduser(
            "{}/{}/{}/netuid{}/{}".format(
                self.config.logging.logging_dir,
                self.config.wallet.name,
                self.config.wallet.hotkey,
                self.config.netuid,
                "validator",
            )
        )
        
        # Ensure the logging directory exists
        if not os.path.exists(self.config.full_path):
            os.makedirs(self.config.full_path, exist_ok=True)

        bt.logging(self.config, logging_dir=self.config.full_path)

    def setup_wallet(self):
        # Initialize the wallet with the provided configuration
        self.wallet = bt.wallet(config=self.config)
        bt.logging.info(f"Wallet: {self.wallet}")


    def setup_subtensor(self):
    # Initialize the subtensor connection with the provided configuration
        self.subtensor = bt.subtensor(config=self.config)
        bt.logging.info(f"Subtensor: {self.subtensor}")

    def setup_dendrite(self):
        # Initialize the dendrite (RPC client) with the wallet
        self.dendrite = bt.dendrite(wallet=self.wallet)
        bt.logging.info(f"Dendrite: {self.dendrite}")

    def setup_metagraph(self):
        # Initialize the metagraph for the network state
        self.metagraph = self.subtensor.metagraph(self.config.netuid)
        bt.logging.info(f"Metagraph: {self.metagraph}")

    def update_score(self, axon, new_score, service, ax):
            try:
                bt.logging.info(f"------------------- the service value is ------------------- : {service}")
                bt.logging.info(f"------------------- the new_score value is ------------------- : {new_score}")
                bt.logging.info(f"------------------- the axon we are getting in axon is ------------------- : {axon}")
                bt.logging.info(f"___________________ the axon we are getting in ax is ___________________ : {ax}")
                try:
                    uids = self.metagraph.uids.tolist()
                except Exception as e:
                    bt.logging.error(f"An error occurred while getting the uids: {e}")
                bt.logging.info(f"------------------- the uids we are getting in uids is ------------------- : {uids}")
                try:
                    zipped_uids = list(zip(uids, self.metagraph.axons))
                except Exception as e:
                    bt.logging.error(f"An error occurred while zipping the uids: {e}")
                bt.logging.info(f"------------------- the zipped_uids we are getting in zipped_uids is ------------------- : {zipped_uids}")
                try:
                    uid_index = list(zip(*filter(lambda x: x[1] == axon, zipped_uids)))[0][0]
                except Exception as e:
                    bt.logging.error(f"An error occurred while getting the uid_index: {e}")
                bt.logging.info(f"------------------- the uid_index we are getting in uid_index is ------------------- : {uid_index}")
                try:
                    if uid_index in ax:
                        alpha = self.config.alpha
                        bt.logging.info(f"------------------- the alpha we are gitting in ax ------------------- : {self.scores[uid_index]}")
                        try:
                            self.scores[uid_index] = alpha * self.scores[uid_index] * (1 - alpha) * new_score * 0.0
                        except Exception as e:
                            print(f"An error occurred while updating the score in update_score functon. yaha ip address wala hai: {e}")
                except Exception as e:
                    print(f"An error occurred while updating the score - checkin if the : {e}")
                else:
                    try:
                        alpha = self.config.alpha
                        bt.logging.info(f"------------------- the alpha we are gitting in else form ------------------- : {self.scores[uid_index]}")
                        try:
                            self.scores[uid_index] = alpha * self.scores[uid_index] + (1 - alpha) * new_score
                        except Exception as e:
                            print(f"An error occurred while updating the score in update_score functon. yaha ip address wala nahi hai: {e}")

                        bt.logging.info(f"Updated score for {service} Hotkey {axon.hotkey}: {self.scores[uid_index]}")
                    except Exception as e:
                        print(f"An error occurred while updating the score - checkin if the error is coming from here or not blah blah blah: {e}")
            except Exception as e:
                print(f"An error occurred while updating the score - checkin if the error is coming from here or not: {e}")


    def punish(self, axon, service, punish_message):
        '''Punish the axon for returning an invalid response'''
        try:
            uids = self.metagraph.uids.tolist()
            zipped_uids = list(zip(uids, self.metagraph.axons))
            uid_index = list(zip(*filter(lambda x: x[1] == axon, zipped_uids)))[0][0]
            alpha = self.config.alpha
            self.scores[uid_index] = alpha * self.scores[uid_index] + (1 - alpha) * (-0.05)
            if self.scores[uid_index] < 0:
                self.scores[uid_index] = 0
            # Log the updated score
            bt.logging.info(f"Score after punishment for Hotkey {axon.hotkey} using {service} is Punished  Due to {punish_message} : {self.scores[uid_index]}")
        except Exception as e:
            print(f"An error occurred while punishing the axon: {e}")

    def get_git_commit_hash(self):
        try:
            # Run the git command to get the current commit hash
            commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
            return commit_hash
        except subprocess.CalledProcessError:
            # If the git command fails, for example, if this is not a git repository
            bt.logging.error("Failed to get git commit hash. '.git' folder is missing")
            return None
        
    async def run_async(self):
        raise NotImplementedError