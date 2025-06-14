var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

import React from 'react';
import ReactDOM from 'react-dom';
import $ from 'jquery';

// Babel helper functions - should remain if not directly involved in JSX transformation
var _createClass = function () {
    function defineProperties(target, props) {
        for (var i = 0; i < props.length; i++) {
            var descriptor = props[i];descriptor.enumerable = descriptor.enumerable || false;descriptor.configurable = true;if ("value" in descriptor) descriptor.writable = true;Object.defineProperty(target, descriptor.key, descriptor);
        }
    }return function (Constructor, protoProps, staticProps) {
        if (protoProps) defineProperties(Constructor.prototype, protoProps);if (staticProps) defineProperties(Constructor, staticProps);return Constructor;
    };
}();
function _possibleConstructorReturn(self, call) {
    if (!self) {
        throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
    }return call && ((typeof call === 'undefined' ? 'undefined' : _typeof(call)) === "object" || typeof call === "function") ? call : self;
}
function _inherits(subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) {
        throw new TypeError("Super expression must either be null or a function, not " + (typeof superClass === 'undefined' ? 'undefined' : _typeof(superClass)));
    }subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } });if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
}
function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
        throw new TypeError("Cannot call a class as a function");
    }
}

var selectedVidId;
var results = [];
var player = null;

// This class seems to be a data structure, not a React component. No JSX needed.
var SearchResult = function SearchResult(title, thumb, id) {
    _classCallCheck(this, SearchResult);
    this.title = title;
    this.thumb = thumb;
    this.id = id;
};

