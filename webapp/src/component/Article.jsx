import React from "react";
import "./Article.css";


class Article extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
        };
    }

    render() {
        return (
            <div className="Article">
                <div className="row">
                    <div className="col-lg-2 col-md-12 Article-image">
                        <img className={"Article-image-img"} src={this.props.a.image_url}/>
                    </div>
                    <div className="col-lg-8 col-md-12">
                        <div className="row">
                            <div className="col-lg-12 col-md-12">
                                <div className="Article-title title3">
                                    {this.props.a.title}
                                </div>
                            </div>
                            <div className="col-lg-6 col-md-6">
                                <div className="Article-category title4">
                                    {this.props.a.category}
                                </div>
                            </div>
                            <div className="col-lg-6 col-md-6">
                                <div className="Article-links">
                                    {this.props.a.url !== null ?
                                        <a href={this.props.a.url} target="_blank">Aller sur l'article</a>
                                    :
                                        ""
                                    }
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-lg-2 col-md-12">
                        Vote
                    </div>
                </div>
            </div>
        );
    }
}

export default Article;