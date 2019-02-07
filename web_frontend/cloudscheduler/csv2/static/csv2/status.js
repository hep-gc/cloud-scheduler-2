var date = Date.now();

function initialize(){
	/* Add event listeners once page loads*/
	addEventListeners("plottable");
	addEventListeners("range");
}


/* Add click events to table elements and range selection*/
function addEventListeners(className) {
	var inputList = document.getElementsByClassName(className);
		var i;
		for (i = 0; i < inputList.length; i++){
			inputList[i].addEventListener('click', function(){
				if(className == 'plottable'){
					this.classList.toggle("plotted");
					togglePlot(this);
				}else selectRange(this);
			});
		}
}


/* Range selection dropdown*/
function dropDown(){
	document.getElementById("range-select").classList.toggle("selected");
	document.getElementById("myDropdown").classList.toggle("show");
}

/* Change time range for plot*/
function selectRange(range){
	const curr_range = document.getElementsByClassName("range-btn");
	curr_range[0].innerHTML = range.innerHTML+'<span class="space"></span><span class="caret"></span>';
	const dropdowns = document.getElementsByClassName("range");
	for (var i = 0; i < dropdowns.length; i++) {
		if (dropdowns[i].classList.contains('selected')) {
			dropdowns[i].classList.remove('selected');
      		}
	}
	range.classList.toggle("selected");
	/* Calculate new range*/
	var to = new Date();
	var from = new Date();
	var multiple = 60000;
	if(range.parentElement.classList.contains("days")) multiple = 86400000;
	to.setTime(date-(range.dataset.to*multiple))
	to = to.getTime();
	from.setTime(date-(range.dataset.from*multiple));
	from = from.getTime();
	/* Update plot with new range*/
	TSPlot.layout.xaxis.range = [from, to];
	Plotly.relayout('plotly-TS', TSPlot.layout);
}


/* Close the range dropdown menu*/
window.onclick = function(event) {
	if (!event.target.matches('.range-btn') && document.getElementsByClassName("dropdown-content")[0].classList.contains('show')) {
		var dropdowns = document.getElementsByClassName("dropdown-content");
		var k = false;
		var i;
		for (i = 0; i < dropdowns.length; i++) {
			var openDropdown = dropdowns[i];
			if (openDropdown.classList.contains('show')) {
				openDropdown.classList.remove('show');
				k = true;
	      		}
    		}
		if(k == true){
			document.getElementById("range-select").classList.toggle("selected");
		}
	}
}


/* Toggle traces, show plot*/
function togglePlot(trace){
	if(TSPlot.showing == true){
		/* Check if trace is already plotted*/
		var x;
		var index = -1;
		for(x = 0; x < TSPlot.traces.length; x++){
			if (TSPlot.traces[x].name == trace.dataset.path){
				index = x;
				break;
			}
		}
		if(index != -1){
			if(TSPlot.traces.length == 1) {
				TSPlot.hide();
			}else{
				Plotly.deleteTraces('plotly-TS', index);
				/* Store plotted traces for refresh*/
				var trace_array = [];
				for(var y = 0; y < TSPlot.traces.length; y++){
					trace_array.push(TSPlot.traces[y].name)
				}
				sessionStorage.setItem("traces", JSON.stringify(trace_array));
			}
		}else{
			/* Plot new trace*/
			getTraceData(trace, true);
		}
	}else{
		document.getElementById("loader").style.display = 'inline-block';		
		/* Create plot*/
		TSPlot.show();
		getTraceData(trace, false);
	}
}


/* Construct query for db*/
function createQuery(trace,time){
	const line = trace.split(" ");
	const group = line[0];
	var query = `SELECT time,value FROM `;
	if(line.length == 3){
		var cloud = line[1];
		var measurement = line[2];
		query += `"${measurement}" WHERE "cloud"='${cloud}' AND "group"='${group}'`;
	}else{
		var measurement = line[1];
		query += `"${measurement}" WHERE "group"='${group}'`;
	}if (time == true){
		query += `AND time > ${TSPlot.layout.xaxis.range[1]}ms`;
	}
	return query;
}


/* Fetch trace data from db and add to plot*/
function getTraceData(trace, showing){
	if(window.location.pathname == "/cloud/status/") var newpath = "plot";
	else var newpath = "/cloud/status/plot";
	query = createQuery(trace.dataset.path, false);
	const csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	fetch(newpath,{
		method: 'POST',
		headers: {'Accept': 'application/json', 'X-CSRFToken': csrftoken},
		credentials: 'same-origin',
		body: query,
		}
	)
	.then(function(response){
		/* Check response status code*/
		if(response.ok){
			return response.json();
		}throw new Error('HTTP response not was not OK. '+response.status);
	})
	.then(function(data){
		/* Parse response into trace object*/
		const responsedata = data.results[0].series[0].values;
		const unpackData = (arr, index) => {
			var newarr = arr.map(x => x[index]);
			return newarr
		}
	    	const newtrace = {
			type: 'scatter',
			name: trace.dataset.path,
			x: unpackData(responsedata, 0),
			y: unpackData(responsedata, 1)
		}
		/* If plot is showing, add trace to plot, otherwise create plot with trace*/
		if(showing == true) return Plotly.addTraces('plotly-TS', newtrace);
		else return TSPlot.initialize(newtrace);
	}).then(function(data){
		if(showing == true){
			/* Store plotted traces for refresh*/
			var trace_array = [];
			for(var y = 0; y < TSPlot.traces.length; y++){
				trace_array.push(TSPlot.traces[y].name)
			}
			sessionStorage.setItem("traces", JSON.stringify(trace_array));
		}
	})
	.catch(error => console.log('Error:', error));
}


