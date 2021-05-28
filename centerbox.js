var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var selectedVidId;
var results = [];

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
                    $('#refresher').click();
                });
            });
        };

        _this.state = { page: "home" };
        _this.keyWordsearch = _this.keyWordsearch.bind(_this);
        return _this;
    }

    _createClass(Content, [{
        key: 'render',
        value: function render() {
            var _this2 = this;

            if (this.state.page == "home") {
                return React.createElement(
                    'div',
                    { 'class': 'centerbox' },
                    React.createElement(
                        'div',
                        { 'class': 'logo' },
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
                        { 'class': 'logo2' },
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
                        { 'class': 'neonBtn', onClick: function onClick() {
                                return _this2.setState({ page: "start" });
                            } },
                        'START'
                    ),
                    React.createElement(
                        'div',
                        { 'class': 'neonBtn', onClick: function onClick() {
                                return _this2.setState({ page: "about" });
                            } },
                        'ABOUT'
                    )
                );
            } else if (this.state.page == "about") {
                return React.createElement(
                    'div',
                    { 'class': 'centerbox' },
                    React.createElement(
                        'div',
                        { 'class': 'logo' },
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
                        'KU was made in May 2021 by Brandon Lee.',
                        React.createElement('br', null),
                        React.createElement(
                            'a',
                            { href: 'github.com/dabslee/Karaoke' },
                            'Source code'
                        ),
                        ' \u2022 ',
                        React.createElement(
                            'a',
                            { href: 'brandonssandbox.com' },
                            'Brandon\'s Website'
                        )
                    ),
                    React.createElement(
                        'div',
                        { 'class': 'neonBtn', onClick: function onClick() {
                                return _this2.setState({ page: "home" });
                            } },
                        'BACK'
                    )
                );
            } else if (this.state.page == "start") {
                var searchresults = [];

                var _loop = function _loop(result) {
                    searchresults.push(React.createElement(
                        'div',
                        { onClick: function onClick() {
                                return _this2.setState({ page: "watch" + result.id });
                            }, 'class': 'searchresult' },
                        React.createElement('img', { src: result.thumb, alt: 'No thumbnail available' }),
                        React.createElement(
                            'p',
                            { style: { marginLeft: "20px" } },
                            result.title
                        )
                    ));
                };

                var _iteratorNormalCompletion = true;
                var _didIteratorError = false;
                var _iteratorError = undefined;

                try {
                    for (var _iterator = results[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                        var result = _step.value;

                        _loop(result);
                    }
                } catch (err) {
                    _didIteratorError = true;
                    _iteratorError = err;
                } finally {
                    try {
                        if (!_iteratorNormalCompletion && _iterator.return) {
                            _iterator.return();
                        }
                    } finally {
                        if (_didIteratorError) {
                            throw _iteratorError;
                        }
                    }
                }

                return React.createElement(
                    'div',
                    { style: { display: "flex", flexDirection: "column", alignItems: "center", marginTop: "10%" } },
                    React.createElement(
                        'div',
                        { 'class': 'logo2', style: { fontWeight: "thin" } },
                        React.createElement(
                            'b',
                            null,
                            'Search for a song:'
                        )
                    ),
                    React.createElement(
                        'div',
                        { style: { width: "100%", display: "flex", flexDirection: "row", justifyContent: "center", marginBottom: "30px" } },
                        React.createElement('input', { id: 'query', placeholder: 'e.g. Never Gonna Give You Up' }),
                        React.createElement(
                            'div',
                            { id: 'searchbutton', 'class': 'logo2', onClick: this.keyWordsearch, style: { cursor: "pointer", margin: 0 } },
                            React.createElement(
                                'b',
                                null,
                                '\u279C'
                            )
                        ),
                        React.createElement('div', { id: 'refresher', onClick: function onClick() {
                                return _this2.setState({ page: "start2" });
                            } })
                    ),
                    React.createElement(
                        'div',
                        { id: 'results' },
                        searchresults
                    ),
                    React.createElement(
                        'div',
                        { 'class': 'neonBtn', onClick: function onClick() {
                                return _this2.setState({ page: "home" });
                            } },
                        'BACK'
                    )
                );
            } else if (this.state.page == "start2") {
                var searchresults = [];

                var _loop2 = function _loop2(_result) {
                    searchresults.push(React.createElement(
                        'div',
                        { onClick: function onClick() {
                                return _this2.setState({ page: "watch" + _result.id });
                            }, 'class': 'searchresult' },
                        React.createElement('img', { src: _result.thumb, alt: 'No thumbnail available' }),
                        React.createElement(
                            'p',
                            { style: { marginLeft: "20px" } },
                            _result.title
                        )
                    ));
                };

                var _iteratorNormalCompletion2 = true;
                var _didIteratorError2 = false;
                var _iteratorError2 = undefined;

                try {
                    for (var _iterator2 = results[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
                        var _result = _step2.value;

                        _loop2(_result);
                    }
                } catch (err) {
                    _didIteratorError2 = true;
                    _iteratorError2 = err;
                } finally {
                    try {
                        if (!_iteratorNormalCompletion2 && _iterator2.return) {
                            _iterator2.return();
                        }
                    } finally {
                        if (_didIteratorError2) {
                            throw _iteratorError2;
                        }
                    }
                }

                return React.createElement(
                    'div',
                    { style: { display: "flex", flexDirection: "column", alignItems: "center", marginTop: "10%" } },
                    React.createElement(
                        'div',
                        { 'class': 'logo2', style: { fontWeight: "thin" } },
                        React.createElement(
                            'b',
                            null,
                            'Search for a song:'
                        )
                    ),
                    React.createElement(
                        'div',
                        { style: { width: "100%", display: "flex", flexDirection: "row", justifyContent: "center", marginBottom: "30px" } },
                        React.createElement('input', { id: 'query', placeholder: 'e.g. Never Gonna Give You Up' }),
                        React.createElement(
                            'div',
                            { id: 'searchbutton', 'class': 'logo2', onClick: this.keyWordsearch, style: { cursor: "pointer", margin: 0 } },
                            React.createElement(
                                'b',
                                null,
                                '\u279C'
                            )
                        ),
                        React.createElement('div', { id: 'refresher', onClick: function onClick() {
                                return _this2.setState({ page: "start" });
                            } })
                    ),
                    React.createElement(
                        'div',
                        { id: 'results' },
                        searchresults
                    ),
                    React.createElement(
                        'div',
                        { 'class': 'neonBtn', onClick: function onClick() {
                                return _this2.setState({ page: "home" });
                            } },
                        'BACK'
                    )
                );
            } else if (this.state.page.includes("watch")) {
                selectedVidId = this.state.page.substring(5);
                var link = "http://www.youtube.com/embed/" + selectedVidId + "?enablejsapi=1&disablekb=1&controls=0";
                return React.createElement(
                    'div',
                    { 'class': 'centerbox' },
                    React.createElement('iframe', { id: 'video', width: '80%', height: '80%', style: { pointerEvents: "none" },
                        src: link }),
                    React.createElement(
                        'div',
                        { style: { display: "flex", flexDirection: "row" } },
                        React.createElement(
                            'div',
                            { 'class': 'neonBtn', onClick: function onClick() {
                                    return _this2.setState({ page: "start" });
                                } },
                            'BACK'
                        ),
                        React.createElement(
                            'div',
                            { id: 'begin-button', 'class': 'neonBtn', onClick: function onClick() {
                                    return $('#video')[0].contentWindow.postMessage('{"event":"command","func":"' + 'playVideo' + '","args":""}', '*');
                                } },
                            'BEGIN'
                        )
                    )
                );
            }
        }
    }]);

    return Content;
}(React.Component);

var domContainer = document.querySelector('#content');
ReactDOM.render(React.createElement(Content), domContainer);

document.addEventListener('keydown', function (e) {
    if (e.code === "Enter" && document.getElementById("searchbutton")) document.getElementById("searchbutton").click();
});