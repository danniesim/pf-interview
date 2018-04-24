import React, { Component } from 'react';

import SearchFilters from './SearchFilters';

class Header extends Component {
	constructor(props) {
		super(props);
		this.state = {
			visible: true,
		};
	}

	toggleVisibility = () => {
		const visible = !this.state.visible;
		this.setState({
			visible
		});
	}

	render() {
		return (
			<nav className={`navbar ${this.state.visible ? 'active' : ''}`}>
				<div className="title">CourseXplore</div>
				<div className="btn toggle-btn" onClick={this.toggleVisibility}>Toggle Filters</div>
				<SearchFilters {...this.props} visible={this.state.visible} />
			</nav>
		);
	}
}

export default Header;