


var fillCalendar = function fillCalendar(year, month){
    //List of month names and the # of days in each month 
    var monthList = [["January",31],["February",28],["March",31],["April",30],["May",31],["June",30],["July",31],["August",31],["September",30],["October",31],["November",30],["December",31]];
  
    var d = new Date(year, month, 1);
    day = d.getDay(); //day of week
    var numDays = monthList[month][1];
    $("#month").text(monthList[month][0] + " " + year);
    
    //handles leap years
    if (month == 1){
    	if (new Date(year, 1, 29).getMonth() == 1){
    	    numDays = 29;
    	}
    }
    //fills list with correct dates
    dates = [];
    var n = 1 - day;
    for(var j = 0; j<42; j++){
    	if(n > numDays){
    	    n = 1;
    	}
    	if (n <= 0){
    	    dates[j] = monthList[(month+11)%12][1]+n;
    	} else {
    	    dates[j] = n;
    	}
    	n++;
    }
    //edits html table
    index = 0;
    $(".cal").each(function(){
    	$(this).find('td').each(function(){
    	    var d = dates[index];
    	    if ((index <= 7 && d > 20) ||
    		(index >= 28 && d < 20)
		){
		//get rid of days in previous month
    		$(this).toggleClass("off",true);
    	    } else if (year < date.getFullYear()){
		$(this).toggleClass("off",true);
	    } else if (month <= date.getMonth() && year == date.getFullYear()){
		//get rid of days that have passed
		$(this).toggleClass("off",true);
		if (month == date.getMonth()){
		    if( d >= date.getDate()){
			$(this).toggleClass("off",false);
		    }
		}
	    }else {
    		$(this).toggleClass("off",false);
    	    }
    	    $(this).find('a').text(d);
    	    index++;
    	})
    });
}

var date = new Date();
currentM = date.getMonth();
currentY = date.getFullYear();
fillCalendar(currentY, currentM);

var nextMonth = function(e){
    currentM++;
    if (currentM >= 12){
	currentM = currentM - 12;
	currentY++;
    }
    fillCalendar(currentY, currentM);
}
  
var prevMonth = function(e){
    currentM--;
    if (currentM < 0){
	currentM = currentM + 12;
	currentY--;
    }
    fillCalendar(currentY, currentM);
}



/****************************Things that we need from backend***********************************************/


var availableRooms = function availableRooms(month, day, year){
    //returns list of available rooms
    
    return [229,231,303,313,315,327,329,333,335,337,339,403,404,405,407,427,437,431] //just for now
}

var unavailableRooms = function unavailableRooms(month, day, year){
    //returns list of taken rooms
}



    




