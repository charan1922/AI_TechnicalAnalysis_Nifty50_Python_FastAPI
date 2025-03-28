from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from app.core.openai import client
from app.core.config import settings
from app.core.logger import logging
from typing import Dict, Any
from pydantic import BaseModel
import json
from openai import AssistantEventHandler
from typing_extensions import override

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/message", tags=["messages"])


class EventHandler(AssistantEventHandler):
    """Custom event handler for processing assistant events."""

    def __init__(self):
        self.events = []

    @override
    def on_text_created(self, text) -> None:
        self.events.append(
            f"data: {json.dumps({'role': 'assistant', 'messageText': ''})}\n\n"
        )

    @override
    def on_text_delta(self, delta, snapshot):
        self.events.append(f"data: {json.dumps({'messageText': delta.value})}\n\n")

    @override
    def on_tool_call_created(self, tool_call):
        self.events.append(
            f"data: {json.dumps({'role': 'assistant', 'messageText': tool_call.type})}\n\n"
        )

    @override
    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == "code_interpreter":
            if delta.code_interpreter.input:
                self.events.append(
                    f"data: {json.dumps({'messageText': delta.code_interpreter.input})}\n\n"
                )
            if delta.code_interpreter.outputs:
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        self.events.append(
                            f"data: {json.dumps({'messageText': output.logs})}\n\n"
                        )

    def get_events(self):
        """Retrieve all accumulated events."""
        while self.events:
            yield self.events.pop(0)


async def stream_assistant_response(thread_id: str, assistant_id: str):
    """Stream assistant responses using the custom event handler."""
    event_handler = EventHandler()
    try:
        with client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            event_handler=event_handler,
        ) as stream:
            stream.until_done()
            async for event in event_handler.get_events():
                yield event
    except Exception as e:
        logger.error(f"Streaming error: {str(e)}")
        yield f"data: {json.dumps({'error': 'Streaming failed'})}\n\n"


class MessageRequest(BaseModel):
    message: str
    threadId: str


@router.post("/")
async def create_message_stream(request: MessageRequest):
    try:
        # Extract message and threadId from the request body
        message = request.message
        threadId = request.threadId

        # Create the user message in the thread
        msg = client.beta.threads.messages.create(
            thread_id=threadId, role="user", content=message
        )
        logger.info(f"User message created in thread {threadId}")

        # headers = {
        #     "Content-Type": "text/event-stream",
        #     "Cache-Control": "no-cache",
        #     "Connection": "keep-alive",
        # }
        # Return a StreamingResponse
        return StreamingResponse(
            stream_assistant_response(threadId, assistant_id=settings.assistant_id),
            # headers=headers,
            media_type="text/event-stream",
        )

    except Exception as e:
        # Handle errors gracefully
        logger.error(f"Error creating message stream: {e}")
        raise HTTPException(status_code=500, detail=str(e))
