const NOTIF_TIME = 5000;
const ICON = {
    'on': "icon_on16.png",
    'off': "icon_off16.png"
};
const FINGERPRINTER_REGEX = {
	    'lookup.bluecava.com': "BLUECAVA",
	    'ds.bluecava.com': "BLUECAVA",
	    'inside-graph.com/ig.js': "INSIDEGRAPH",
	    'online-metrix.net': "THREATMETRIX",
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
	    'isingles.co.uk/js/fprint/_core.js': "ISINGLES",
	    'bbnaut.swf': "BBELEMENTS",
	    'pianomedia.eu.*novosense.swf': "PIANOMEDIA",
	    '(alipay|alibaba).*lsa.swf': "ALIPAY",
	    'mercadoli[b|v]re.*dpe-.*swf': "MERCADOLIBRE"
	};

var TOGGLE = true;

// Notifications
var shownotify = function (msg) {
	console.log(msg);
    // Test for notification support.
    if (window.webkitNotifications) {
		var notification = window.webkitNotifications
			.createNotification(chrome.extension.getURL("icon48.png"), 'FPDetective', msg);
        notification.show();
    	setInterval(function () {
            notification.cancel()
        }, NOTIF_TIME);
    }
};

// Notify and change extension's icon
var notify_and_change_icon = function(notif_msg, new_icon) {
    shownotify(notif_msg);
	chrome.browserAction.setIcon({
        path: new_icon
	});
};

// TOGGLE FPDetective extension by toolbar button
chrome.browserAction.onClicked.addListener(function (tab) {
    TOGGLE = !TOGGLE;
    if (TOGGLE) {
		notify_and_change_icon("FPDetective extension enabled.", ICON['on']);
    } else {
		notify_and_change_icon("FPDetective extension disabled.", ICON['off']);
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
                    shownotify("FP script detected: " + details.url);
                    return;
	    		}
            }
        }
    }, 
  { urls: ["*://*/*"] }
);
