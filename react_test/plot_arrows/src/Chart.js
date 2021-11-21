import background from './img/site_1.png';
import React, {Component, useState, useEffect} from "react";
import Highcharts from 'highcharts'
import Box from '@mui/material/Box';
import HighchartsReact from 'highcharts-react-official'
import highchartsVector from 'highcharts/modules/vector'
import h337 from 'heatmap.js'
highchartsVector(Highcharts)



function Chart(props) {
    useEffect(() => {
            console.log("heatmap!")
            var image = document.querySelectorAll('input[type=image]')
            console.log(image)
            var heatmapInstance = h337.create({
                // only container is required, the rest will be defaults
                container: document.querySelector('.chart'),
                opacity: 0.1
            });
            // now generate some random data
            var points = [];
            var max = 10;
            var width = 840;
            var height = 400;
            var len = 200;
        
            while (len--) {
                var val = Math.floor(Math.random()*100);
                max = Math.max(max, val);
                var point = {
                    x: Math.floor(Math.random()*width),
                    y: Math.floor(Math.random()*height),
                    value: val
                };
                points.push(point);

            }
            // heatmap data format
            var data = {
                max: max,
                data: points
            };
            // if you have a set of datapoints always use setData instead of addData
            // for data initialization
            heatmapInstance.setData(data);
     })

    return (
        <Box class="chart" >
            <HighchartsReact
            highcharts={Highcharts}
            options={props.options}
            />
        </Box>
    );
  
  }
  
  export default Chart;
  