const {Cc, Ci, Cr} = require("chrome");
const self = require("sdk/self");
const data = self.data;
const notif = require("notifications");
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

// Interface
// ------------------------------------------------------------------

// Create a widget, and attach the panel to it, so the panel is
// shown when the user clicks the widget.
var widget = require("sdk/widget").Widget({
    label: "FPDetectiveExtension",
    id: "fpd-panel",
    contentURL: data.url("icon_on16.png"),
    onClick: function () {
        TOGGLE = !TOGGLE;
        if (TOGGLE) {
            widget.contentURL = data.url("icon_on16.png");
        } else {
            widget.contentURL = data.url("icon_off16.png");
        }
    }
});

// ------------------------------------------------------------------

// Initialize observer service
var observerService = Cc["@mozilla.org/observer-service;1"].getService(Ci.nsIObserverService);

function TracingListener() {
    this.originalListener = null;
}

// Request observer
var httpRequestObserver = {
    observe: function (aSubject, aTopic, aData) {
        var httpChannel = aSubject.QueryInterface(Ci.nsIHttpChannel);
        if ("http-on-modify-request" == aTopic) {
            var url = httpChannel.originalURI.spec;
            if (TOGGLE) {
                for (var reg_str in FINGERPRINTER_REGEX) {
                    // Build reg expression
                    var re = new RegExp(reg_str, "g");
                    if (url.match(re)) {
						notif.notify({
                            title: "FPDetective: FP script detected",
                            text: "A FP script by " + FINGERPRINTER_REGEX[reg_str] + " has been detected: " + url
                        });
                        //aSubject.cancel(Cr.NS_BINDING_ABORTED); // Cancel request TODO: fix if uncommented notification won't pop up!
						return;
                    }
                }
            }
        }
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

exports.main = function () {
    console.log("FPDetective addon is running...");
};

// Unload addon event
exports.onUnload = function (reason) {
    // Unregister service
    observerService.removeObserver(httpRequestObserver, "http-on-modify-request");
};
