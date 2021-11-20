
//Custom gradient config
// create configuration object
var config = {
  container: document.getElementById('heatmapContainer'),
  radius: 10,
  maxOpacity: .5,
  minOpacity: 0,
  blur: .75,
  gradient: {
    // enter n keys between 0 and 1 here
    // for gradient color customization
    '.5': 'blue',
    '.8': 'red',
    '.95': 'white'
  }
};
var heatmapInstance = h337.create(config);

var data = [

  {

    z: [[1, null, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, -10, 20]],
    x: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    y: ['Morning', 'Afternoon', 'Evening'],
    type: 'heatmap',
//define whether gaps on data have hover labels associated
    hoverongaps: true

  }

];