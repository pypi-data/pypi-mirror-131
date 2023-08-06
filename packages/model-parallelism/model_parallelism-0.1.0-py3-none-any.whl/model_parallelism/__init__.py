import logging

import deepspeed

logger = logging.getLogger(__name__)


def initialize(model, optimizer=None, **kwargs):
    """
    Takes a torch.nn.Module as a model and an optional optimizer.
    """
    logger.info("Creating DeepSpeed engine")

    batch_size = kwargs.pop("batch_size")

    learning_rate = kwargs.pop("learning_rate")

    ds_config = {
        "train_micro_batch_size_per_gpu": batch_size,
        "fp16": {"enabled": True},
        "zero_optimization": {
            "stage": 2,
            "overlap_comm": True,
            "offload_optimizer": {"device": "cpu"},
            "cput_offload": True,
            "round_robin_gradients": True,
        },
    }

    if isinstance(optimizer, str):
        ds_config["optimizer"] = {"type": optimizer, "params": {"lr": learning_rate}}

    if not isinstance(optimizer, str) and optimizer is not None:
        engine, optimizer, _, _ = deepspeed.initialize(
            model=model, optimizer=optimizer, config=ds_config
        )
        return engine, optimizer
    else:
        engine, _, _, _ = deepspeed.initialize(
            model=model, model_parameters=model.parameters(), config=ds_config
        )
        return engine
