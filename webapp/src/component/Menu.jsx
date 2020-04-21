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
					{this.state.open ? <i class="fas fa-times"></i>: <i class="fas fa-bars"></i>}
				</button>
				<div 
					className={"cn-wrapper " + (this.state.open ? "opened-nav": "")} 
					id="cn-wrapper">
					<ul>
						<li><a href="https://www.youtube.com/channel/UCtqK3jsmIpnuIQT105cKr2A" target="_blank">
							<span><i class="fab fa-youtube" style={{"color": "#FF0000"}}></i></span></a>
						</li>
						<li><a href="https://twitter.com/highlitenews" target="_blank">
							<span><i class="fab fa-twitter" style={{"color": "#1DA1F2"}}></i></span></a>
						</li>
						<li><a href="https://www.instagram.com/highlite.news/?hl=en" target="_blank">
							<span><i class="fab fa-instagram" style={{"color": "#8a3ab9"}}></i></span></a>
						</li>
						<li><a href="#" onClick={() => this.props.changeMenu("HOME")}>
							<span><i class="fas fa-home"></i></span></a>
						</li>
						<li><a href="#" onClick={() => this.props.changeMenu("VOTE")}>
							<span><i class="fas fa-person-booth"></i></span></a>
						</li>
						<li><a href="https://www.snapchat.com/add/highlite.news" target="_blank">
							<span><i class="fab fa-snapchat-ghost" style={{"color": "#000000"}}></i></span></a>
						</li>
						<li><a href="https://tiktok.com/@highlite.news" target="_blank">
							<span><i class="fas fa-music" style={{"color": "#EE1D52"}}></i></span></a>
						</li>
					 </ul>
				</div>
			</div>
		);
	}
}

export default Menu;