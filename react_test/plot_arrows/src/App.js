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


function App () {
  const [vectors, setVectors] = useState({});
  const [hour, setHour] = useState(0);
  const [date, setDate] = useState(new Date('2021-08-05T21:11:54'));
  const [site, setSite] = useState(1)



  const handleSliderChange = (event, newValue) => {
    setHour(newValue);
  };

  const handleDateChange = (newValue) => {
    setDate (newValue);
  };


  useEffect(() => {
    console.log('effect')
    axios
      .get(`http://localhost:5000/visualizer/vector/${date.toISOString().substring(0, 10)}/${site}`)
      .then(response => {
        console.log('promise fulfilled')
        setVectors(response.data)
      })
  }, [date])


  console.log('render', vectors.length, 'vectors')
  return (
    <Box sx={{ width: '100%' }}>
      <AppBar/>
      <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
        <Grid item xs={11}>
          <Chart/>
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
