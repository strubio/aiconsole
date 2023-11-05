# The AIConsole Project
#
# Copyright 2023 10Clouds
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
    
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from aiconsole import projects

from aiconsole.websockets import connection_manager
from aiconsole.websockets.handle_incoming_message import handle_incoming_message

router = APIRouter()

_log = logging.getLogger(__name__)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    connection = await connection_manager.connect(websocket)
    await projects.send_project_init(connection)

    try:
        while True:
            json_data = await websocket.receive_json()
            await handle_incoming_message(connection, json_data)
    except WebSocketDisconnect:
        connection_manager.disconnect(connection)