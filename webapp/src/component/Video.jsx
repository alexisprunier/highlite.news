import React from "react";
import "./Video.css";
import {getRequest} from "../utils/request";
import Loading from "./Loading";
import Article from "./Article";
import {NotificationManager} from 'react-notifications';


class Video extends React.Component {

    constructor(props) {
        super(props);

        this.onArticleLinkClick = this.onArticleLinkClick.bind(this);

        this.state = {
            articles: null,
            opened: false,
        };
    }

    onArticleLinkClick(video_id) {
        if (this.state.articles == null) {
            getRequest.call(this, "r/get_articles_of_video?video_id=" + video_id, data => {
                this.setState({
                    articles: data,
                });
            }, response => {
                NotificationManager.warning(response.statusText);
            }, error => {
                NotificationManager.error(error.message);
            });
        }

        let opened = !this.state.opened;

        this.setState({ opened: opened });
    }

    render() {
        return (
            <div className="Video">
                <div className="row">
                    <div className="col-md-4 col-xs-12 Video-video">
                        <img src={"img/background_" + this.props.v.category.replace(" ", "") + ".jpg"}/>
                    </div>
                    <div className="col-md-8 col-xs-12">
                        <div className="row">
                            <div className="col-md-12 col-xs-12">
                                <div className="Video-title title3">
                                    {this.props.v.title}
                                </div>
                            </div>
                            <div className="col-md-12 col-xs-12 col-12">
                                <div className="Video-category title4">
                                    {this.props.v.category}
                                </div>
                            </div>
                            <div className="col-md-6 col-xs-6 col-6">
                                <div className="Video-link">
                                    {this.props.v.youtube_id !== null ?
                                        <a href={"https://youtube.com/watch?v=" + this.props.v.youtube_id} target="_blank">Voir la vidéo</a>
                                    :
                                        ""
                                    }
                                </div>
                            </div>
                            <div className="col-md-6 col-xs-6 col-6">
                                <div className="Video-article-link">
                                    {this.props.v.youtube_id !== null ?
                                        <a onClick={() => this.onArticleLinkClick(this.props.v.id)} href="#">
                                            {this.state.opened ? "Cacher les articles" : "Voir les articles"}
                                        </a>
                                    :
                                        ""
                                    }
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                {this.state.opened ?
                    <div className="Video-articles">
                        {this.state.articles === null ?
                            <div className="Video-loading-articles">
                                <Loading/>
                            </div>
                        : 
                            this.state.articles.length === 0 ?
                                <div className="Video-loading-articles">
                                    <div className="Video-no-article title3">Pas d'article trouvé</div>
                                </div>
                            :
                                this.state.articles.map(a => { return (
                                    <Article
                                        a={a}
                                    />
                                )})}
                    </div>
                : ""}
            </div>
        );
    }
}

export default Video;