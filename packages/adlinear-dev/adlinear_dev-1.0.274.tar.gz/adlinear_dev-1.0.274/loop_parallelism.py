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


def list_gcs(s: str):
    container_op = dsl.ContainerOp(
        name='main-coon',
        image='eu.gcr.io/second-capsule-253207/adlinear:latest',
        command=['python'],
        arguments=['main_coon.py']
    )
    container_op.add_resource_limit("memory", '100M')
    container_op.add_resource_limit("cpu", '.1')
    container_op.add_resource_request("memory", '100M')
    container_op.add_resource_request("cpu", '.1')
    return container_op


@dsl.pipeline(name='list-gcs-buckets')
def pipeline():
    loop_args = list(range(3))
    with dsl.ParallelFor(loop_args, parallelism=10) as item:
        list_gcs(item)


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(pipeline, __file__ + '.yaml')
