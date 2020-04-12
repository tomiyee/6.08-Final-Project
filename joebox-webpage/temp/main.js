function start() {
  console.log("Starting...");
  window.setInterval(loop, 2000);
}
window.onload = start;
function loop() {
  console.log("Looping!");
}
function clickHandling() {
  $('p').hide();
}
