import asyncio
import os
import io
from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.file.file import File as DifyFile
from dify_plugin.entities.tool import ToolInvokeMessage
from pydub import AudioSegment

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
        
        # Convert MP3 to WAV if necessary
        file_extension = getattr(dify_file, 'extension', '').lower()
        # if file_extension == '.mp3' or (hasattr(dify_file, 'mime_type') and dify_file.mime_type == 'audio/mpeg'):
        if file_extension == '.mp3':
            try:
                # Load MP3 audio from bytes
                audio_segment = AudioSegment.from_mp3(io.BytesIO(audio_bytes))
                audio_segment = audio_segment.set_frame_rate(16000).set_channels(1).set_sample_width(2)  # 16-bit PCM
                # Convert to WAV format
                wav_buffer = io.BytesIO()
                audio_segment.export(wav_buffer, format="wav")
                audio_bytes = wav_buffer.getvalue()
                yield self.create_text_message("已将MP3文件转换为WAV格式")
            except Exception as e:
                yield self.create_text_message(f"音频格式转换失败: {e}")
                # return

        # Run transcription
        try:
            result = asyncio.run(transcribe(audio_bytes, funasr_host, funasr_port))
            # 1. Yield the primary result as a text message for direct display
            # yield self.create_text_message(result)

            # 2. Yield a JSON object with more detailed information
            yield self.create_json_message({
                "transcription": result,
                "engine": "funasr",
                "server_host": funasr_host,
                "input_file": {
                    "url": getattr(dify_file, 'url', ''),
                    "mime_type": getattr(dify_file, 'mime_type', None),
                    "filename": getattr(dify_file, 'filename', None),
                    "extension": getattr(dify_file, 'extension', None),
                    "size": getattr(dify_file, 'size', None),
                    "type": str(getattr(dify_file, 'type', 'unknown'))
                }
            })

            # 3. Yield the transcription as a downloadable text file
            # transcription_bytes = result.encode('utf-8')
            # yield self.create_blob_message(blob=transcription_bytes, 
            #                             meta={'mime_type': 'text/plain', 'file_name': 'transcription.txt'})

        except Exception as e:
            yield self.create_text_message(f"Transcription failed: {e}")
