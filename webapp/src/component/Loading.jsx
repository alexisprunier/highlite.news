import React from 'react';
import './Loading.css'

class Loading extends React.Component {

    render() {
        return (
            <div className="loader">
                <div className="spinner">
                    <div className="double-bounce1"></div>
                    <div className="double-bounce2"></div>
                </div>
            </div>
        )
    }
}

export default Loading;