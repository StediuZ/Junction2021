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
            console.log(props.hourlyheat)
            var heatmapInstance = h337.create({
                // only container is required, the rest will be defaults
                container: document.querySelector('.chart'),
                opacity: 0.1
            });
            
            var points = [];
            var max = 0;
            var width = 5270;
            var height = 2636;
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

            var chart = document.querySelector('.chart')
            var rect = chart.getBoundingClientRect()
            var div_width = rect["width"]
            var div_height = rect["height"]
            console.log(chart.getBoundingClientRect())
            console.log(div_height)

            var img_height = props.meta["height"]
            img_height = 2636

            var img_width = props.meta["width"]
            img_width = 5270

            for (let i = 0;i <points.length; i++) {
                points[i] = {
                    x:points[i]["x"]/img_width*div_width,
                    y:div_height*0.05 + points[i]["y"]/img_height*div_height*0.9,
                    value: points[i]["value"]
                }
                console.log(div_height*0.05 + points[i]["y"]/img_height*div_height*0.9,)

            }
            console.log(points)
            // heatmap data format
            var data = {
                max: 20,
                data: points
            };
            // if you have a set of datapoints always use setData instead of addData
            // for data initialization
            heatmapInstance.setData(data);
     }, [props.hourlyheat])

    return (
        <Box className="chart" >
            <HighchartsReact
            highcharts={Highcharts}
            options={props.options}
            />
        </Box>
    );
  
  }
  
  export default Chart;
  