var Content = function (_React$Component) {
    _inherits(Content, _React$Component);

    function Content(props) {
        _classCallCheck(this, Content);
        var _this = _possibleConstructorReturn(this, (Content.__proto__ || Object.getPrototypeOf(Content)).call(this, props));

        _this.keyWordsearch = function () {
            var parser = new DOMParser();
            gapi.client.setApiKey('AIzaSyDhSebIt708zCZaFeSOdJiNqKLGlMvg5gE');
            gapi.client.load('youtube', 'v3', function () {
                var q = $('#query').val();
                var request = gapi.client.youtube.search.list({
                    q: q,
                    part: 'snippet',
                    maxResults: 10
                });
                request.execute(function (response) {
                    results = [];
                    var srchItems = response.result.items;
                    $.each(srchItems, function (index, item) {
                        var vidTitle = parser.parseFromString(item.snippet.title, 'text/html').body.textContent;
                        console.log(vidTitle);
                        var vidThumburl = item.snippet.thumbnails.default.url;
                        var vidId = item.id.videoId;
                        results.push(new SearchResult(vidTitle, vidThumburl, vidId));
                    });
                    $('#refresher').click(); // This might need to trigger a state update if UI depends on `results`
                });
            });
        };

        _this.handleBegin = function () {
            if (player && player.playVideo) player.playVideo();
        };

        _this.state = { page: "home" };
        _this.keyWordsearch = _this.keyWordsearch.bind(_this); // keyWordsearch binding is fine
        return _this;
    }

    _createClass(Content, [{
        key: 'render',
        value: function render() {
            var _this2 = this; // Used in onClick handlers

            if (this.state.page == "home") {
                return React.createElement(
                    'div',
                    { className: 'centerbox' },
                    React.createElement(
                        'div',
                        { className: 'logo' },
                        React.createElement(
                            'b',
                            null,
                            'Kar',
                            React.createElement(
                                'span',
                                null,
                                'a'
                            ),
                            'ok',
                            React.createElement(
                                'span',
                                null,
                                'e'
                            )
                        )
                    ),
                    React.createElement(
                        'div',
                        { className: 'logo2' },
                        React.createElement(
                            'b',
                            null,
                            'UNLIMITE',
                            React.createElement(
                                'span',
                                null,
                                'D'
                            )
                        )
                    ),
                    React.createElement(
                        'div',
                        { className: 'neonBtn', onClick: function onClick() {
                                return _this2.setState({ page: "start" });
                            } },
                        'START'
                    ),
                    React.createElement(
                        'div',
                        { className: 'neonBtn', onClick: function onClick() {
                                return _this2.setState({ page: "about" });
                            } },
                        'ABOUT'
                    )
                );
            } else if (this.state.page == "about") {
                return React.createElement(
                    'div',
                    { className: 'centerbox' },
                    React.createElement(
                        'div',
                        { className: 'logo' },
                        React.createElement(
                            'b',
                            null,
                            'A',
                            React.createElement(
                                'span',
                                null,
                                'b'
                            ),
                            'out'
                        )
                    ),
                    React.createElement(
                        'p',
                        { style: { textAlign: "left", width: "25%" } },
                        'Karaoke Unlimited (KU) is a free webapp for conducting home Karaoke sessions! Rather than relying on a preset bank of songs to choose from, KU allows you to choose songs from videos on YouTube. Once you choose a video, you can sing along to it on KU, and once finished, KU will offer a score based on how closely your singing matched the video\'s audio!'
                    ),
                    React.createElement(
                        'p',
                        { style: { textAlign: "left", width: "25%" } },
                        'To begin using KU, simply navigate back to the main screen and then press "START." Then, enter the link of the YouTube video you want to use on the screen that pops up. KU will then display the video on screen, and whenever you\'re ready, you can press the record button to begin singing! Once done, simply tap the record button again to finish and receive your score.'
                    ),
                    React.createElement(
                        'p',
                        { style: { textAlign: "left", width: "25%" } },
                        '\xA9 2025 Brandon Lee.',
                        React.createElement('br', null),
                        React.createElement(
                            'a',
                            { href: 'github.com/dabslee/Karaoke' },
                            'Source code'
                        ),
                        ' • ',
                        React.createElement(
                            'a',
                            { href: 'brandonssandbox.com' },
                            'Brandon\'s Website'
                        )
                    ),
                    React.createElement(
                        'div',
                        { className: 'neonBtn', onClick: function onClick() {
                                return _this2.setState({ page: "home" });
                            } },
                        'BACK'
                    )
                );
            } else if (this.state.page == "start" || this.state.page == "start2") {
                // Combined start and start2 as they are very similar
                var searchresults = [];
                // Loop for generating search results - this needs to be JSX
                // The original _loop function created React.createElement calls.
                // We will map results to JSX elements directly.
                results.forEach(function (result) {
                    // Changed from for...of to forEach for broader compatibility if Symbol.iterator is an issue
                    searchresults.push(React.createElement(
                        'div',
                        { onClick: function onClick() {
                                return _this2.setState({ page: "watch" + result.id });
                            }, className: 'searchresult', key: result.id },
                        ' ',
                        React.createElement('img', { src: result.thumb, alt: 'No thumbnail available' }),
                        React.createElement(
                            'p',
                            { style: { marginLeft: "20px" } },
                            result.title
                        )
                    ));
                });

                // Determine which page to switch back to for the refresher
                var nextPage = this.state.page === "start" ? "start2" : "start";

                return React.createElement(
                    'div',
                    { style: { display: "flex", flexDirection: "column", alignItems: "center", marginTop: "10%" } },
                    React.createElement(
                        'div',
                        { className: 'logo2', style: { fontWeight: "thin" } },
                        React.createElement(
                            'b',
                            null,
                            'Search for a song:'
                        )
                    ),
                    React.createElement(
                        'div',
                        { style: { width: "100%", display: "flex", flexDirection: "row", justifyContent: "center", marginBottom: "30px" } },
                        React.createElement('input', { id: 'query', placeholder: 'e.g. Never Gonna Give You Up', style: { width: '80%' } }),
                        React.createElement(
                            'div',
                            { id: 'searchbutton', className: 'logo2', onClick: this.keyWordsearch, style: { cursor: "pointer", margin: 0 } },
                            React.createElement(
                                'b',
                                null,
                                '\u2794'
                            )
                        ),
                        React.createElement('div', { id: 'refresher', onClick: function onClick() {
                                return _this2.setState({ page: nextPage });
                            } })
                    ),
                    React.createElement(
                        'div',
                        { id: 'results' },
                        searchresults,
                        ' '
                    ),
                    React.createElement(
                        'div',
                        { className: 'neonBtn', onClick: function onClick() {
                                return _this2.setState({ page: "home" });
                            } },
                        'BACK'
                    )
                );
            } else if (this.state.page.includes("watch")) {
                selectedVidId = this.state.page.substring(5); // This global var assignment is kept as is
                return React.createElement(
                    'div',
                    { className: 'centerbox' },
                    React.createElement('div', { id: 'video', style: { width: "80%", pointerEvents: "none", aspectRatio: "16/9", height: "auto" } }),
                    React.createElement(
                        'div',
                        { style: { display: "flex", flexDirection: "row" } },
                        React.createElement(
                            'div',
                            {
                                className: 'neonBtn',
                                onClick: function onClick() {
                                    if (player) {
                                        player.destroy();
                                        player = null;
                                    }
                                    _this2.setState({ page: "start" });
                                }
                            },
                            'BACK'
                        ),
                        React.createElement(
                            'div',
                            { id: 'begin-button', className: 'neonBtn', onClick: this.handleBegin },
                            'BEGIN'
                        )
                    )
                );
            }
            return null; // Default return if no state matches
        }
    }, {
        key: 'componentDidUpdate',
        value: function componentDidUpdate(prevProps, prevState) {
            // This logic remains the same as it doesn't involve React.createElement
            if (this.state.page.includes("watch") && (!prevState.page || !prevState.page.includes("watch") || this.state.page !== prevState.page)) {
                var _selectedVidId = this.state.page.substring(5);
                if (window.YT && window.YT.Player) {
                    if (player) player.destroy();
                    player = new window.YT.Player('video', {
                        videoId: _selectedVidId,
                        width: '80%',
                        playerVars: {
                            'autoplay': 0,
                            'controls': 0,
                            'disablekb': 1,
                            'enablejsapi': 1
                        }
                    });
                }
            }
        }
    }]);

    return Content;
}(React.Component);

var domContainer = document.querySelector('#content');
// Convert the final ReactDOM.render to use JSX
ReactDOM.render(React.createElement(Content, null), domContainer);

// This event listener remains the same
document.addEventListener('keydown', function (e) {
    if (e.code === "Enter" && document.getElementById("searchbutton")) document.getElementById("searchbutton").click();
});