/* On refresh, check for plotted traces to update colour in status table*/
function checkForPlottedTraces(){
	if (typeof(Storage) !== "undefined"){
		if(sessionStorage.length != 0){
			var traces = sessionStorage.getItem("traces").split(",");
			if(traces.length == 1){
				var plotted_traces = sessionStorage.getItem("traces");
				var stat = document.querySelectorAll('td[data-path='+plotted_traces+']');
				stat[0].classList.toggle("plotted");
			}
			else{
				var plotted_traces = JSON.parse(sessionStorage.getItem("traces"));
				for(var x = 0; x < plotted_traces.length; x++){
					var stat = document.querySelectorAll('td[data-path="'+plotted_traces[x]+'"]');
					stat[0].classList.toggle("plotted");
				}
			}
		}
	}
}


/* Refresh plot every 30 seconds with new data from db*/
//var plot_timer;
function refresh_plot() {
	if(TSPlot.showing == true){
		/* Only refresh if plot is showing and current range is Last hour or less*/
		if((TSPlot.layout.xaxis.range[1] - TSPlot.layout.xaxis.range[0]) <= 3600000 && (TSPlot.layout.xaxis.range[1] >= date)){
			var traces = TSPlot.traces;
			var newdata = {
				y: [],
				x: []
			};
			var index = [];
			var query = createQuery(traces[0].name,true)
			index.push(0);
			/* Create string of queries for db*/
			for (var i = 1; i < traces.length; i++){
				index.push(i);
				query += ';'
				query += createQuery(traces[i].name,true)
			}
			const csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
			fetch('cloud/status/plot',{
				method: 'POST',
				headers: {'Accept': 'application/json', 'X-CSRFToken': csrftoken},
				credentials: 'same-origin',
				body: query,
				}
			)
			.then(function(response){
				/* Check response status code*/
				if(response.ok){
					return response.json();
				}throw new Error('HTTP response not was not OK. '+response.status)
			})
			.then(function(data){
				/* Parse response into arrays of new points*/
				var new_points = true;
				for(var k = 0; k < traces.length; k++){
					if(!(typeof (data.results[k]) !== 'undefined') || !(typeof (data.results[k].series) !== 'undefined')){
						new_points = false;
						break;
					}
					const responsedata = data.results[k].series[0].values;
					const unpackData = (arr, index) => {
						var newarr = arr.map(x => x[index]);
						return newarr
					}
					var updatetrace = {
						x: unpackData(responsedata, 0),
						y: unpackData(responsedata, 1)
					}
				
					/* Update new data for traces*/
					newdata.y.push(unpackData(responsedata, 1));
					newdata.x.push(unpackData(responsedata, 0));
				}
				/* Update plot with new data*/
				if(new_points == true) return updateTraces(newdata, index);
				else return;
			})
			.catch(error => console.log('Error:', error));
		}					
	}
}


/* Update plot traces with most recent data points and new range*/
function updateTraces(newdata, index){
	Plotly.extendTraces('plotly-TS', newdata, index);
	date = Date.now();
	var diff = date - TSPlot.layout.xaxis.range[1];
	TSPlot.layout.xaxis.range[1] = date; 
	TSPlot.layout.xaxis.range[0] += diff;
	Plotly.relayout('plotly-TS', TSPlot.layout);
}


/* Plot Object*/
var TSPlot = {
	layout: {
		yaxis: {
			rangemode: "tozero"
		},
		xaxis: {
			type: 'date',
		},
		margin: {
			l: 50,
			r: 50,
			t: 40,
			b: 40
		}
	},

	showing: false,
	traces: [],

	/* Create new plot with trace in div*/
	initialize: function(trace) {
		var to = date;
		var from = new Date();
		from = from.setTime(to-3600000);
		TSPlot.layout.xaxis.range = [from, to];
		TSPlot.traces = [trace];		
		Plotly.newPlot('plotly-TS', TSPlot.traces, TSPlot.layout, {responsive: true, displayModeBar: false});
		sessionStorage.setItem("traces", JSON.stringify(trace.name));
	},

	/* Hide plot*/
	hide: function() {
		TSPlot.showing = false;
		TSPlot.traces = [];
		Plotly.purge('plotly-TS');
		document.getElementById("plot").style.display = 'none';
		const curr_range = document.getElementsByClassName("range-btn");
		curr_range[0].innerHTML = 'Last 1 hour<span class="space"></span><span class="caret"></span>';
		/* Remove indication of plotted traces*/
		var list = document.getElementsByClassName('plotted');
		var init_length = list.length;
		for (var i = 0; i < init_length; i++) {
			var value = list[0];
			value.classList.remove('plotted');
		}
		sessionStorage.clear();
	},

	/* Show plot*/
	show: function(){
		TSPlot.showing = true;
		document.getElementById("plot").style.display = 'block';
	}

}//TSPlot

	
