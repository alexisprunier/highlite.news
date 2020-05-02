import React from "react";
import "./Article.css";
import {postRequest} from "../utils/request";


class Article extends React.Component {

    constructor(props) {
        super(props);

        this.vote = this.vote.bind(this);

        this.state = {
        };
    }

    vote() {
        let params = {"article_id": this.props.a.id}

        postRequest.call(this, "r/vote", params, () => {
            console.Log("OK");
        }, response => {
        }, error => {
        });
    }

    render() {
        return (
            <div className="Article">
                <div className="row">
                    <div className="col-lg-2 col-md-12 Article-image">
                        <img className={"Article-image-img"} src={this.props.a.image_url}/>
                    </div>
                    <div className="col-lg-8 col-md-12">
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
                    <div className="col-lg-2 col-md-12">
                        <div className="Article-vote" onClick={this.vote}>
                            <i class="fas fa-vote-yea"></i>
                            <div>{this.props.a.nb_vote}</div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Article;