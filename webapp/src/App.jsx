import React from "react";
import Menu from "./component/Menu";
import PageHome from "./component/PageHome";
import PageVote from "./component/PageVote";
import "./App.css";
import {NotificationContainer} from 'react-notifications';
import 'react-notifications/lib/notifications.css';


class App extends React.Component {

    constructor(props) {
        super(props);

        this.changeMenu = this.changeMenu.bind(this);

        console.log(window.location.hash)

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
        return (
            <div id="container">
                <div id="content">
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