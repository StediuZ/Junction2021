import React, {Component} from "react";
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';

function valuetext(value) {
    return `${value}°C`;
  }
  
  export default function DiscreteSlider() {
    return (
      <Box sx={{mr:4, ml:4}}>
        <Slider
          aria-label="Hour"
          defaultValue={0}
          getAriaValueText={valuetext}
          valueLabelDisplay="auto"
          step={1}
          marks
          min={0}
          max={23}
        />

      </Box>
    );
}