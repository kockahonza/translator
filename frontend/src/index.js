import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import 'bulma/css/bulma.css'


class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			output: "",
			numOfActiveChanges: 0,
		};
		this.updateOutput("hello world");
	}

	handleChange(event) {
		const input = event.target.value;
		let numOfActiveChanges = this.state.numOfActiveChanges + 1;
		this.setState({
			numOfActiveChanges: numOfActiveChanges,
		});
		setTimeout(() => {
			if (numOfActiveChanges < this.state.numOfActiveChanges) {
				console.log("Ending " + numOfActiveChanges);
				return;
			}
			this.setState({
				numOfActiveChanges: 0,
			});
			this.updateOutput(input);
		}, 500);
	}

	updateOutput(input) {
		fetch('http://192.168.0.146:8000', {
			method: 'POST',
			headers: {
				'content-type': 'application/json'
			},
			body: JSON.stringify({input: input}),
		}).then(response => {
			return response.json();
		}).then(data => {
			console.log(data);
			this.setState(data);
		}).catch(function(err) {
			console.log('An error occured');
		});
	}

	render() {
		return (
			<div className="container">
				<div className="column is-6 is-offset-3">

					<div className="box">
						<div className="field">
							<p className="control is-expanded">
								<input
									className="input"
									placeholder="Enter text"
									onChange={this.handleChange.bind(this)}
									defaultValue="hello world"
								/>
							</p>
						</div>
					</div>

					<div className="box has-text-black">
						<div className="output content">
							{this.state.output}
						</div>
					</div>

				</div>
			</div>
		);
	}
}

// ========================================

ReactDOM.render(
	<App />,
	document.getElementById('root')
);
