import os

import tensorflow as tf
import numpy as np

from tensor2tensor import problems
from tensor2tensor.utils import trainer_lib
from tensor2tensor.utils import registry

tfe = tf.contrib.eager
tfe.enable_eager_execution()

Modes = tf.estimator.ModeKeys


class ProblemManager():
    def __init__(self, root_dir, model_name="transformer",
                 hparams_set="transformer_base_single_gpu"):
        data_dir = os.path.join(root_dir, 'data')
        train_dir = os.path.join(root_dir, 'train')

        problem_name_file = open(os.path.join(root_dir, 'problem_name'))
        problem_name = problem_name_file.readline()[:-1]
        problem_name_file.close()
        problem = problems.problem(problem_name)

        self.encoders = problem.feature_encoders(data_dir)

        hparams = trainer_lib.create_hparams(hparams_set, data_dir=data_dir,
                                             problem_name=problem_name)

        self.translate_model = registry.model(model_name)(hparams, Modes.EVAL)

        checkpoint_file = open(os.path.join(train_dir, 'checkpoint'))
        ckpt_name = checkpoint_file.readline()[24:-2]
        checkpoint_file.close()
        self.ckpt_path = os.path.join(train_dir, ckpt_name)

    def encode(self, input_str):
        """Input str to features dict, ready for inference"""
        inputs = self.encoders["inputs"].encode(input_str) + [1]
        batch_inputs = tf.reshape(inputs, [1, -1, 1])
        return {"inputs": batch_inputs}

    def decode(self, integers):
        """List of ints to str"""
        integers = list(np.squeeze(integers))
        if 1 in integers:
            integers = integers[:integers.index(1)]
        return self.encoders["inputs"].decode(integers)

    def translate(self, inputs):
        encoded_inputs = self.encode(inputs)
        with tfe.restore_variables_on_create(self.ckpt_path):
            model_output = self.translate_model.infer(encoded_inputs)[
                "outputs"]
        return self.decode(model_output)
