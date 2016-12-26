/*global console */

function createTable(tableData) {
    "use strict";
    var table, tableBody;

    // remove the old one
    table = document.getElementById("totals_table");
    if (typeof (table) !== 'undefined' && table !== null) {
        table.parentNode.removeChild(table);
    }

    // create it again
    table = document.createElement('table');
    table.id = "totals_table";
    tableBody = document.createElement('tbody');

    tableData.forEach(function (rowData) {
        var row;
        row = document.createElement('tr');

        rowData.forEach(function (cellData) {
            var cell = document.createElement('td');
            cell.appendChild(document.createTextNode(cellData));
            row.appendChild(cell);
        });
        tableBody.appendChild(row);
    });

    table.appendChild(tableBody);
    document.body.appendChild(table);
}

var numMin = function (time_start, time_end) {
    "use strict";
    var hours, total_min;
    time_start = parseInt(time_start, 10);
    time_end = parseInt(time_end, 10);
    if (time_start < 100) {
        time_start = time_start * 100;
    }
    if (time_end < 100) {
        time_end = time_end * 100;
    }
    hours = Math.floor(time_end / 100) - Math.floor(time_start / 100);
    total_min = hours * 60;
    total_min += time_end % 100;
    total_min -= time_start % 100;
    return total_min;
};

var minToHoursAndMin = function (minutes) {
    "use strict";
    var hours;
    hours = Math.floor(minutes / 60);
    minutes = minutes % 60;
    return [hours, minutes];
};

function getTotals(inputStr) {
    "use strict";
    var lines, i, line, tokens, timeStart, timeEnd, array1D, array2D, totalMin, hoursAndMin, totalTime, totalHrsAndMin;
    array2D = [];
    totalTime = 0;
    array2D.push(['line', 'hours', 'min', 'total hours', 'total min']);
    lines = inputStr.split("\n");
    for (i = 0; i < lines.length; i = i + 1) {
        line  = lines[i];
        if (line !== "" && !line.startsWith("#")) {
            tokens = line.match(/\S+/g);
            if (tokens.length === 2) {
                timeStart = tokens[0];
                timeEnd = tokens[1];
                totalMin = numMin(timeStart, timeEnd);
                totalTime = totalTime + totalMin;
                totalHrsAndMin = minToHoursAndMin(totalTime);
                hoursAndMin = minToHoursAndMin(totalMin);
                array1D = [line, hoursAndMin[0], hoursAndMin[1], totalHrsAndMin[0],
                        totalHrsAndMin[1]];
                array2D.push(array1D);
            }

        }
    }
    return array2D;
}

function main() {
    "use strict";
    var input;
    input = document.getElementById("time_in").value;
    createTable(getTotals(input));
    localStorage.setItem('time', input);
}


if (localStorage.getItem('time')) {
    var content = document.getElementById('time_in');
    content.value = localStorage.getItem('time');
}
