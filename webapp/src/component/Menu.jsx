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
							<span><i class="fab fa-youtube"></i></span></a>
						</li>
						<li><a href="https://twitter.com/highlitenews" target="_blank">
							<span><i class="fab fa-twitter"></i></span></a>
						</li>
						<li><a href="https://www.instagram.com/highlite.news/?hl=en" target="_blank">
							<span><i class="fab fa-instagram"></i></span></a>
						</li>
						<li><a href="#"><span><i class="fas fa-home"></i></span></a></li>
						<li><a href="#"><span><i class="fas fa-person-booth"></i></span></a></li>
						<li><a href="https://www.snapchat.com/add/highlite.news" target="_blank">
							<span><i class="fab fa-snapchat-ghost"></i></span></a>
						</li>
						<li><a href="https://tiktok.com/@highlite.news" target="_blank">
							<span><i class="fas fa-music"></i></span></a>
						</li>
					 </ul>
				</div>
			</div>
		);
	}
}

export default Menu;