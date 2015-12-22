


var fillCalendar = function fillCalendar(year, month){
    var monthList = [["January",31],["February",28],["March",31],["April",30],["May",31],["June",30],["July",31],["August",31],["September",30],["October",31],["November",30],["December",31]];
    //^List of month names and the # of days in each month 

    var d = new Date(year, month, 1);
    day = d.getDay(); //day of week
    var numDays = monthList[month][1];
    $("#month").text(monthList[month][0] + " " + year);

    if (month == 1){
	//leapyear
    }      
   
    dates = [];
    var n = 1 - day;
    for(var j = 0; j<42; j++){
	if(n > numDays){
	    n = 1;
	}
	if (n <= 0){
	    dates[j] = monthList[month-1][1]+n;
	} else {
	    dates[j] = n;
	}
	n++;
    }

    index = 0;
    $("#cal").each(function(){
	$(this).find('td').each(function(){
	    var d = dates[index];
	    if ((index <= 7 && d > 20) ||
	       (index >= 28 && d < 20)){
		$(this).toggleClass("off",true);
	    } else {
		$(this).toggleClass("off",false);
	    }
	    $(this).text(d);
	    index++;
	})
    });
}
fillCalendar(2015,11);
