# Copyright 2020 Vadim Sharay <vadimsharay@gmail.com>
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

import click


@click.command()
@click.option(
    "--uri",
    default="mongodb://root:root@localhost:27017/default?authSource=admin",
    prompt="Enter database uri",
    help="full uri (with database) [default: mongodb://root:root@localhost:27017/default?authSource=admin]",
)
@click.option(
    "--collection", prompt="Collection name [required]", help="Mongodb collection name"
)
@click.option("--path", default=".", help="tfrecords destination path")
@click.option(
    "--features",
    default="",
    help="features list (ex. field1,field2,field3) [default: all]",
)
@click.option(
    "--files_template",
    default="{}.tfrecord",
    help="tfrecord file name format [default: '{}.tfrecord']",
)
@click.option(
    "--count_per_file",
    default=100000,
    help="Count items per one tfrecord file [default: 100000]",
)
@click.option("--skip", default=0, help="default: None")
@click.option("--limit", default=0, help="default: None")
@click.option("--verbose", is_flag=True)
def run(
    uri,
    collection,
    path,
    features,
    files_template,
    count_per_file,
    skip,
    limit,
    verbose,
):
    """
    Library exports data from a mongodb to tfrecords files
    """

    if features:
        features = features.split(",")

    from mongo_tfrecords.exporter import export

    export(
        collection=collection,
        database=uri,
        path=path,
        features=features,
        files_template=files_template,
        count_per_file=count_per_file,
        skip=skip,
        limit=limit,
        verbose=verbose,
    )


if __name__ == "__main__":
    run()
