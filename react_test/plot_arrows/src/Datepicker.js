import * as React from 'react';
import DesktopDatePicker from '@mui/lab/DesktopDatePicker';
import DateAdapter from '@mui/lab/AdapterMoment';
import LocalizationProvider from '@mui/lab/LocalizationProvider';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';



export default function MaterialUIPickers(props) {

    return (
        <Box sx={{ml:5}}>
            <LocalizationProvider dateAdapter={DateAdapter}>
                <DesktopDatePicker
                    label="Date"
                    inputFormat="DD/MM/yyyy"
                    value={props.value}
                    onChange={props.onChange}
                    renderInput={(params) => <TextField {...params} />}
                />
            </LocalizationProvider>
        </Box>
        
    );
  }
  