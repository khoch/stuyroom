


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
    	    var thisDay = new Number();
	    thisDay = dates[index];
	    var datestring = new String();
	    datestring = year + "-" + month + "-" + thisDay;
	    //if not weekend
	    $(this).off();
	    if (!(index%7 == 0 || (index+1)%7 == 0)){	

		$(this).on("click", function(e){
		    $("#availrooms").empty();
		    $("#unavailrooms").empty();	
		    $(".active").toggleClass('active');
		    $(this).find('a').toggleClass('active');	
		    $(this).toggleClass('active');
		});
	    }
	    //get rid of days in previous month
    	    if ((index <= 7 && thisDay > 20) ||
    		(index >= 28 && thisDay < 20)
	       ){
    		$(this).toggleClass("off",true);
		//get rid of days that have passed
    	    } else if (year < date.getFullYear()){
		$(this).toggleClass("off",true);
	    } else if (month < date.getMonth() && year == date.getFullYear()){
		$(this).toggleClass("off",true);
	    } else if (!(index%7 == 0 || (index+1)%7 == 0)){
    		$(this).toggleClass("off",false);
		$(this).on("click", function(e){

		    calEvent(datestring);
		});
    	    } else {
		$(this).toggleClass("off",false);
	    }
    	    $(this).find('a').text(thisDay);
    	    index++;
    	})
    });
}

var date = new Date();
currentM = date.getMonth();
currentY = date.getFullYear();
fillCalendar(currentY, currentM);

var calEvent = function calEvent(dateString){
    availableRooms(dateString, function(rooms){
	for (var i = 0; i < rooms.length;i++){
	    $("#availrooms").append('<li><a href="reserve?rm=' + rooms[i]+ '&date=' + dateString+'">'
				    + rooms[i]  + '</a></li>');
	}
	$(".available").find("span").text("Available");
    });
    
    unavailableRooms(dateString, function(takenrooms){
	for (var i = 0; i < takenrooms.length; i++){
	    $("#unavailrooms").append('<li>' + takenrooms[i][0] + ' : ' + takenrooms[i][1] + '</li>');
	}
	$(".unavailable").find("span").text("Unavailable");
    });
}

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


function availableRooms(dstring,callback){
    //returns list of available rooms
    //console.log("!" + dstring);
    $.ajax({
	url: "/available",
	type: 'GET',
	dataType: 'json',
	data: {date: dstring},
	success: function(d){
	    console.log(d);
	    callback(d);
	},
	error: function(error){
	    console.log("geh");
	    console.log(error);
	}
    });

}




function unavailableRooms(dstring,callback){
    //returns 2d list of unavailable rooms + club using it

    $.ajax({
	url: "/taken",
	type: 'GET',
	dataType: 'json',
	data: {date: dstring},
	success: function(d){
	    console.log(d);
	    callback(d);
	},
	error: function(error){
	    console.log(error);
	}

    });

}



    




