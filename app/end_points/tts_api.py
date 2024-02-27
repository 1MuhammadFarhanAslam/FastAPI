import bittensor as bt
from classes.tts import TextToSpeechService
import torch
import random
import lib


class TTS_API(TextToSpeechService):
    def __init__(self):
        super().__init__()
        self.output_path = None  # Initialize output_path attribute

    def get_filtered_axons(self):
        try:
            uids = self.metagraph.uids.tolist()
            queryable_uids = (self.metagraph.total_stake >= 0)

            queryable_uids = queryable_uids * torch.Tensor([
                self.metagraph.neurons[uid].axon_info.ip != '0.0.0.0' for uid in uids
            ])

            queryable_uid = queryable_uids * torch.Tensor([
                any(self.metagraph.neurons[uid].axon_info.ip == ip for ip in lib.BLACKLISTED_IPS) or
                any(self.metagraph.neurons[uid].axon_info.ip.startswith(prefix) for prefix in lib.BLACKLISTED_IPS_SEG)
                for uid in uids
            ])

            bt.logging.debug(f"Queryable uids in fastapi: {queryable_uids}")
        except Exception as e:
            print(f"An error occurred while filtering queryable uids in fastapi: {e}")

        try:
            active_miners = torch.sum(queryable_uids)
            dendrites_per_query = self.total_dendrites_per_query

            if active_miners == 0:
                active_miners = 1

            if active_miners < self.total_dendrites_per_query * 3:
                dendrites_per_query = int(active_miners / 3)
            else:
                dendrites_per_query = self.total_dendrites_per_query

            bt.logging.debug(f"Dendrites per query in fastapi: {dendrites_per_query}")
        except Exception as e:
            print(f"An error occurred while dendrites per query calculation in fastapi : {e}")

        try:
            if dendrites_per_query < self.minimum_dendrites_per_query:
                dendrites_per_query = self.minimum_dendrites_per_query

            bt.logging.debug(f"Dendrites per query in fastapi 2nd time: {dendrites_per_query}")

            zipped_uids = list(zip(uids, queryable_uids))
            bt.logging.debug(f"Zipped uids in fastapi: {zipped_uids}")

            zipped_uid = list(zip(uids, queryable_uid))
            bt.logging.debug(f"Zipped uid in fastapi: {zipped_uid}")

            filtered_zipped_uids = list(filter(lambda x: x[1], zipped_uids))
            filtered_uids = [item[0] for item in filtered_zipped_uids] if filtered_zipped_uids else []
            bt.logging.debug(f"Filtered uids in fastapi: {filtered_uids}")

            filtered_zipped_uid = list(filter(lambda x: x[1], zipped_uid))
            filtered_uid = [item[0] for item in filtered_zipped_uid] if filtered_zipped_uid else []

            self.filtered_axon = filtered_uids
            bt.logging.info(f"Filtered axons in fastapi: {self.filtered_axon}")
        except Exception as e:
            print(f"An error occurred while filtering axons in fastapi: {e}")

        return self.filtered_axon  # Return filtered axons list

    
