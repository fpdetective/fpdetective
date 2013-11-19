const {Cc, Ci, Cr} = require("chrome");
const self = require("sdk/self");
const data = self.data;
const notif = require("notifications");
const observerService = Cc["@mozilla.org/observer-service;1"]
	.getService(Ci.nsIObserverService);
	
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

// Interface
// ------------------------------------------------------------------
// Show a toast-like notification
// Create a widget, and attach the panel to it, so the panel is
// shown when the user clicks the widget.
var widget = require("sdk/widget").Widget({
    label: "FPDetectiveExtension",
    id: "fpd-panel",
    contentURL: data.url(ICON['on']),
    onClick: function () {
        TOGGLE = !TOGGLE;
        if (TOGGLE) {
            notify_and_change_icon("FPDetective extension enabled.", ICON['on']);
        } else {
            notify_and_change_icon("FPDetective extension disabled.", ICON['off']);
        }
    }
});

var notify = function (notif_msg) {
    notif.notify({
        title: "FPDetective",
        text: notif_msg
    });
};

// Notify and change extension's icon
var notify_and_change_icon = function(notif_msg, new_icon) {
    notify(notif_msg);
    widget.contentURL = data.url(new_icon);
};

// Main function
// ------------------------------------------------------------------
exports.main = function () {
	// Define HTTP requests observer
	var httpRequestObserver = {
		// Return true if a FP script is detected in an HTTP request, false otherwise
		observe: function (aSubject, aTopic, aData) {
		    var httpChannel = aSubject.QueryInterface(Ci.nsIHttpChannel);
		    if (TOGGLE && "http-on-modify-request" == aTopic) {
		        var url = httpChannel.originalURI.spec;
		        for (var reg_str in FINGERPRINTER_REGEX) {
		            // Build reg expression
		            var re = new RegExp(reg_str, "g");
		            if (url.match(re)) {
		                notify("A FP script by " + FINGERPRINTER_REGEX[reg_str] + " has been detected: " + url);
		                return true;
		            }
		        }
		    }
			return false;
		},
		QueryInterface: function (aIID) {
		    if (aIID.equals(Ci.nsIObserver) || aIID.equals(Ci.nsISupports)) {
		        return this;
		    }
		    throw Cr.NS_NOINTERFACE;
		}
	};

	// Register service
	observerService.addObserver(httpRequestObserver,
	    "http-on-modify-request", false);
};

// Unload addon event
exports.onUnload = function (reason) {
    // Unregister service
    observerService.removeObserver(httpRequestObserver, "http-on-modify-request");
};
