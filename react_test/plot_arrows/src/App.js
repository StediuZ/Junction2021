import React, {Component, useState, useEffect} from "react";
import axios from 'axios';
import './App.css';
import Chart from './Chart'
import Slider from './Slider'
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';


function App () {
  const [vectors, setVectors] = useState({});
  useEffect(() => {
    console.log('effect')
    axios
      .get('http://localhost:3001/notes')
      .then(response => {
        console.log('promise fulfilled')
        setVectors(response.data)
      })
  }, [])
  console.log('render', vectors.length, 'vectors')
  return (
    <Box sx={{ width: '100%' }}>
      <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
        <Grid item xs={9}>
          <Chart/>
        </Grid> 
        <Grid item xs={9}>
          <Slider/>
        </Grid>
      </Grid>
    </Box>
  );

}

export default App; 
