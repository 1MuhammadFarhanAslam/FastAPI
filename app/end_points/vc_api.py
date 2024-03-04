# tts_api.py
import bittensor as bt
from classes.vc import VoiceCloningService
import torch
import random
import lib


class VC_API(VoiceCloningService):
    def __init__(self):
        super().__init__()
        self.current_index = 0  # Initialize the current index
        self.filtered_axons = self._generate_filtered_axons_list()  # Generate the initial list

    def _generate_filtered_axons_list(self):
        """Generate the list of filtered axons."""
        try:
            uids = self.metagraph.uids.tolist()
            queryable_axons = (self.metagraph.total_stake >= 0).numpy() * torch.Tensor([
                self.metagraph.neurons[uid].axon_info.ip != '0.0.0.0' for uid in uids
            ]).numpy()
            bt.logging.debug(f"Queryable uids in fastapi: {queryable_axons}")
            return [(uid, axon) for uid, axon in zip(uids, queryable_axons) if axon]
        except Exception as e:
            print(f"An error occurred while generating filtered axons list: {e}")
            return []

    def get_filtered_axons(self):
        """Get the next item from the filtered axons list."""
        # Regenerate the list if it was exhausted
        if not self.filtered_axons:
            self.filtered_axons = self._generate_filtered_axons_list()
            self.current_index = 0  # Reset the index

        # Get the next item
        if self.filtered_axons:  # Check if the list is not empty
            item_to_return = self.filtered_axons[self.current_index % len(self.filtered_axons)]
            self.current_index += 1  # Increment for next call
            return item_to_return
        else:
            return None  # Return None if there are no queryable axons
