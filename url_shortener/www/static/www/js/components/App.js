import React from "react";
import request from "superagent";
import { getCookie } from "../utils";

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            shortened: null,
            original: "",
            errMsg: null
        };

        // Bindings
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.createShortenedURL = this.createShortenedURL.bind(this);
        this.renderError = this.renderError.bind(this);
        this.renderShortenedURL = this.renderShortenedURL.bind(this);
    }

    render() {
        return (
            <div className="app">
                <div>
                {this.renderError()}
                <form onSubmit={this.handleSubmit}>
                        <input className="url-input" type="text" value={this.state.original}
                               onChange={this.handleChange}/>
                    <input className="submit-btn" type="submit" value="Shorten" />
                </form>
                {this.renderShortenedURL()}
                </div>
            </div>
        );
    }

    createShortenedURL(url) {
        // TODO: Put base url in config
        const _this = this;
        const csrfToken = getCookie("csrftoken");
        request
            .post("http://127.0.0.1:3000/api/shortened_urls/")
            .send({url: url})
            .set("X-CSRFToken", csrfToken)
            .end(function (err, res) {
                const data = res.body;
                if (err) {
                    _this.setState({errMsg: data.error})
                } else {
                    _this.setState({
                        shortened: data.shortened_url,
                        errMsg: null
                    })
                }
            });
    }

    handleChange(event) {
        this.setState({original: event.target.value});
    }

    handleSubmit(event) {
        event.preventDefault();
        this.createShortenedURL(this.state.original);
    }

    renderError() {
        if (this.state.errMsg) {
            return (
                <p className="error-msg">Error: {this.state.errMsg}</p>
            );
        } else {
            return null;
        }
    }

    renderShortenedURL() {
        if (this.state.shortened) {
            return (
                <div>
                    Here is your shortened url:&nbsp;
                    <a href={this.state.shortened} target="_blank">{this.state.shortened}</a>
                </div>
            );
        } else {
            return null;
        }
    }
}

export default App;
