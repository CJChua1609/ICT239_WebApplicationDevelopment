function drawChart(chartData) {
    var elem = document.getElementById('myChart');
    const ctx = document.getElementById('myChart');
    
    // retrieving chartData from backend
    // chartData = JSON.parse(chartData);
    var xLabels = chartData.labels;
    var charts = chartData.charts;
    // convert the time into string for time chart
    
    for (const [key, values] of Object.entries(charts)) {
        charts[key] = values.map(value => {
            let d = new Date(value + '+8'); // GMT+8
            let year = d.getFullYear();
            let month = ('' + (d.getMonth() + 1)).padStart(2, '0');
            let day = ('' + d.getDate()).padStart(2, '0');
            let hour = ('' + d.getHours()).padStart(2, '0');
            let mins = ('' + d.getMinutes()).padStart(2, '0');
            return (year + '-' + month + '-' + day + ' ' + hour + ':' + mins + ':00');
        })
    }
    


    var vLabels = []; // ['flight1','flight2','flight3',...]
    var vData = []; // [ [{x; ,y: }], [],...]

    for (const [key, values] of Object.entries(charts)) {
        let xy = [] // time needs a pair
        vLabels.push(key) // Flight 1
        for (let i = 0; i < values.length; i++) {
            xy.push({ 'x': charts[key][i], 'y': xLabels[i] }) // x: Flight 1 data i, y: Hole i
        }
        console.log(xy)
        vData.push(xy)
    }
    console.log(2)
    // defining and generating graph
    var myChart = new Chart(ctx, {
        type: "line",
        data: {
            // labels: xLabels,
            datasets: []
        },
        options: {
            responsive: true,
            maintainaspectratio: false,
            
            scales: {
                x: {
                    offset : true,
                    type: 'time',
                    time: {
                        unit: 'hour',
                    },
                    ticks :{
                        stepSize: 10,
                        major: {
                            enabled: true
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    type: 'category',
                    grid: {
                        borderColor: "rgba(249, 238, 236, 0.74)"
                    },
                    reverse: true,
                    
                }
            }
            
            
        }
    });
    console.log(3)
    // push values to graph
    for (i= 0; i < vLabels.length; i++ ) {
        myChart.data.datasets.push({
            label: vLabels[i], 
            type: "line",
            borderColor: '#' + (0x1100000 + Math.random() * 0xffffff).toString(16).substr(1, 6),
            backgroundColor: "rgba(249, 238, 236, 0.74)",
            data: vData[i], 
            spanGaps: true
        }); 
        myChart.update();
    }
    

    
}


function myFunc() {
    $.ajax({
        url:"/chart?a=" + document.getElementById('mySelect').value,
        type: "POST",
    
      //   dataType: 'json',   //you may use jsonp for cross origin request
      //   crossDomain: true,
        error: function() {
          alert("Error");
        },
        success: function(data, status, xhr) { 
        // get chart canvas, prevent duplicate graph
		let width = $('#myChart').width(); 
		let height = $('#myChart').height();
		$('#myChart').remove(); // this is my <canvas> element
		$('#myChartPlaceHolder').append('<canvas id="myChart"><canvas>');
		var canvas = document.querySelector('#myChart');
		var ctx = canvas.getContext('2d');
		//var ctx = document.getElementById("myChart").getContext("2d");
		ctx.canvas.width = width; 
		ctx.canvas.height = height;


            console.log("success chart plotting")
            drawChart(data) //call draw chart function
      }})
}
