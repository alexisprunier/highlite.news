import React from "react";
import "./PageHome.css";
import {getRequest} from "../utils/request";
import Video from "./Video";


class PageHome extends React.Component {

    constructor(props) {
        super(props);

        this.getDates = this.getDates.bind(this);

        this.state = {
            videos: []
        };
    }

    componentDidMount() {
        getRequest.call(this, "r/get_videos", data => {
            this.setState({
                videos: data,
            });
        }, response => {
        }, error => {
        });
    }

    getDates() {
        return [...new Set(this.state.videos.map(v => { return v.date }))];
    }

    render() {
        return (
            <div id="PageHome">
                <div className="title1">
                    Dernières vidéos publiées
                </div>
                {this.getDates().map(d => { return (
                    <div>
                        <div className="title2">
                            {d}
                        </div>
                        {this.state.videos.filter(v => v.date == d).map(v => { return (
                            <Video
                                v={v}
                            />
                        )})}
                    </div>
                )})}
            </div>
        );
    }
}

export default PageHome;