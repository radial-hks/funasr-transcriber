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
            
            # 1. Yield the primary result as a text message for direct display
            yield self.create_text_message(result)

            # 2. Yield a JSON object with more detailed information
            yield self.create_json_message({
                "transcription": result,
                "engine": "funasr",
                "server_host": funasr_host
            })

            # 3. Yield the transcription as a downloadable text file
            # transcription_bytes = result.encode('utf-8')
            # yield self.create_blob_message(blob=transcription_bytes, 
            #                             meta={'mime_type': 'text/plain', 'file_name': 'transcription.txt'})

        except Exception as e:
            yield self.create_text_message(f"Transcription failed: {e}")
