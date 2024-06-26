# Copyright 2024 Ant Group Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict

from benchmark_examples.autoattack import global_config
from benchmark_examples.autoattack.applications.base import ApplicationBase, InputMode
from benchmark_examples.autoattack.attacks.base import AttackBase, AttackType
from benchmark_examples.autoattack.defenses.base import DefenseBase
from secretflow.ml.nn.callbacks import Callback
from secretflow.ml.nn.sl.defenses.mid import MIDefense


class Mid(DefenseBase):
    def __str__(self):
        return 'mid'

    def build_defense_callback(self, app: ApplicationBase) -> Callback | None:
        print(f"feainput nums = {app.get_device_f_fea_nums()}")
        return MIDefense(
            base_params={
                app.device_f: {
                    "input_dim": app.hidden_size,
                    "output_dim": app.hidden_size,
                    "mid_lambda": self.config.get('mid_lambda', 0.5),
                }
            },
            fuse_params={
                app.device_f: {
                    "input_dim": app.hidden_size,
                    "output_dim": app.hidden_size,
                    "mid_lambda": self.config.get('mid_lambda', 0.5),
                }
            },
            exec_device='cuda' if global_config.is_use_gpu() else 'cpu',
        )

    def check_attack_valid(self, attack: AttackBase) -> bool:
        return attack.attack_type() in [AttackType.FEATURE_INFERENCE]

    def check_app_valid(self, app: ApplicationBase) -> bool:
        return app.base_input_mode() == InputMode.SINGLE

    def tune_metrics(self) -> Dict[str, str]:
        return {}
