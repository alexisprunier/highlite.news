import React from "react";
import "./Article.css";
import {postRequest, getRequest} from "../utils/request";
import {NotificationManager} from 'react-notifications';


class Article extends React.Component {

    constructor(props) {
        super(props);

        this.vote = this.vote.bind(this);

        this.state = {
            voteCount: null,
        };
    }

    vote() {
        let params = {"article_id": this.props.a.id}

        postRequest.call(this, "r/vote", params, () => {
            NotificationManager.info('Le vote a été comptabilisé');

            getRequest.call(this, "r/get_votes_of_article?article_id=" + this.props.a.id, data => {
                this.setState({ voteCount: data })
            }, response => {
                NotificationManager.warning(response.statusText);
            }, error => {
                NotificationManager.error(error.message);
            });

        }, response => {
            NotificationManager.warning(response.statusText);
        }, error => {
            NotificationManager.error(error.message);
        });
    }

    hasVote() {
        return typeof this.props.a.nb_vote !== "undefined";
    }

    getTextSize() {
        return this.hasVote() ? "8" : "10";
    }

    render() {
        return (
            <div className="Article">
                <div className="row">
                    <div className="col-lg-2 col-md-12 Article-image">
                        <img className={"Article-image-img"} src={this.props.a.image_url}/>
                    </div>
                    <div className={"col-lg-" + this.getTextSize() + " col-md-12"}>
                        <div className="row">
                            <div className="col-lg-12 col-md-12">
                                <div className="Article-title title3">
                                    {this.props.a.title}
                                </div>
                            </div>
                            <div className="col-lg-6 col-md-6 col-6">
                                <div className="Article-category title4">
                                    {this.props.a.source}
                                </div>
                            </div>
                            <div className="col-lg-6 col-md-6 col-6">
                                <div className="Article-links">
                                    {this.props.a.url !== null ?
                                        <a href={this.props.a.url} target="_blank">Aller sur l'article</a>
                                    :
                                        ""
                                    }
                                </div>
                            </div>
                        </div>
                    </div>
                    {this.hasVote() ?
                        <div className={"col-lg-2 col-md-12"}>
                            <div className={"Article-vote " + (this.state.voteCount === null ? "" : "Article-vote-done")} onClick={this.vote}>
                                <i class="fas fa-vote-yea"></i>
                                <div>{this.state.voteCount === null ? this.props.a.nb_vote : this.state.voteCount}</div>
                            </div>
                        </div>
                    : ""}
                </div>
            </div>
        );
    }
}

export default Article;