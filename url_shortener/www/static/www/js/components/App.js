import React from "react";
import request from 'superagent';
import {getCookie} from "../utils";

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            shortened: null,
            original: '',
            errMsg: null
        };

        // Bindings
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.createShortenedURL = this.createShortenedURL.bind(this);
    }

    createShortenedURL(url) {
        // TODO: Put base url in config
        const _this = this;
        const csrfToken = getCookie('csrftoken');
        request
            .post("http://127.0.0.1:3000/api/shortened_urls/")
            .send({url: url})
            .set('X-CSRFToken', csrfToken)
            .end(function (err, res) {
                const data = res.body;
                if (err) {
                    _this.setState({errMsg: data.error})
                } else {
                    _this.setState({
                        shortened: data.shortened_url
                    })
                }
            });
    }

    render() {
        return (
            <div className="app">
                <form onSubmit={this.handleSubmit}>
                    <label>
                        Name:
                        <input type="text" value={this.state.original}
                               onChange={this.handleChange}/>
                    </label>
                    <input type="submit" value="Submit"/>
                </form>
            </div>
        );
    }

    handleChange(event) {
        this.setState({original: event.target.value});
    }

    handleSubmit(event) {
        event.preventDefault();
        this.createShortenedURL(this.state.original);
    }
}

export default App;
