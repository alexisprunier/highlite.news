import React from "react";
import "./PageVote.css";
import {getRequest} from "../utils/request";
import Article from "./Article";


class PageVote extends React.Component {

    constructor(props) {
        super(props);

        this.getCategory = this.getCategory.bind(this);

        this.state = {
            articles: []
        };
    }

    componentDidMount() {
        getRequest.call(this, "r/get_articles", data => {
            this.setState({
                articles: data,
            });
        }, response => {
        }, error => {
        });
    }

    getCategory() {
        return [...new Set(this.state.articles.map(v => { return v.category }))];
    }

    render() {
        return (
            <div id="PageHome">
                <div className="title1">
                    Votez pour les articles du jour
                </div>
                {this.getCategory().map(c => { return (
                    <div>
                        <div className="title2">
                            {c}
                        </div>
                        {this.state.articles.filter(a => a.category == c).map(a => { return (
                            <Article
                                a={a}
                            />
                        )})}
                    </div>
                )})}
            </div>
        );
    }
}

export default PageVote;