# Karaoke Unlimited

<img src="https://img.shields.io/badge/React-18.2.0-darkcyan?style=flat-square&logo=react&logoColor=white"> <img src="https://img.shields.io/badge/jQuery-3.7.1-blue?style=flat-square&logo=jquery&logoColor=white"> <img src="https://img.shields.io/badge/Babel-6.26.0-yellow?style=flat-square&logo=babel&logoColor=white"> <img src="https://img.shields.io/badge/JSX-supported-orange?style=flat-square&logo=react&logoColor=white"> <img src="https://img.shields.io/badge/Flask-3.1.1-lightgrey?style=flat-square&logo=flask&logoColor=white">

![Home Screen](assets/img/homescreen.png)

Karaoke Unlimited (KU) is a free webapp for conducting home Karaoke sessions! Rather than relying on a preset bank of songs to choose from, KU allows you to choose songs from videos on YouTube. Once you choose a video, you can sing along to it on KU, and once finished, KU will offer a score based on how closely your singing matched the video's audio!

To begin using KU, simply navigate back to the main screen and then press "START." Then, enter the link of the YouTube video you want to use on the screen that pops up. KU will then display the video on screen, and whenever you're ready, you can press the record button to begin singing! Once done, simply tap the record button again to finish and receive your score.

## How to Run

1. **Install dependencies:**
   Assuming you have Node installed, open your terminal or command prompt, navigate to the project's root directory, and run the following command:
   ```bash
   npm install
   ```

   You'll also need to [install FFmpeg](https://ffmpeg.org/download.html) and add its executables to your environment PATH.

2. **Build the project:**
   In the same terminal, run the following script. This will watch for changes in the `src` directory and output the built files into the project's root directory.
   ```bash
   npm run build
   ```

3. **Serve the application:**
   Navigate to the project's root directory in your terminal and run:
   ```bash
   run_all.bat
   ```
   This will boot up the lightweight Flask backend at `http://localhost:5000/` and serve the project at `http://localhost:8000/`.

4. **Open the application:**
   Open your web browser and navigate to the address provided by your local HTTP server (e.g., `http://localhost:8000`). You should see `index.html` loaded.
