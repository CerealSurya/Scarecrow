//Code made from https://www.youtube.com/channel/UCojXvfr41NqDxaPb9amu8-A

const data = {
    //labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [{

    }]
  };

  // config 
  const config = {
    type: 'sticklestick',
    data,
    options: {}
  };

  // render init block
  const myChart = new Chart(
    document.getElementById('myChart'),
    config
);