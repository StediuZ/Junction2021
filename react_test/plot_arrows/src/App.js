import React, {Component, useState, useEffect} from "react";
import axios from 'axios';
import './App.css';
import Chart from './Chart'
import Slider from './Slider'
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import DatePicker from './Datepicker';
import AppBar from './AppBar'
import { mockdata } from "./data"
import { seriesType } from "highcharts";

function calc_height () {
  var height_ratio = 2636/5270
  return height_ratio*100 + "%"
}

//window.onload = place_div


function App () {
  const [vectors, setVectors] = useState({});
  const [hour, setHour] = useState(0);
  const [date, setDate] = useState(new Date('2021-08-05T21:11:54'));
  const [site, setSite] = useState(1)
  const [aspect, setAspect] = useState("50%")
  const [heatdata, setHeatdata] = useState({})
  const [hourlyHeat, setHourlyHeat] = useState([])
  const [meta, setMeta] = useState({})
  const [options, setOptions] = useState({
    chart: {
      plotBackgroundImage: "http://127.0.0.1:8080/site_1.png",
      height: calc_height()
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
  })

  useEffect(() => {
    setHourlyHeat(heatdata[(hour).toString()])
  }, [hour, heatdata])

  useEffect(() => {
    setOptions({
      chart: {
        plotBackgroundImage: `http://127.0.0.1:8080/site_${site}.png`,
        height: calc_height()
        },
        title: {
          text: `Site ${site}`
        },
        series: [{
          data: vectors,
          type: "vector"
        }],
        xAxis: {
          visible: false
        },
        yAxis: {
          visible: false
      }
    })
  }, [vectors, site])



  const handleSliderChange = (event, newValue) => {
    setHour(newValue);
  };

  const handleDateChange = (newValue) => {
    setDate (newValue);
  };


  useEffect(() => {
    axios
      /*.get(`http://localhost:5000/visualizer/vector/${date.toISOString().substring(0, 10)}/${site}`)*/
      .get(`http://localhost:3000/visualizer/vectors`)
      .then(response => {
        console.log('promise fulfilled')
        setVectors(response.data)
      })
  }, [date, site])

  useEffect(() => {
    axios
      .get(`http://localhost:3000/visualizer/heat/${date.toISOString().substring(0, 10)}/${site}`)
      .then(response => {
        console.log(response.data)
        console.log("HERE!")
        setHeatdata(response.data)
      })
  }, [date, site])

  useEffect(() => {
    axios
      .get(`http://localhost:3000/visualizer/sitemeta/${site}`)
      .then(response => {
        console.log('Meta retrieved')
        setMeta(response.data)
      })
  }, [site])


  console.log('render', vectors.length, 'vectors')
  return (
    <Box sx={{ width: '100%' }}>
      <div className="heatmap_div" style={{height:"0px"}}/>
      <AppBar/>
      <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
        <Grid item xs={11}>
          <Chart options={options} hourlyheat={hourlyHeat} meta={meta}/>
          <Slider hour={hour} onChange={handleSliderChange}/>
        </Grid> 
        <Grid item xs={4}>
          <DatePicker date={date} onChange={handleDateChange}/>
        </Grid>
      </Grid>
    </Box>
  );

}

export default App; 
