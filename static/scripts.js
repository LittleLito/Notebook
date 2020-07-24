function add_0(num) {
   if (num<=9) {
      return '0' + num
   }
   else {
      return num
   }
}

function getTime(){
   str = "Datetime："
   var p = document.getElementById("sy_time");
   time = new Date();
   year = add_0(time.getFullYear());
   month = add_0(time.getMonth() + 1);
   day = add_0(time.getDate());
   hour = add_0(time.getHours());
   minutes = add_0(time.getMinutes());
   seconds = add_0(time.getSeconds());
   str = str + year + "-" + month + "-" + day + " " + hour + ":" + minutes + ":" + seconds;
   p.innerText = str;
   setTimeout(getTime,1000);
}

window.onload = function(){
    getTime();
}
