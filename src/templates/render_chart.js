
function interpret_data()
{
    //Loop through the json file
    //Convert the datetime from epoch to an actual timestamp
        //Formated sumthin like this Tuesday, January 4, 2022 8:30:00 AM
    //going to return a list of objects that have the information in the order
    //x, o, h, l, c

    //var mydata = JSON.parse(__filenamewithout .json__);
    // alert(mydata[0].name);
    // alert(mydata[0].age);
    // alert(mydata[1].name);
    // alert(mydata[1].age);
}

function render()
{
    //Code templated from https://www.youtube.com/channel/UCojXvfr41NqDxaPb9amu8-A
    const data = {
        //labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
            data: [
                {
                    x: startingdate,
                    o: opening,
                    h: high,
                    l: low,
                    c: close
                }
            ]
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
}