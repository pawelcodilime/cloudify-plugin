########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.


# ctx is imported and used in operations
import os

from cloudify import ctx
from cloudify.decorators import operation


@operation
def start_server(**kwargs):
    path = ctx.node.properties['path']
    port = ctx.node.properties['port']

    command = (
        'cd {}; nohup python -m SimpleHTTPServer {}> /dev/null 2>&1'
        ' & echo $! > /tmp/python-webserver.pid'
    ).format(path, port)

    ctx.logger.info('Starting HTTP server using: {0}'.format(command))
    os.system(command)


@operation
def stop_server(**kwargs):
    with open('/tmp/python-webserver.pid') as f:
        pid = f.read()

    try:
        ctx.logger.info('Server stopped.')
        os.kill(int(pid), 9)
    except OSError:
        ctx.logger.info('Server is already not running.')
