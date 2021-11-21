import React, {Component} from "react";
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';


  
  export default function DiscreteSlider(props) {
    return (
      <Box sx={{mr:4, ml:4}}>
        <Slider
          aria-label="Hour"
          value={props.value}
          onChangeCommitted={props.onChange}
          valueLabelDisplay="auto"
          step={1}
          marks
          min={0}
          max={23}
        />

      </Box>
    );
}