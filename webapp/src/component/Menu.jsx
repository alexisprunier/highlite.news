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
					{this.state.open ? "Close": "Menu"}
				</button>
				<div 
					className={"cn-wrapper " + (this.state.open ? "opened-nav": "")} 
					id="cn-wrapper">
					<ul>
						<li><a href="#"><span>About</span></a></li>
						<li><a href="#"><span>Tutorials</span></a></li>
						<li><a href="#"><span>Articles</span></a></li>
						<li><a href="#"><span>Snippets</span></a></li>
						<li><a href="#"><span>Plugins</span></a></li>
						<li><a href="#"><span>Contact</span></a></li>
						<li><a href="#"><span>Follow</span></a></li>
					 </ul>
				</div>
			</div>
		);
	}
}

export default Menu;