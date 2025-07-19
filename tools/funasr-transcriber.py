import asyncio
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.file.file import File as DifyFile
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.client import transcribe

class FunasrTranscriberTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # Get the uploaded file
        dify_file: DifyFile = tool_parameters['audiofile']

        # Read file content
        audio_bytes = dify_file.blob

        # Get credentials
        # self.runtime.credentials['funasr_host']
        funasr_host = self.runtime.credentials['funasr_host']
        funasr_port = self.runtime.credentials['funasr_port']

        # Run transcription
        try:
            result = asyncio.run(transcribe(audio_bytes, funasr_host, funasr_port))
            yield self.create_json_message({"text": result})
        except Exception as e:
            yield self.create_text_message(f"Transcription failed: {e}")
