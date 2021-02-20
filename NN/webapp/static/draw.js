var canvas;
var context;
var clickX = new Array();
var clickY = new Array();
var clickDrag = new Array();
var paint = false;
var curColor = "#111111";
/**
    - Preparing the Canvas : Basic functions
**/
function drawCanvas(){

    canvas = document.getElementById('canvas');
    context = document.getElementById('canvas').getContext("2d");

    $('#canvas').mousedown(function (e) {
        var rect = this.getBoundingClientRect();
        var mouseX = e.pageX - rect.left;
        var mouseY = e.pageY - rect.top;

        paint = true;
        addClick(e.pageX - rect.left, e.pageY - rect.top);
        redraw();
    });

    $('#canvas').mousemove(function (e) {
      var rect = this.getBoundingClientRect();
        if (paint) {
            addClick(e.pageX - rect.left, e.pageY - rect.top, true);
            redraw();
        }
    });

    $('#canvas').mouseup(function (e) {
        paint = false;
    });
}

/**
    - Saves the click postition
**/
function addClick(x, y, dragging) {
    clickX.push(x);
    clickY.push(y);
    clickDrag.push(dragging);
}

/**
    - Clear the canvas and redraw
**/
function redraw() {

    context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
    context.strokeStyle = curColor;
    context.lineJoin = "round";
    context.lineWidth = 6;
for (var i = 0; i < clickX.length; i++) {
    context.beginPath();
    if (clickDrag[i] && i) {
        context.moveTo(clickX[i - 1], clickY[i - 1]);
    } else {
        context.moveTo(clickX[i] - 1, clickY[i]);
    }
    context.lineTo(clickX[i], clickY[i]);
    context.closePath();
    context.stroke();
}
}

function erase(){
  context.clearRect(0, 0, canvas.width, canvas.height);
  clickX=[];
  clickY=[];
  clickDrag=[];
  document.getElementById("answer").hidden = true;
}

$("document").ready(function(){
    $("#send").click(function(){
      var image = new Image();
      image.id = "pic";
      image.src = canvas.toDataURL("image/png");
      $.ajax({
          url: '/canvas',
          type: "post",
          contentType: "application/json",
          data: JSON.stringify({"data": image.src})
        }).done(function(data) {
            document.getElementById("answer").hidden = false;
            document.getElementById("answer").innerHTML = "Your digit is "+data.result;
          });
                });
});
