#### **Step 1: Clone the Repository**

1. Open a terminal or command prompt.
2. Run the following command to clone the repository:

   ```bash
   git clone https://github.com/arzumanabbasov/voice-api-bugra.git
   ```

3. Navigate into the cloned repository:

   ```bash
   cd voice-api-bugra
   ```

---

#### **Step 2: Create and Activate a Virtual Environment**

**Linux:**
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

**Windows:**
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
   ```

---

#### **Step 3: Install Required Dependencies**

1. Install dependencies listed in the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

---

#### **Step 4: (Optional) Install FFmpeg for Audio Processing**

**Why FFmpeg is Needed:**
The `pydub` library uses FFmpeg for audio processing. While it's not mandatory for the basic transcription functionality, you may encounter errors if FFmpeg is not installed.

**Linux:**
1. Install FFmpeg using your package manager:
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

2. Verify installation:
   ```bash
   ffmpeg -version
   ```

**Windows:**
1. Download FFmpeg from the gyan.dev website: [FFmpeg Download](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z).
2. Extract the files to a folder (e.g., `C:\ffmpeg`).
3. Add the `bin` directory (e.g., `C:\ffmpeg\bin`) to your system's `PATH` environment variable:
   - Search for "Environment Variables" in the Start Menu.
   - Under "System Variables," find `Path` and click "Edit."
   - Add the full path to the `bin` folder and click "OK."
4. Verify installation:
   ```bash
   ffmpeg -version
   ```

**What Happens Without FFmpeg:**
If FFmpeg is not installed, you may encounter errors when processing certain audio formats. WAV files should still work without it.

---

#### **Step 5: Run the Flask Application**

1. Start the Flask server by running the following command:
   ```bash
   python app.py
   ```

2. The server will start on `http://127.0.0.1:5000` (default Flask port).

---

#### **Step 6: Test the API**

1. Use tools like **Postman** or **cURL** to test the `/upload` endpoint:
   - Upload an audio file to `http://127.0.0.1:5000/upload` using the `POST` method.
   - Ensure the file is in a supported audio format (e.g., WAV).

   **Example cURL Command:**
   ```bash
   curl -X POST -F "file=@path_to_audio_file.wav" http://127.0.0.1:5000/upload
   ```

2. The response will include the segmented transcription and details.
