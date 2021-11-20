import background from './img/site_1.png';
import React, {Component} from "react";
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import highchartsVector from 'highcharts/modules/vector'
import { mockdata } from "./data"
highchartsVector(Highcharts)

var uiscale = 4

const options = {
  chart: {
    plotBackgroundImage: "http://127.0.0.1:8080/site_1.png",
    height: 2635/uiscale,
    width: 5270/uiscale
  },
  title: {
    text: "Flow"
  },
  series: [{
    data: mockdata,
    type: "vector"
  }],
  xAxis: {
    visible: false
  },
  yAxis: {
    visible: false
  }
}

class Chart extends Component {
    constructor(props) {
      super(props);
    }
    render() {
      return (
        <div >
          <HighchartsReact
            highcharts={Highcharts}
            options={options}
          />
        </div>
      );
    }
  
  }
  
  export default Chart;
  