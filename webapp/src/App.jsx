import React from "react";
import Menu from "./component/Menu";
import PageHome from "./component/PageHome";
import PageVote from "./component/PageVote";
import "./App.css";


class App extends React.Component {

    constructor(props) {
        super(props);

        this.changeMenu = this.changeMenu.bind(this);

        this.state = {
            selectedMenu: "VOTE"
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
            </div>
        );
    }
}

export default App;