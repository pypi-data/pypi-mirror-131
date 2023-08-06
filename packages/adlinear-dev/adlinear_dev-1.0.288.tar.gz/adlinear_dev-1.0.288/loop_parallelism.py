# Copyright 2020 The Kubeflow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import kfp.dsl as dsl
import kfp
from kubernetes.client.models import V1Toleration


def main_coon():
    container_op = dsl.ContainerOp(
        name='main-coon',
        image='eu.gcr.io/second-capsule-253207/adlinear:latest',
        command=['python'],
        arguments=['main_coon.py']
    )
    # Single job specification
    container_op.add_resource_limit("memory", '2G')
    container_op.add_resource_limit("cpu", '1')
    container_op.add_resource_request("memory", '2G')
    container_op.add_resource_request("cpu", '1')
    container_op.add_toleration(
        V1Toleration(key="dedicated", operator="Equal", value="standard-preemptible", effect="NoSchedule")
    )
    return container_op


@dsl.pipeline(name='main-coon')
def pipeline():
    loop_args = list(range(20))  # run 20 jobs
    with dsl.ParallelFor(loop_args, parallelism=10) as _:  # On max 10 machines at a time
        main_coon()


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(pipeline, __file__ + '.yaml')
