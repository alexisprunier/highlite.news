import React from "react";
import "./PageHome.css";
import {getRequest} from "../utils/request";
import Video from "./Video";
import Loading from "./Loading";
import {NotificationManager} from 'react-notifications';


class PageHome extends React.Component {

    constructor(props) {
        super(props);

        this.getDates = this.getDates.bind(this);

        this.state = {
            videos: null,
            selectedVideo: null
        };
    }

    componentDidMount() {
        getRequest.call(this, "r/get_videos", data => {
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
            <div id="PageHome">
                <div className="title1">
                    Dernières vidéos publiées
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
                        this.getDates().map(d => { return (
                            <div>
                                <div className="title2">
                                    {d}
                                </div>
                                {this.state.videos.filter(v => v.creation_date == d).map(v => { return (
                                    <Video
                                        v={v}
                                    />
                                )})}
                            </div>
                        )})
                }
            </div>
        );
    }
}

export default PageHome;