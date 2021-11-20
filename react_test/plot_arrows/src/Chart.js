import background from './img/site_1.png';
import React, {Component} from "react";
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import highchartsVector from 'highcharts/modules/vector'
import { mockdata } from "./data"
highchartsVector(Highcharts)

var uiscale = 4

function calc_height () {
    var height_ratio = 2636/5270
    return height_ratio*100 + "%"
}

const options = {
  chart: {
    plotBackgroundImage: "http://127.0.0.1:8080/site_1.png",
    height: calc_height
  },
  title: {
    text: ""
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
  