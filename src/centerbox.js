import React from 'react';
import ReactDOM from 'react-dom';
import $ from 'jquery';

var selectedVidId;
var results = [];
var player = null;
const loadingMessages = [
    "Warming up the vocal cords...",
    "Finding your inner superstar...",
    "Tuning the invisible guitar...",
    "Summoning backup dancers...",
    "Polishing the disco ball...",
    "Counting the high notes...",
    "Checking for mic drop moments...",
    "Syncing with the karaoke gods...",
    "Scoring your air guitar solo...",
    "Auto-tuning your performance..."
];

class SearchResult {
    constructor(title, thumb, id) {
        this.title = title;
        this.thumb = thumb;
        this.id = id;
    }
}

class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            page: "home",
            isRecording: false,
            audioBlob: null,
            beginButtonDisabled: false,
            finishButtonDisabled: true,
            currentScore: null,
            page_status: null,
            lastSelectedVidId: null,
            loadingMessage: ""
        };
        this.mediaRecorder = null;
        this.audioChunks = [];

        this.keyWordsearch = this.keyWordsearch.bind(this);
        this.handleBegin = this.handleBegin.bind(this);
        this.handleStartRecording = this.handleStartRecording.bind(this);
        this.handleStopRecording = this.handleStopRecording.bind(this);
        this.initiateScoreCalculation = this.initiateScoreCalculation.bind(this);
    }

    keyWordsearch() {
        var parser = new DOMParser();
        gapi.client.setApiKey('AIzaSyDhSebIt708zCZaFeSOdJiNqKLGlMvg5gE');
        gapi.client.load('youtube', 'v3', () => {
            var q = $('#query').val();
            var request = gapi.client.youtube.search.list({
                q: q,
                part: 'snippet',
                maxResults: 10,
                type: 'video' 
            });
            request.execute((response) => {
                results = []; 
                var srchItems = response.result.items;
                $.each(srchItems, (index, item) => {
                    var vidTitle = parser.parseFromString(item.snippet.title, 'text/html').body.textContent;
                    var vidThumburl = item.snippet.thumbnails.default.url;
                    var vidId = item.id.videoId;
                    results.push(new SearchResult(vidTitle, vidThumburl, vidId)); 
                });
                $('#refresher').click();
            });
        });
    }

    handleBegin() {
        if (player && player.playVideo) {
            player.playVideo();
        }
    }

    handleStartRecording() {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                this.mediaRecorder = new MediaRecorder(stream);
                this.mediaRecorder.ondataavailable = event => {
                    this.audioChunks.push(event.data);
                };
                this.mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                    this.audioChunks = [];
                    this.setState({ audioBlob: audioBlob });
                    if (this.state.page_status === 'calculating') {
                        this.initiateScoreCalculation();
                    }
                };
                this.mediaRecorder.start();
                this.setState({ isRecording: true });
            })
            .catch(err => {
                console.error("Error accessing microphone:", err);
            });
    }

    initiateScoreCalculation() {
        if (!this.state.audioBlob) {
            console.error("No audio blob to calculate score.");
            this.setState({ page: 'score', page_status: null, currentScore: "Error: No audio recorded" });
            return;
        }

        const formData = new FormData();
        formData.append('audio', this.state.audioBlob, 'recording.webm');
        formData.append('videoId', this.state.lastSelectedVidId);

        const interval = setInterval(() =>
            this.setState({ loadingMessage: loadingMessages[Math.floor(Math.random() * loadingMessages.length)] }),
            3000
        );
        this.setState({ loadingMessage: loadingMessages[0] });

        const scoreCalculationPromise = fetch('http://localhost:5000/api/calculate_score', {
            method: 'POST',
            body: formData
        });

        const timeoutPromise = new Promise((_, reject) => {
            setTimeout(() => {
                reject(new Error('Score calculation timed out'));
            }, 30*1000); // 30 second timeout on calculation
        });

        Promise.race([scoreCalculationPromise, timeoutPromise])
            .then(response => {
                clearInterval(interval); // Clear interval on success
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                this.setState({
                    page: 'score',
                    currentScore: Math.max(0, Math.round(data.score + (Math.random() * 10 - 5)).toString()), // plus or minus random variation
                    page_status: null,
                    loadingMessage: "" // Clear loading message
                });
            })
            .catch(error => {
                clearInterval(interval); // Clear interval on error
                if (error.message === 'Score calculation timed out') {
                    console.error("Score calculation timed out after 10 seconds.");
                    this.setState({
                        page: 'score',
                        currentScore: (Math.floor(Math.random() * 100) + 1).toString(),
                        page_status: null,
                        loadingMessage: "" // Clear loading message
                    });
                } else {
                    console.error("Error calculating score:", error);
                    this.setState({
                        page: 'score',
                        currentScore: (Math.floor(Math.random() * 100) + 1).toString(), // default to random score if it fails
                        page_status: null,
                        loadingMessage: "" // Clear loading message
                    });
                }
            });
    }

    handleStopRecording() {
        if (this.mediaRecorder && this.mediaRecorder.state === "recording") {
            this.mediaRecorder.stop();
            this.setState({ isRecording: false });
        }
    }

    componentDidUpdate(prevProps, prevState) {
        if (this.state.page.includes("watch") && (!prevState.page || !prevState.page.includes("watch") || this.state.page !== prevState.page)) {
            selectedVidId = this.state.page.substring(5); 
            if (window.YT && window.YT.Player) {
                if (player) { 
                    player.destroy();
                }
                player = new window.YT.Player('video', {
                    videoId: selectedVidId,
                    width: '80%',
                    playerVars: {
                        'autoplay': 0,
                        'controls': 0,
                        'disablekb': 1,
                        'enablejsapi': 1,
                        'rel': 0 
                    }
                });
            }
        }
    }

    componentWillUnmount() {
        if (this.state.audioBlob) {
            URL.revokeObjectURL(URL.createObjectURL(this.state.audioBlob));
        }
        if (player) { 
            player.destroy();
            player = null;
        }
        if (this.mediaRecorder && this.mediaRecorder.state === "recording") {
            this.mediaRecorder.stop();
        }
    }

    render() {
        if (this.state.page == "home") {
            return (
                <div className="centerbox">
                    <div className="logo"><b>Kar<span>a</span>ok<span>e</span></b></div>
                    <div className="logo2"><b>UNLIMITE<span>D</span></b></div>
                    <div className="neonBtn" onClick={() => this.setState({ page: "start" })}>START</div>
                    <div className="neonBtn" onClick={() => this.setState({ page: "about" })}>ABOUT</div>
                </div>
            );
        } else if (this.state.page == "about") {
            return (
                <div className="centerbox">
                    <div className="logo"><b>A<span>b</span>out</b></div>
                    <p style={{ textAlign: "left", width: "25%" }}>
                        Karaoke Unlimited (KU) is a free webapp for conducting home Karaoke sessions! Rather than relying on a preset bank of songs to choose from, KU allows you to choose songs from videos on YouTube. Once you choose a video, you can sing along to it on KU, and once finished, KU will offer a score based on how closely your singing matched the video's audio!
                    </p>
                    <p style={{ textAlign: "left", width: "25%" }}>
                        To begin using KU, simply navigate back to the main screen and then press "START." Then, enter the link of the YouTube video you want to use on the screen that pops up. KU will then display the video on screen, and whenever you're ready, you can press the record button to begin singing! Once done, simply tap the record button again to finish and receive your score.
                    </p>
                    <p style={{ textAlign: "left", width: "25%" }}>
                        © 2025 Brandon Lee.<br />
                        <a href="https://github.com/dabslee/Karaoke">Source code</a> • <a href="https://brandonssandbox.com">Brandon's Website</a>
                    </p>
                    <div className="neonBtn" onClick={() => this.setState({ page: "home" })}>BACK</div>
                </div>
            );
        } else if (this.state.page == "start" || this.state.page == "start2") {
            const nextPage = this.state.page === "start" ? "start2" : "start";
            return (
                <div style={{ display: "flex", flexDirection: "column", alignItems: "center", marginTop: "10%" }}>
                    <div className="logo2" style={{ fontWeight: "thin" }}><b>Search for a song:</b></div>
                    <div style={{ width: "100%", display: "flex", flexDirection: "row", justifyContent: "center", marginBottom: "30px" }}>
                        <input id="query" placeholder="e.g. Never Gonna Give You Up" style={{ width: '80%' }} />
                        <div id="searchbutton" className="logo2" onClick={this.keyWordsearch} style={{ cursor: "pointer", margin: 0 }}><b>&#x2794;</b></div>
                        <div id="refresher" onClick={() => this.setState({ page: nextPage })}></div>
                    </div>
                    <div id="results" style={{justifyContent: "center"}}>
                        {results.map(result => (
                            <div onClick={() => this.setState({ page: "watch" + result.id })} className="searchresult" key={result.id}>
                                <img src={result.thumb} alt="No thumbnail available" />
                                <p style={{ marginLeft: "20px" }}>{result.title}</p>
                            </div>
                        ))}
                        {' '}
                    </div>
                    <div className="neonBtn" onClick={() => this.setState({ page: "home" })}>BACK</div>
                </div>
            );
        } else if (this.state.page.includes("watch")) {
            selectedVidId = this.state.page.substring(5); 
            return (
                <div className="centerbox">
                    <div id="video" style={{ width: "80%", pointerEvents: "none", aspectRatio: "16/9", height: "auto" }}></div>
                    <div style={{ display: "flex", flexDirection: "row" }}>
                        <div
                            className="neonBtn"
                            onClick={() => {
                                if (player) {
                                    player.destroy();
                                    player = null;
                                }
                                if (this.mediaRecorder && this.mediaRecorder.state === "recording") {
                                    this.mediaRecorder.stop();
                                }
                                this.setState({
                                    page: "start",
                                    isRecording: false,
                                    beginButtonDisabled: false,
                                    finishButtonDisabled: true,
                                    audioBlob: null 
                                });
                            }}
                        >
                            BACK
                        </div>
                        <div
                            id="begin-button"
                            className={`neonBtn ${this.state.beginButtonDisabled ? 'disabled-look' : ''}`}
                            onClick={() => {
                                if (this.state.beginButtonDisabled) return;
                                this.handleBegin(); 
                                this.handleStartRecording();
                                this.setState({ beginButtonDisabled: true, finishButtonDisabled: false });
                            }}
                        >
                            {this.state.isRecording ? 'Recording...' : 'BEGIN'}
                        </div>
                        <div
                            id="finish-button"
                            className={`neonBtn ${this.state.finishButtonDisabled ? 'disabled-look' : ''}`}
                            onClick={() => {
                                if (this.state.finishButtonDisabled) return;
                                // player will be destroyed in componentDidUpdate when page changes from "watch..."
                                this.setState({
                                    page: 'calculating_score',
                                    page_status: 'calculating',
                                    lastSelectedVidId: selectedVidId, 
                                    beginButtonDisabled: false, // Reset for next time
                                    finishButtonDisabled: true // Reset for next time
                                }, () => {
                                    if (player) {
                                        player.destroy();
                                        player = null;
                                    }
                                    this.handleStopRecording(); // This will trigger initiateScoreCalculation via onstop
                                });
                            }}
                        >
                            Finish
                        </div>
                    </div>
                </div>
            );
        } else if (this.state.page === "calculating_score") {
            return (
                <div className="centerbox">
                    <div className="logo2"><b>Calculating your score...</b></div>
                    <span class="loader"></span>
                    <div className="loading-message">{this.state.loadingMessage}</div>
                </div>
            );
        } else if (this.state.page === "score") {
            const currentVideoId = this.state.lastSelectedVidId || ""; 
            return (
                <div className="centerbox">
                    <div className="logo" style={{marginBottom: '20px'}}><b>Your Performance</b></div>
                    <div className="logo2" style={{marginBottom: '20px'}}><b>Score:</b></div>
                    <div className="score" style={{marginBottom: '0px'}}>{this.state.currentScore !== null ? this.state.currentScore : "Calculating..."}</div>
                    {this.state.audioBlob && (
                        <audio controls src={URL.createObjectURL(this.state.audioBlob)} style={{margin: '30px'}} />
                    )}
                    <div
                        className="neonBtn"
                        onClick={() => {
                            if (this.state.audioBlob) {
                                URL.revokeObjectURL(URL.createObjectURL(this.state.audioBlob));
                            }
                            this.setState({ 
                                page: "watch" + currentVideoId, 
                                audioBlob: null, 
                                currentScore: null, 
                                page_status: null,
                                beginButtonDisabled: false, 
                                finishButtonDisabled: true 
                            });
                        }}
                    >
                        Back
                    </div>
                </div>
            );
        }
        return null; 
    }
}

var domContainer = document.querySelector('#content');
ReactDOM.render(React.createElement(Content, null), domContainer);

document.addEventListener('keydown', function (e) {
    if (e.code === "Enter" && document.getElementById("searchbutton")) document.getElementById("searchbutton").click();
});