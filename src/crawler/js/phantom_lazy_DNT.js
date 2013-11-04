// https://code.google.com/p/phantomjs/issues/attachmentText?id=351&aid=3510000000&name=iphone4S.js&token=CF9yuekhCQeCEaB8a9-YLGQdA_g%3A1367969992618
var WAIT_AFTER_LOAD = 10000;

var page = new WebPage(),
    address, output, size;

page.onResourceRequested = function (request) {
	console.log('requested: ' + request.url);
    console.log('request headers: ' + JSON.stringify(request, undefined, 4));
};
page.onResourceReceived = function (response) {
	console.log('received: ' + response.url);
    console.log('response headers: ' + JSON.stringify(response, undefined, 4));
};
page.customHeaders = {
	'DNT': '1'
};

if (phantom.args.length < 1 || phantom.args.length > 2) {
    console.log('You need to pass a URL and nothing else.');
    phantom.exit();
} else {
    address = phantom.args[0];
    page.settings = { 
        userAgent: 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1673.0 Safari/537.36',
        javascriptEnabled: true ,
        loadPlugins: false
        };
    
    console.log('opening url: ' + address + ',');
    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('Unable to load the address!');
        } else {
            window.setTimeout(function () {
            	console.log("Finished all steps!");
                phantom.exit();
            }, WAIT_AFTER_LOAD);
        }
    });
}