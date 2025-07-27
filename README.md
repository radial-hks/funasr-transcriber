## FunASR Transcriber Plugin for Dify

**Author:** radial
**Version:** 0.0.1
**Type:** Tool

### Description

This plugin integrates FunASR (A Fun-text Autonomous Speech Recognition) into Dify, allowing you to transcribe audio files into text directly within your Dify applications. It utilizes a WebSocket client to communicate with a FunASR server for real-time speech recognition.

### Features

- **Audio Transcription**: Transcribe audio files (WAV, MP3, PCM) into text.
- **Format Conversion**: Automatically converts MP3 files to WAV format for optimal compatibility.
- **Easy Integration**: Seamlessly connect to a running FunASR server.
- **Configurable**: Set the FunASR server host and port via environment variables.
- **Rich Output**: Returns transcription as text, JSON with metadata, and downloadable file.

### Prerequisites

Before using this plugin, you need to have a FunASR server running. You can set one up using Docker:

```bash
sudo docker run -p 10096:10095 -it --privileged=true \
  -v $PWD/funasr-runtime-resources/models:/workspace/models \
  registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-online-cpu-0.1.13
```

This command will start a FunASR server listening on port `10095`.

### Installation & Configuration

1.  **Clone the repository or place the plugin in your Dify `plugins` directory.**

2.  **Create a `.env` file** in the root of the plugin directory by copying the `.env.example` file:

    ```bash
    cp .env.example .env
    ```

3.  **Edit the `.env` file** to configure the connection to your Dify instance and the FunASR server:

    ```dotenv
    # Dify remote installation config
    INSTALL_METHOD=remote
    REMOTE_INSTALL_URL=debug.dify.ai:5003
    REMOTE_INSTALL_PORT=5003
    REMOTE_INSTALL_KEY=your-dify-remote-install-key

    # FunASR Server Configuration
    FUNASR_HOST=localhost
    FUNASR_PORT=10095
    
    # Dify File URL (The URL where Dify can access uploaded files)
    FILES_URL=http://localhost:5003
    ```

    - `REMOTE_INSTALL_KEY`: Your secret key for remote installation in Dify.
    - `FUNASR_HOST`: The hostname or IP address of your FunASR server (defaults to `localhost`).
    - `FUNASR_PORT`: The port of your FunASR server (defaults to `10095`).
    - `FILES_URL`: The base URL that Dify uses to serve files. This is crucial for the plugin to retrieve the audio file for transcription.

4.  **Install the plugin** in Dify through the remote installation method.

### Usage

Once the plugin is installed and configured in Dify:

1.  Go to the **Studio -> Tools** section in Dify.
2.  Find and add the **FunASR Transcriber** tool to your application.
3.  In your application, you can now use the tool by providing an audio file as input.
4.  **Supported formats**: WAV, MP3, PCM (MP3 files will be automatically converted to WAV).
5.  The tool will return:
    - Transcribed text as a string
    - JSON object with detailed information including file metadata
    - Downloadable transcription text file



