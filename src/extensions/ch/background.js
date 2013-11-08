const notif_time = 4000;
const FINGERPRINTER_REGEX = {
    'lookup.bluecava.com': "BLUECAVA",
    'ds.bluecava.com/v50/AC/BCAC': "BLUECAVA",
    'inside-graph.com/ig.js': "INSIDEGRAPH",
    'h.online-metrix.net': "THREATMETRIX",
    'mpsnare.iesnare.com': "IOVATION",
    'device.maxmind.com': "MAXMIND",
    'maxmind.com/app/device.js': "MAXMIND",
    'analytics-engine.net/detector/fp.js': "ANALYTICSENGINE",
    'sl\d.analytics-engine.net/fingerprint': "ANALYTICSENGINE",
    'web-aupair.net/sites/default/files/fp/fp.js': "ANALYTICSENGINE",
    'coinbase\.com/assets/application\-[0-9a-z]{32}\.js': "COINBASE",
    'd3w52z135jkm97\.cloudfront\.net\/assets\/application\-[0-9a-z]{32}\.js': "COINBASE",
    'sbbpg=sbbShell': "SITEBLACKBOX",
    'tags.master-perf-tools.com/V\d+test/tagv\d+.pkmin.js': "PERFERENCEMENT",
    'mfc\d/lib/o-mfccore.js': "MYFREECAMS",
    'jslib/pomegranate.js': "MINDSHARE",
    'gmyze.com.*[fingerprint|ax].js': "AFKMEDIA",
    'cdn-net.com/cc.js': "CDNNET",
    'privacytool.org/AnonymityChecker/js/fontdetect.js': "ANONYMIZER",
    'analyticsengine.s3.amazonaws.com/archive/fingerprint.compiled.js': "ANALYTICSPROS",
    'dscke.suncorp.com.au/datastream-web/resources/js/fp/fontlist-min.js': "AAMI",
    'virwox.com/affiliate_tracker.js': "VIRWOX",
    'http://www.isingles.co.uk/js/fprint/_core.js': "ISINGLES"
};

var TOGGLE = true;

// Notifications
var shownotify = function (msg) {
    // Test for notification support.
    if (window.webkitNotifications) {
		var notification = window.webkitNotifications
			.createNotification('icon16.png', 'FPDetective', msg);
        notification.show();
    	setInterval(function () {
            notification.cancel()
        }, notif_time);
    }
};

// TOGGLE FPDetective extension by toolbar button
chrome.browserAction.onClicked.addListener(function (tab) {
    TOGGLE = !TOGGLE;
    if (TOGGLE) {
	console.log("***** FPDetective enabled.");
	shownotify("FPDetective addon enabled.");
        chrome.browserAction.setIcon({
            path: "icon_on16.png"
        });
    } else {
	console.log("***** FPDetective disabled.");
	shownotify("FPDetective addon disabled.");
        chrome.browserAction.setIcon({
            path: "icon_off16.png"
        });
    }
});

// Intercept 
chrome.webRequest.onBeforeRequest.addListener(
    function (details) {
        console.log(">> Request to " + details.url);
        if (TOGGLE) {
            for (var reg_str in FINGERPRINTER_REGEX) {
                // Build reg expression
            	var re = new RegExp(reg_str, "g");
            	if (details.url.match(re)) {
                    // Notify the user
                    console.log("***** FP script detected and blocked: " + details.url);
                    shownotify("FP script detected and blocked: " + details.url);
                    return {
                        cancel: true
                    };
	    	}
            }
        }
    }, 
  { urls: ["*://*/*"] }, ["blocking"]
);
