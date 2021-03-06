#!/usr/bin/env python3.4
#
# Copyright (c) 2013-2014 by Ron Frederick <ronf@timeheart.net>.
# All rights reserved.
#
# This program and the accompanying materials are made available under
# the terms of the Eclipse Public License v1.0 which accompanies this
# distribution and is available at:
#
#     http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
#     Ron Frederick - initial implementation, API, and documentation

import asyncio, asyncssh, sys

class MySSHClientSession(asyncssh.SSHClientSession):
    def next_operation(self):
        if self._operations:
            operation = self._operations.pop(0)
            print(operation, '= ', end='')
            self._chan.write(operation + '\n')
        else:
            self._chan.write_eof()

    def connection_made(self, chan):
        self._chan = chan

    def session_started(self):
        self._operations = ['2+2', '1*2*3*4', '2^32']
        self.next_operation()

    def data_received(self, data, datatype):
        print(data, end='')

        if '\n' in data:
            self.next_operation()

    def connection_lost(self, exc):
        if exc:
            print('SSH session error: ' + str(exc), file=sys.stderr)

@asyncio.coroutine
def run_client():
    conn, client = yield from asyncssh.create_connection(None, 'localhost')
    chan, session = yield from conn.create_session(MySSHClientSession, 'bc')
    yield from chan.wait_closed()
    conn.close()

try:
    asyncio.get_event_loop().run_until_complete(run_client())
except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))
