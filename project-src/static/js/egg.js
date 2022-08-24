var count = 0 ;
var egg = new Egg("e,n,c,i,p,h,e,r,r", function() {
    console.log("Easter egg triggered");
    count+=1 ;
    if (count <=1) {$("body").load("./static/eg.html");count+=1}
    else {location.reload();}
}).listen();

//https://type.fit/api/quotes