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
                <div className="Video-youtube">
                    <iframe 
                        width="168" 
                        height="93" 
                        src={this.props.v.youtube_url}
                        frameborder="0" 
                        allow="autoplay; encrypted-media" 
                        allowfullscreen>
                    </iframe>
                </div>
                <div className="Video-title">
                    {this.props.v.title}
                </div>
                <div className="Video-category">
                    {this.props.v.category}
                </div>
                <div className="Video-links">
                    Voir les liens
                </div>
            </div>
        );
    }
}

export default Video;