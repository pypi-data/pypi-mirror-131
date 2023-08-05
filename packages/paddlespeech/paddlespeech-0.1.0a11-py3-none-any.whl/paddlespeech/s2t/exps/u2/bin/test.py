# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Evaluation for U2 model."""
import cProfile

from paddlespeech.s2t.exps.u2.config import get_cfg_defaults
from paddlespeech.s2t.exps.u2.model import U2Tester as Tester
from paddlespeech.s2t.training.cli import default_argument_parser
from paddlespeech.s2t.utils.utility import print_arguments

# TODO(hui zhang): dynamic load 


def main_sp(config, args):
    exp = Tester(config, args)
    with exp.eval():
        exp.setup()
        exp.run_test()


def main(config, args):
    main_sp(config, args)


if __name__ == "__main__":
    parser = default_argument_parser()
    # save asr result to 
    parser.add_argument(
        "--result_file", type=str, help="path of save the asr result")
    args = parser.parse_args()
    print_arguments(args, globals())

    # https://yaml.org/type/float.html
    config = get_cfg_defaults()
    if args.config:
        config.merge_from_file(args.config)
    if args.opts:
        config.merge_from_list(args.opts)
    config.freeze()
    print(config)
    if args.dump_config:
        with open(args.dump_config, 'w') as f:
            print(config, file=f)

    # Setting for profiling
    pr = cProfile.Profile()
    pr.runcall(main, config, args)
    pr.dump_stats('test.profile')
