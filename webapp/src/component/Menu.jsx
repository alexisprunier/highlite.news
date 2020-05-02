import React from 'react';
import './Menu.css'


class Menu extends React.Component {

	constructor(props){
		super(props);

		this.onMenuClick = this.onMenuClick.bind(this);

		this.state={
			open: false
		}
	}

	componentDidMount() {
	}

	onMenuClick() {
		this.setState({ open: !this.state.open});
	}

	render(){
		return(
			<div className="menu">
				<button 
					className="cn-button" 
					id="cn-button"
					onClick={this.onMenuClick}>
					{this.state.open ? <i className="fas fa-times"></i>: <i className="fas fa-bars"></i>}
				</button>
				<div 
					className={"cn-wrapper " + (this.state.open ? "opened-nav": "")} 
					id="cn-wrapper">
					<ul>
						<li><a href="#" onClick={() => this.props.changeMenu("HOME")}>
							<span><i className="fas fa-home"></i></span></a>
						</li>
						<li><a href="#" onClick={() => this.props.changeMenu("VOTE")}>
							<span><i className="fas fa-person-booth"></i></span></a>
						</li>
						<li><a href="https://www.facebook.com/highlite.news" target="_blank">
							<span><i className="fab fa-facebook" style={{"color": "#3B5998"}}></i></span></a>
						</li>
						<li><a href="https://twitter.com/highlitenews" target="_blank">
							<span><i className="fab fa-twitter" style={{"color": "#1DA1F2"}}></i></span></a>
						</li>
						<li><a href="https://www.instagram.com/highlite.news/?hl=en" target="_blank">
							<span><i className="fab fa-instagram" style={{"color": "#8a3ab9"}}></i></span></a>
						</li>
						<li><a href="https://tiktok.com/@highlite.news" target="_blank">
							<span><i className="fas fa-music" style={{"color": "#EE1D52"}}></i></span></a>
						</li>
						<li><a href="https://www.snapchat.com/add/highlite.news" target="_blank">
							<span><i className="fab fa-snapchat-ghost" style={{"color": "#000000"}}></i></span></a>
						</li>
					 </ul>
				</div>
			</div>
		);
	}
}

export default Menu;