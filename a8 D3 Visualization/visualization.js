'use strict';

//the SVG element to add visual content to
var svg = d3.select('#visContainer')
	.append('svg')
	.attr('height', 480)
	.attr('width', 1100)
	.style('border', '1px solid gray');

var MARGIN_SIZE = {
	left: 70,
	bottom: 70,
	top: 50,
	right: 120
}

//Use the SVG_SIZE and MARGIN_SIZE values to calculate the `width` and `height` 
//of the displayable area of the plot (where the circles will go)
var displayWidth = parseFloat(svg.attr('width')) - MARGIN_SIZE.left - MARGIN_SIZE.right;
var displayHeight = parseFloat(svg.attr('height')) - MARGIN_SIZE.bottom - MARGIN_SIZE.top;

var plot = svg.append('g')
	.attr('transform', 'translate(' + MARGIN_SIZE.left + ', ' + MARGIN_SIZE.top + ')')
	.attr('width', displayWidth)
	.attr('height', displayHeight)
	.attr("class", "areaClass");

var data;

var color = d3.scaleOrdinal().range(["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6",
	"#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499"]);

// add title and names
function addPreliminaries() {
	// Title
	d3.select('h1').text('Global Population over the years - 2009-2018');
	d3.select('head').select('title').text('Global Population over the years')

	// Names
	d3.select('.lead').text('Shreya Sabharwal, Sahil Aggarwal');
}

// create an array of specific range
function range(start, count) {
	return Array.apply(0, Array(count))
		.map(function (element, index) {
			return index + start;
		});
}

// update function to enter and exit elements for interactions
function update(data, xScale, yScale) {

	var minX = 2009;
	//place plotted areas
	var xData = range(minX, 10);

	// create data structure to use for interactions
	var areaData = [];
	data.forEach(function (row, index) {
		var singleLineData = []
		xData.forEach(function (item) {
			singleLineData.push(row['y' + item]);
		});
		areaData.push({ 'yData': singleLineData, 'countryName': row.countryName, 'region': row.region, 'seriesCode': row.seriesCode })
	});

	//join areas with the loaded data
	var areas = plot.selectAll('path').data(areaData);

	var areaFunction = d3.area()
		.x(function (d, i) { return xScale(xData[i]); })
		.y1(function (d) {
			return yScale(d);
		})
		.y0(displayHeight);

	// merge entering elements
	var present = areas.enter().append("path")
		.attr("stroke", 'black')
		.attr("stroke-width", 0.1)
		.style('fill-opacity', 0.5)
		.merge(areas);

	// add transition and attributes
	present.transition().duration(1000)
		.attr("d", function (d) { return areaFunction(d.yData) })
		.attr("fill", function (d, i) {
			return color(d.region);
		});

	present.append('title').text(function (d) {
		console.log(d.countryName);
		return ('Country: ' + d.countryName)
	});

	// mouseover, mouseout and onclick event handling
	present.on("mouseover", function () {
		// highlight elements
		d3.select(this)
			.attr("fill", "red")
			.style('fill-opacity', 1)
	}).on("mouseout", function (d, i) {
		//retain the original color on mouseout
		d3.select(this).style('fill-opacity', 0.5).attr("fill", function () {
			return "" + color(d.region) + "";
		});
	}).on("click", function (d) {
		// update data for clicked element
		var filteredData = data.filter(function (row) {
			return (row.countryName == d.countryName && row.seriesCode == d.seriesCode);
		});

		var scale = createScale(filteredData, false);
		var xScale = scale[0];
		var yScale = scale[1];
		drawAxis(xScale, yScale);
		update(filteredData, xScale, yScale);
	});

	areas.exit().remove();

	addLegend(color);

}

// create scale for x and y values
function createScale(data, islog) {
	// Maximum and minimum values of X and Y axes
	var minX = 2009;
	var maxX = 2018;
	// extract minimum value of y
	var tempYMin = []
	for (var i = minX; i <= maxX; i++) {
		var min = d3.min(data, function (d) {
			return parseFloat(d['y' + i]);
		});
		tempYMin.push(min);
	}

	var minY = d3.min(tempYMin);
	// get maximum value of y
	var tempYMax = []
	for (var i = minX; i <= maxX; i++) {
		var max = d3.max(data, function (d) {
			return parseFloat(d['y' + i]);
		});
		tempYMax.push(max);
	}

	var maxY = d3.max(tempYMax);

	// scale for x values
	var xScale = d3.scaleLinear()
		.domain([minX, maxX])
		.range([0, displayWidth]);

	// scale for y values
	var yScale;
	if (islog == true) {
		yScale = d3.scaleLog()
			.domain([minY, maxY])
			.range([displayHeight, 0]);
	} else {
		yScale = d3.scaleLinear()
			.domain([minY * 0.9, maxY])
			.range([displayHeight, 0]);
	}

	return [xScale, yScale]
}

