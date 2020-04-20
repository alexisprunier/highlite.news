import React from "react";
import "./Video.css";


class Video extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
        };
    }

    render() {
        return (
            <div className="Video">
                <div className="row">
                    <div className="col-md-4 col-xs-12 Video-video">
                        <iframe 
                            src={this.props.v.youtube_url}
                            frameborder="0" 
                            allow="autoplay; encrypted-media" 
                            allowfullscreen>
                        </iframe>
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
                                <div className="Video-articles">
                                    {this.props.v.youtube_id !== null ?
                                        <a href={"https://youtube.com/watch?v=" + this.props.v.youtube_id} target="_blank">Voir les articles</a>
                                    :
                                        ""
                                    }
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Video;