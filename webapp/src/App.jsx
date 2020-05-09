import React from "react";
import Menu from "./component/Menu";
import PageHome from "./component/PageHome";
import PageVote from "./component/PageVote";
import PageAdmin from "./component/PageAdmin";
import "./App.css";
import {NotificationContainer} from 'react-notifications';
import 'react-notifications/lib/notifications.css';


class App extends React.Component {

    constructor(props) {
        super(props);

        this.changeMenu = this.changeMenu.bind(this);

        this.state = {
            selectedMenu: window.location.hash === "#vote" ? "VOTE" : "HOME"
        };
    }

    componentDidMount() {

    }

    changeMenu(menu) {
        this.setState({ selectedMenu: menu })
    }

    render() {
        if (window.location.hash == "#PORTESECRETE") {
            return (
                <div id="container">
                    <div id="content">
                        <PageAdmin/>
                    </div>
                    <div id="background"/>
                </div>
            );
        }

        return (
            <div id="container">
                <div id="content">
                    <div className="SocialNetwork">
                        <div className="row">
                            <div className="col-md-3 col-xs-12 SocialNetworkLogo">
                                <img src={"img/Highlite62x200.png"}/>
                            </div>
                            <div className="col-md-3 col-xs-12 SocialNetworkCenter">
                                <div 
                                    className="fb-like" 
                                    data-href="https://www.facebook.com/highlite.news" 
                                    data-width="" 
                                    data-layout="button_count" 
                                    data-action="like" 
                                    data-size="small" 
                                    data-share="false">
                                </div>
                            </div>
                             <div className="col-md-3 col-xs-12 SocialNetworkCenter">
                                <a 
                                    href="https://twitter.com/highlitenews?ref_src=twsrc%5Etfw" 
                                    className="twitter-follow-button" data-show-count="false">
                                    Follow @highlitenews
                                </a>
                            </div>
                            <div className="col-md-3 col-xs-12 SocialNetworkCenter">
                                <div 
                                    className="g-ytsubscribe" 
                                    data-channelid="UCtqK3jsmIpnuIQT105cKr2A" 
                                    data-layout="default" 
                                    data-count="default">
                                </div>
                            </div>
                        </div>
                    </div>
                    {this.state.selectedMenu == "HOME" ?
                        <PageHome/>
                    : ""}
                    {this.state.selectedMenu == "VOTE" ?
                        <PageVote/>
                    : ""}
                </div>
                <div id="background"/>
                <Menu
                    changeMenu={this.changeMenu}
                />
                <NotificationContainer/>
            </div>
        );
    }
}

export default App;