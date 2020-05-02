import React from "react";
import "./PageVote.css";
import {getRequest} from "../utils/request";
import Article from "./Article";
import Loading from "./Loading";
import {NotificationManager} from 'react-notifications';


class PageVote extends React.Component {

    constructor(props) {
        super(props);

        this.getCategory = this.getCategory.bind(this);

        this.state = {
            articles: null
        };
    }

    componentDidMount() {
        getRequest.call(this, "r/get_articles", data => {
            this.setState({
                articles: data,
            });
        }, response => {
            NotificationManager.warning(response.statusText);
        }, error => {
            NotificationManager.error(error.message);
        });
    }

    getCategory() {
        return [...new Set(this.state.articles.map(v => { return v.category }))];
    }

    render() {
        return (
            <div id="PageVote">
                <div className="title1">
                    Vote pour les articles du jour !
                </div>
                {this.state.articles === null ? 
                    <div className="PageVote-loading-box">
                        <Loading/>
                    </div>
                :
                    this.state.articles.length === 0 ? 
                        <div className="PageVote-loading-box">
                            <div className="PageVote-no-article title3">Pas d'article disponible pour le vote</div>
                        </div>
                    :
                        this.getCategory().map(c => { return (
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
                        )})  
                }
            </div>
        );
    }
}

export default PageVote;