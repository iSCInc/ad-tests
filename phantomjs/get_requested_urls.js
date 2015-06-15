var page = require('webpage').create();
var system = require('system');
var urls = Array();

page.onResourceRequested = function(request, networkRequest) { 
  if (system.args[1] == request.url) {
    return;
  } else {
    urls.push(request.url)
  }
};

page.onLoadFinished = function(status) {
  console.log(JSON.stringify(urls));
  setTimeout(function(){
    phantom.exit();
  }, 0);
};

page.onResourceError = function(){
  return false;
}

page.onError = function(){
  return false;
}

page.open(system.args[1]);
