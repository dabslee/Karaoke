# Karaoke Project

<img src="https://img.shields.io/badge/-darkcyan?style=flat-square&logo=react&logoColor=white">
<img src="https://img.shields.io/badge/-blue?style=flat-square&logo=jquery&logoColor=white">
<img src="https://img.shields.io/badge/-yellow?style=flat-square&logo=babel&logoColor=white">

Karaoke Unlimited (KU) is a free webapp for conducting home Karaoke sessions! Rather than relying on a preset bank of songs to choose from, KU allows you to choose songs from videos on YouTube. Once you choose a video, you can sing along to it on KU, and once finished, KU will offer a score based on how closely your singing matched the video's audio!

To begin using KU, simply navigate back to the main screen and then press "START." Then, enter the link of the YouTube video you want to use on the screen that pops up. KU will then display the video on screen, and whenever you're ready, you can press the record button to begin singing! Once done, simply tap the record button again to finish and receive your score.

## How to Run

1. **Install dependencies:**
   Open your terminal or command prompt, navigate to the project's root directory, and run the following command:
   ```bash
   npm install
   ```

2. **Build the project:**
   In the same terminal, run the following script. This will watch for changes in the `src` directory and output the built files into the project's root directory.
   ```bash
   ./babelrun.sh
   ```
   (If you are on Windows, you might need to run it using a bash-like shell like Git Bash, or execute the command within `babelrun.sh` directly: `npx babel --watch src --out-dir . --presets react-app/prod`)

3. **Serve the application:**
   To avoid potential CORS (Cross-Origin Resource Sharing) errors when running the application directly from the file system, it's best to serve it using a local HTTP server.

   **Using Python's built-in server (if you have Python installed):**
   Navigate to the project's root directory in your terminal and run:
   ```bash
   # For Python 3
   python -m http.server
   # For Python 2
   python -m SimpleHTTPServer
   ```
   This will typically serve the project at `http://localhost:8000/`.

4. **Open the application:**
   Open your web browser and navigate to the address provided by your local HTTP server (e.g., `http://localhost:8000`). You should see `index.html` loaded.