// create axis based on x and y scaling
function drawAxis(xScale, yScale) {
	// create x axis
	var xAxis = d3.axisBottom(xScale).ticks(10, '.0f');

	var x = svg.selectAll(".x")
		.data(["dummy"]);

	var newX = x.enter().append("g")
		.attr("class", "x axis")
		.attr("transform", "translate(" + [MARGIN_SIZE.left, displayHeight + MARGIN_SIZE.top] + ")");

	x.merge(newX).call(xAxis);
	x.exit().remove();

	// create y axis
	var yAxis = d3.axisLeft(yScale).ticks(5, '.0f').tickFormat(d3.format('.3s'));

	var y = svg.selectAll(".y")
		.data(["dummy"]);

	var newY = y.enter().append("g")
		.attr("class", "y axis")
		.attr("transform", "translate(" + [MARGIN_SIZE.left, MARGIN_SIZE.top] + ")");

	y.merge(newY).call(yAxis);
	y.exit().remove();

	// x axis and y axis labels
	svg.append('text')
		.text('Years')
		.attr('transform', 'translate(' + (MARGIN_SIZE.left + displayWidth / 2.3) + ',' + (displayHeight + MARGIN_SIZE.top + 40) + ')');
	svg.append('text')
		.text('Population')
		.attr('transform', 'translate(' + (MARGIN_SIZE.left - 40) + ',' + (MARGIN_SIZE.top + 2 * displayHeight / 3.3 + 40) + ') rotate(-90)');

}

// fetch, filter and sort data
async function createplot() {
	addPreliminaries();

	// DATA PREPARATION
	data = await d3.csv('data/data.csv', function (row) {
		return {
			countryName: row['Country Name'],
			seriesName: row['Series Name'],
			seriesCode: row['Series Code'],
			region: row['Region'],
			y2009: +row['2009 [YR2009]'],
			y2010: +row['2010 [YR2010]'],
			y2011: +row['2011 [YR2011]'],
			y2012: +row['2012 [YR2012]'],
			y2013: +row['2013 [YR2013]'],
			y2014: +row['2014 [YR2014]'],
			y2015: +row['2015 [YR2015]'],
			y2016: +row['2016 [YR2016]'],
			y2017: +row['2017 [YR2017]'],
			y2018: +row['2018 [YR2018]'],
		}
	});

	data.columns = ['countryName', 'seriesName', 'seriesCode', 'region', 'y2009', 'y2010', 'y2011', 'y2012', 'y2013', 'y2014', 'y2015', 'y2016', 'y2017', 'y2018']
	// filter out columns having empty values
	data = data.filter(function (row) {
		var toRemove = data.columns.some(function (col) {
			return row[col] == ''
		});
		return (toRemove != true);
	});


	//sort data on the basis of population
	data.sort(function (a, b) {
		return d3.descending(+a.y2014, +b.y2014);
	});

	// filtering data for Total population of all countries
	var totalData = data.filter(function (row) {
		return (row.seriesCode == 'SP.POP.TOTL');
	});
	console.log(totalData.length);

	var scale = createScale(totalData, true);
	var xScale = scale[0];
	var yScale = scale[1];
	drawAxis(xScale, yScale);

	update(totalData, xScale, yScale);
}

// Submit button functionality
d3.select('#submit').on('click', function () {
	var cntryName = d3.select('#countryName').property('value');
	var gender = d3.selectAll("input[name='gender']:checked").property('value');
	var seriesCode, islog = false;
	if (gender === 'male') {
		seriesCode = 'SP.POP.TOTL.MA.IN'
	} else if (gender === 'female') {
		seriesCode = 'SP.POP.TOTL.FE.IN'
	} else {
		seriesCode = 'SP.POP.TOTL';
	}

	var filteredData = data.filter(function (row) {
		return (row.countryName.toLowerCase() === cntryName.toLowerCase() && row.seriesCode === seriesCode);
	});

	var scale = createScale(filteredData, islog);
	var xScale = scale[0];
	var yScale = scale[1];
	drawAxis(xScale, yScale);
	update(filteredData, xScale, yScale);
	//addLegend(color);

});

// Radio button functionality
d3.selectAll("input[name='gender']").on("change", function () {
	var gender = this.value;
	var cntryName = d3.select('#countryName').property('value');
	var seriesCode, islog;
	if (gender === 'male') {
		seriesCode = 'SP.POP.TOTL.MA.IN'
		islog = false;
	} else if (gender === 'female') {
		seriesCode = 'SP.POP.TOTL.FE.IN'
		islog = false;
	} else {
		seriesCode = 'SP.POP.TOTL';
		if (cntryName == "") {
			islog = true;
		} else {
			islog = false;
		}
	}
	// filtering data for Total population of all males
	var genderData = data.filter(function (row) {
		if (cntryName == "") {
			return (row.seriesCode == seriesCode)
		} else {
			return (row.seriesCode == seriesCode && row.countryName.toLowerCase() == cntryName.toLowerCase());
		}
	});

	var scale = createScale(genderData, islog);
	var xScale = scale[0];
	var yScale = scale[1];
	drawAxis(xScale, yScale);
	update(genderData, xScale, yScale);
});

// create legend
function addLegend(color) {
	var legendRectSize = 18;
	var legendSpacing = 4;

	var legendHolder = svg.append('g')
		// translate the holder to the right side of the graph
		.attr('transform', "translate(" + (MARGIN_SIZE.left + displayWidth + 10) + ",0)");

	var legend = legendHolder.selectAll('.legend')
		.data(color.domain());

	var present = legend.enter()
		.append('g')
		.attr('class', 'legend')
		.style('font-size', '8px')
		.attr('transform', function (d, i) {
			return "translate(0," + i * 20 + ")";
		}).merge(legend);

	present.append('rect')
		.attr('width', legendRectSize)
		.attr('height', legendRectSize)
		.style('fill', color)
		.style('stroke', color)
		.style('opacity', 0.5);

	present.append('text')
		.attr('x', legendRectSize + legendSpacing)
		.attr('y', legendRectSize - legendSpacing)
		.text(function (d) { return d; });
}

createplot();

