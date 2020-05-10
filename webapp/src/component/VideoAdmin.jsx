import React from "react";
import "./VideoAdmin.css";
import Loading from "./Loading";
import {getRequest, getBlobRequest} from "../utils/request";
import {NotificationManager} from 'react-notifications';


class VideoAdmin extends React.Component {

    constructor(props) {
        super(props);

        this.downloadVideo = this.downloadVideo.bind(this);
    }

    downloadVideo(videoName) {
        getBlobRequest.call(this, "r/download_video?video_name=" + videoName, blob => {
            const url = window.URL.createObjectURL(new Blob([blob]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', videoName);
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        }, response => {
            NotificationManager.warning(response.statusText);
        }, error => {
            NotificationManager.error(error.message);
        });
    }

    render() {
        return (
            <div className="VideoAdmin">
                <div className="row">
                    <div className="col-md-4 col-xs-12 VideoAdmin-picture">
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
                                    <a onClick={() => this.downloadVideo(this.props.v.file_name.split("/").slice(-1)[0])} href="#">
                                        Download {this.props.v.format} format
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default VideoAdmin;