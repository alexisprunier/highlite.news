import React from "react";
import Menu from "./component/Menu";
import PageHome from "./component/PageHome";
import "./App.css";


class App extends React.Component {

    constructor(props) {
        super(props);

        this.changeMenu = this.changeMenu.bind(this);

        this.state = {
            selectedMenu: "HOME"
        };
    }

    componentDidMount() {

    }

    changeMenu(menu) {
        this.setState({ menu: menu })
    }

    render() {
        return (
            <div id="container">
                <div id="content">
                    {this.state.selectedMenu == "HOME" ?
                        <PageHome/>
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