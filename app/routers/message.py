from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from app.utils.function_handlers import handle_tool_outputs
from app.core.openai import client
from app.core.config import settings
from app.core.logger import logging
from typing import Dict, Any
from pydantic import BaseModel
import json
from openai import AssistantEventHandler
from typing_extensions import override
import asyncio

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


@router.post("/stream")
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


async def check_status(thread_id: str, run_id: str):
    """
    Periodically check the status of the assistant run and handle actions or completion.

    Args:
        thread_id (str): The thread ID.
        run_id (str): The run ID.
    """
    try:
        while True:
            run_object = client.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run_id
            )
            status = run_object.status
            logger.info(f"Current status: {status}")

            if status == "completed":
                logger.info("Run completed. Fetching messages...")
                messages_list = client.beta.threads.messages.list(thread_id=thread_id)

                logger.debug(f"Messages list: {messages_list}")

                messages = [
                    {
                        "runId": message.run_id,
                        "msgId": message.id,
                        "thread_id": message.thread_id,
                        "role": message.role,
                        "createdAt": message.created_at,
                        "messageText": (
                            message.content[0].text.value if message.content else None
                        ),
                    }
                    for message in messages_list.data[::-1]  # Access data directly
                ]

                return {"status": "completed", "messages": messages}

            elif status == "requires_action":
                logger.info("Run requires action. Handling required actions...")
                required_actions = (
                    run_object.required_action.submit_tool_outputs.tool_calls
                )

                tools_output = []

                for action in required_actions:
                    func_name = action.function.name
                    function_arguments = json.loads(action.function.arguments)

                    try:
                        output = await handle_tool_outputs(
                            func_name, function_arguments
                        )
                        logger.info(f"Output of handleToolOutputs: {output}")
                        tools_output.append(
                            {
                                "tool_call_id": action.id,
                                "output": json.dumps(output),
                            }
                        )
                    except Exception as e:
                        logger.error(f"Error in handleToolOutputs: {str(e)}")
                        tools_output.append(
                            {
                                "tool_call_id": action.id,
                                "output": json.dumps({"error": str(e)}),
                            }
                        )

                # Submit the tool outputs to the Assistant API
                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=run_id,
                    tool_outputs=tools_output,
                )

            await asyncio.sleep(3)  # Poll every 3 seconds

    except Exception as e:
        logger.error(f"Error in check_status: {str(e)}")
        raise HTTPException(status_code=500, detail="Error checking status")


@router.post("/")
async def create_message_with_polling(request: MessageRequest):
    """
    Create a user message and start polling for assistant run status.

    Args:
        request (MessageRequest): The request body containing message and threadId.

    Returns:
        dict: The final status and messages after completion.
    """
    try:
        # Extract message and threadId from the request body
        message = request.message
        thread_id = request.threadId

        # Create the user message in the thread
        client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=message
        )
        logger.info(f"User message created in thread {thread_id}")

        # Start the assistant run
        response = client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=settings.assistant_id
        )
        run_id = response.id
        logger.info(f"Assistant run started with run ID: {run_id}")

        # Poll for status and return the result
        result = await check_status(thread_id, run_id)
        return result

    except Exception as e:
        logger.error(f"Error creating message with polling: {e}")
        raise HTTPException(status_code=500, detail=str(e))
