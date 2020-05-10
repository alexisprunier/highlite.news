import React from "react";
import "./PageAdmin.css";
import {getRequest} from "../utils/request";
import VideoAdmin from "./VideoAdmin";
import Loading from "./Loading";
import {NotificationManager} from 'react-notifications';


class PageAdmin extends React.Component {

    constructor(props) {
        super(props);

        this.getDates = this.getDates.bind(this);

        this.state = {
            videos: null,
            selectedVideo: null
        };
    }

    componentDidMount() {
        getRequest.call(this, "r/get_videos_of_the_day", data => {
            this.setState({
                videos: data,
            });
        }, response => {
            NotificationManager.warning(response.statusText);
        }, error => {
            NotificationManager.error(error.message);
        });
    }

    getDates() {
        return [...new Set(this.state.videos.map(v => { return v.creation_date }))].reverse();;
    }

    render() {
        return (
            <div id="PageAdmin">
                <div className="title1">
                    Panel d'administration
                </div>
                {this.state.videos === null ? 
                    <div className="PageHome-loading-box">
                        <Loading/>
                    </div>
                :
                    this.state.videos.length === 0 ? 
                        <div className="PageHome-loading-box">
                            <div className="PageHome-no-article title3">Pas de vidéo disponible</div>
                        </div>
                    :
                        this.state.videos.map(v => { return (
                            <VideoAdmin
                                v={v}
                            />
                        )})
                }
            </div>
        );
    }
}

export default PageAdmin;