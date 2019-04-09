var currentFile = "";
var globalLabels = [];
var globalData1 = [];
var globalData2 = [];
var globalWhich = 0;
function handleFiles(files, which) {
    // Check for the various File API support.
    globalWhich = which;
    if (window.FileReader) {
        // FileReader are supported.
        getAsText(files[0]);
        currentFile = files[0].name;
    } else {
        alert('FileReader are not supported in this browser.');
    }
}

function getAsText(fileToRead) {
    var reader = new FileReader();
    // Read file into memory as UTF-8
    reader.readAsText(fileToRead);
    var fileToReadName = "" + fileToRead.name;
    // Handle errors load
    reader.onload = loadHandler;
    reader.onerror = errorHandler;
}

function loadHandler(event) {
    var csv = event.target.result;
    processData(csv);
}

function formattedDate(date) {
    var day = "0" + date.getDate();
    var month = "0" + (date.getMonth() + 1);
    var year = date.getFullYear();
    return day.substr(-2) + '.' + month.substr(-2) + '.' + year;
}

function formattedTime(date) {
    var hours = date.getHours();
    var minutes = "0" + date.getMinutes();
    var seconds = "0" + date.getSeconds();
    return hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
}

function processData(csv) {
    var allTextLines = csv.split(/\r\n|\n/);
    var lines = [];
    var linesDict = {};
    var header = allTextLines[0].split(',');
    var globalData;
    if (globalWhich === 1) {
        globalData = globalData1;
    } else {
        globalData = globalData2;
    }
    console.log("header", header);
    var cumulative = 0;
    for (var i = 1; i < allTextLines.length; i++) {
        var data = allTextLines[i].split(',');
        var tarr = {};
        for (var j = 0; j < data.length; j++) {
            tarr[header[j]] = data[j];
        }
        var date = new Date(tarr["Timestamp"] * 1000);
        tarr["DateRaw"] = date;
        tarr["Date"] = formattedDate(date);
        tarr["Time"] = formattedTime(date);
        cumulative = Math.floor(cumulative/1.5 + parseFloat(tarr["Value"]));
        tarr["Cumulative"] = cumulative;
        lines.push(tarr);
        linesDict[tarr["Date"] + "/" + tarr["Time"]] = tarr;
    }
    console.log(lines);
    //console.log("LinesDict",linesDict);

    // plot("spo2", [{x:"12:50",y:10}, {x:"12:55",y:18},{x:"13:00",y:15},{x:"15:50",y:10}])
    console.log("Current File", currentFile);
    var plotName = "undefined";
    try {
        plotName = currentFile.split("_")[2];
    } catch (err) {

    }
    ;
    if (currentFile.toLowerCase().indexOf("spo2") > -1)
        plotName = "Оксигенация";
    if (currentFile.toLowerCase().indexOf("steps") > -1)
        plotName = "Шаги";
    if (currentFile.toLowerCase().indexOf("activity") > -1)
        plotName = "Активность";
    if (currentFile.toLowerCase().indexOf("bperf") > -1)
        plotName = "Перфузия";
    if (currentFile.toLowerCase().indexOf("_hr_") > -1)
        plotName = "Пульс";
    if (currentFile.toLowerCase().indexOf("_ee_") > -1)
        plotName = "Калории";
    if (currentFile.toLowerCase().indexOf("_rr_") > -1)
        plotName = "Дыхание";
    if (currentFile.toLowerCase().indexOf("_hrv_") > -1)
        plotName = "Равномерность Пульса";
    if (globalLabels.length === 0) {
        for (var i = 0; i < lines.length; i++) {
            if (lines[i]["Time"].substr(-4) === "0:00" || lines[i]["Time"].substr(-4) === "5:00") {
                globalLabels.push(lines[i]["Date"] + "/" + lines[i]["Time"]);
            }
        }
    }
    var localData = [];
    var prevValue = 0
    var maxValue = 0;
    for (var i = 0; i < globalLabels.length; i++) {
        if (!(globalLabels[i] in linesDict)) {
            localData.push({x: i, y: prevValue});
        } else {
            var newValue = parseFloat(linesDict[globalLabels[i]]["Value"]);
            if (currentFile.toLowerCase().indexOf("steps") > -1)
                newValue = linesDict[globalLabels[i]]["Cumulative"];
            localData.push({x: i, y: newValue});
            prevValue = newValue;
            if (newValue > maxValue)
                maxValue = newValue;
        }
    }
    console.log(globalLabels, localData);
    var letters = '0123456789ABCDEF';
    var red = "" + Math.floor((Math.random() * 255));
    var green = "" + Math.floor((Math.random() * 255));
    var yAxis = "A";
    if (maxValue <= 20)
        yAxis = "B";
    if (maxValue <= 1)
        yAxis = "C";
    if (maxValue > 100)
        yAxis = "D";
    var newData = {
        label: plotName,
        data: localData,
        yAxisID: yAxis,
        backgroundColor: [
            'rgba(' + red + ',' + green + ', 132, 0.2)',
        ],
        borderColor: [
            'rgba(' + red + ',' + green + ', 132, 1)',

        ],
        borderWidth: 1
    };
    globalData.push(newData);
    plot(globalLabels, globalData, globalWhich)
}

function errorHandler(evt) {
    if (evt.target.error.name == "NotReadableError") {
        alert("Canno't read file !");
    }
}