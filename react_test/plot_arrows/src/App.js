import React, {Component} from "react";
import './App.css';
import Chart from './Chart'
import Slider from './Slider'


class App extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div >
        <Chart/>
        <Slider/>
      </div>
    );
  }

}

export default App; 
