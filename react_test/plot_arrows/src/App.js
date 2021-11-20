import React, {Component} from "react";
import './App.css';
import Chart from './Chart'


class App extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div >
        <Chart/>
      </div>
    );
  }

}

export default App;
