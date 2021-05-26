var selectedVidId;
var results = [];

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
        this.state = {page: "home"};
        this.keyWordsearch = this.keyWordsearch.bind(this);
    }

    keyWordsearch = () => {
        gapi.client.setApiKey('AIzaSyDhSebIt708zCZaFeSOdJiNqKLGlMvg5gE');
        gapi.client.load('youtube', 'v3', function(){
            var q = $('#query').val();
            var request = gapi.client.youtube.search.list({
                q: q,
                part: 'snippet',
                maxResults: 10
            });
            request.execute(function(response) {
                results = [];
                var srchItems = response.result.items;
                $.each(srchItems, function(index, item){
                    var vidTitle = item.snippet.title;
                    var vidThumburl =  item.snippet.thumbnails.default.url;
                    var vidId = item.id.videoId;
                    results.push(new SearchResult(vidTitle, vidThumburl, vidId));
                });
                $('#refresher').click();
            });
        });
    }

    render() {
        if (this.state.page == "home") {
            return (
                <div class="centerbox">
                    <div class="logo"><b>Kar<span>a</span>ok<span>e</span></b></div>
                    <div class="logo2"><b>UNLIMITE<span>D</span></b></div>
                    <div class="neonBtn" onClick={() => this.setState({page : "start"})}>START</div>
                    <div class="neonBtn" onClick={() => this.setState({page : "about"})}>ABOUT</div>
                </div>
            );
        } else if (this.state.page == "about") {
            return (
                <div class="centerbox">
                    <div class="logo"><b>A<span>b</span>out</b></div>
                    <p style={{textAlign:"left", width:"25%"}}>
                        Karaoke Unlimited (KU) is a free webapp for conducting home Karaoke sessions! Rather than relying on a preset bank of songs to choose from, KU allows you to choose songs from videos on YouTube. Once you choose a video, you can sing along to it on KU, and once finished, KU will offer a score based on how closely your singing matched the video's audio!
                    </p>
                    <p style={{textAlign:"left", width:"25%"}}>
                        To begin using KU, simply navigate back to the main screen and then press "START." Then, enter the link of the YouTube video you want to use on the screen that pops up. KU will then display the video on screen, and whenever you're ready, you can press the record button to begin singing! Once done, simply tap the record button again to finish and receive your score.
                    </p>
                    <p style={{textAlign:"left", width:"25%"}}>
                        KU was made in May 2021 by Brandon Lee.<br/>
                        <a href="github.com/dabslee/Karaoke">Source code</a> • <a href="brandonssandbox.com">Brandon's Website</a>
                    </p>
                    <div class="neonBtn" onClick={() => this.setState({page : "home"})}>BACK</div>
                </div>
            );
        } else if (this.state.page == "start") {
            var searchresults = [];
            for (let result of results) {
                searchresults.push(
                    <div onClick={() => this.setState({page : "watch" + result.id})} class="searchresult">
                        <img src={result.thumb} alt="No thumbnail available"/>
                        <p style={{marginLeft: "20px"}}>{result.title}</p>
                    </div>
                );
            }
            return (
                <div style={{display:"flex",flexDirection:"column",alignItems:"center",marginTop:"10%"}}>
                    <div class="logo2" style={{fontWeight:"thin"}}><b>Search for a song:</b></div>
                    <div style={{width:"100%", display:"flex", flexDirection:"row", justifyContent:"center", marginBottom:"30px"}}>
                        <input id="query" placeholder="e.g. Never Gonna Give You Up"></input>
                        <div id="searchbutton" class="logo2" onClick={this.keyWordsearch} style={{cursor:"pointer", margin:0}}><b>➜</b></div>
                        <div id="refresher" onClick={() => this.setState({page : "start2"})}></div>
                    </div>
                    <div id="results" style={{display:"flex", flexDirection:"column", marginBottom:"30px"}}>{searchresults}</div>
                </div>
            );
        } else if (this.state.page == "start2") {
            var searchresults = [];
            for (let result of results) {
                searchresults.push(
                    <div onClick={() => this.setState({page : "watch" + result.id})} class="searchresult">
                        <img src={result.thumb} alt="No thumbnail available"/>
                        <p style={{marginLeft: "20px"}}>{result.title}</p>
                    </div>
                );
            }
            return (
                <div style={{display:"flex",flexDirection:"column",alignItems:"center",marginTop:"10%"}}>
                    <div class="logo2" style={{fontWeight:"thin"}}><b>Search for a song:</b></div>
                    <div style={{width:"100%", display:"flex", flexDirection:"row", justifyContent:"center", marginBottom:"30px"}}>
                        <input id="query" placeholder="e.g. Never Gonna Give You Up"></input>
                        <div id="searchbutton" class="logo2" onClick={this.keyWordsearch} style={{cursor:"pointer", margin:0}}><b>➜</b></div>
                        <div id="refresher" onClick={() => this.setState({page : "start2"})}></div>
                    </div>
                    <div id="results" style={{display:"flex", flexDirection:"column", marginBottom:"30px"}}>{searchresults}</div>
                </div>
            );
        } else if (this.state.page.includes("watch")) {
            let link = "http://www.youtube.com/embed/" + this.state.page.substring(5) + "?enablejsapi=1&disablekb=1";
            return (
                <div class="centerbox">
                    <iframe id="video" width="1000" height="500" style={{pointerEvents:"none"}}
                        src={link}>
                    </iframe>
                    <div style={{display:"flex", flexDirection:"row"}}>
                        <div class="neonBtn" onClick={() => this.setState({page : "start"})}>BACK</div>
                        <div id="begin-button" class="neonBtn" onClick={() => $('#video')[0].contentWindow.postMessage('{"event":"command","func":"' + 'playVideo' + '","args":""}', '*')}>BEGIN</div>
                    </div>
                </div>
            );
        }
    }
}

const domContainer = document.querySelector('#content');
ReactDOM.render(React.createElement(Content), domContainer);

document.addEventListener('keydown', (e) => {
    if (e.code === "Enter" && document.getElementById("searchbutton"))
        document.getElementById("searchbutton").click();
});