import React from "react";
import Menu from "./component/Menu";
import "./App.css";


class App extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
        };
    }

    componentDidMount() {

    }

    render() {
        return (
            <div id="container">
                <div id="content">

                </div>            
                <Menu/>
            </div>
        );
    }
}

export default App;