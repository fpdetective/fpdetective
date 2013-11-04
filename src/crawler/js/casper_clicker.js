var fs = require("fs");
phantom.casperPath = fs.workingDirectory + "/../../../run/bins/casperjs"; // from test dir
if (!phantom.injectJs(phantom.casperPath + '/bin/bootstrap.js')){
	phantom.casperPath = fs.workingDirectory + "/../../run/bins/casperjs"; // src/crawler dir
	if (!phantom.injectJs(phantom.casperPath + '/bin/bootstrap.js')){
		console.log("Cannot find casperjs module, quitting...");
		phantom.exit();	
	}
}

var links_to_click = [];
var MAX_LINKS_TO_CLICK = 25;
var MAX_DURATION_PER_LINK = 10000; // will click link and wait at most for 10 seconds
var TIMEOUT_TOLERANCE = 2000;
var WAIT_AFTER_LOAD = 10000;
var WAIT_AFTER_RELOAD = 1000;
var WAIT_AFTER_CLICK = 5000;

var LINK_LABELS = ['Sign In', 'Sign Up', 'Sign On', 'Register', 'Login', 'Log-in', 'Log-on', 'Sign'];
var LINK_URLS = ['login', 'logon', ' sign', 'register', 'subscri', 'log-in', 'log-on', 'join', 'sell', 'member',
                   'auth', 'account', 'user', 'password', 'store', 'shop', 'my'];
                   
var MAX_SCRIPT_DURATION = MAX_LINKS_TO_CLICK  * MAX_DURATION_PER_LINK;

var TLDs = ["ac", "ad", "ae", "aero", "af", "ag", "ai", "al", "am", "an", "ao", "aq", "ar", "arpa", "as", "asia", "at", "au", "aw", "ax", "az", "ba", "bb", "bd", "be", "bf", "bg", "bh", "bi", "biz", "bj", "bm", "bn", "bo", "br", "bs", "bt", "bv", "bw", "by", "bz", "ca", "cat", "cc", "cd", "cf", "cg", "ch", "ci", "ck", "cl", "cm", "cn", "co", "com", "coop", "cr", "cu", "cv", "cx", "cy", "cz", "de", "dj", "dk", "dm", "do", "dz", "ec", "edu", "ee", "eg", "er", "es", "et", "eu", "fi", "fj", "fk", "fm", "fo", "fr", "ga", "gb", "gd", "ge", "gf", "gg", "gh", "gi", "gl", "gm", "gn", "gov", "gp", "gq", "gr", "gs", "gt", "gu", "gw", "gy", "hk", "hm", "hn", "hr", "ht", "hu", "id", "ie", "il", "im", "in", "info", "int", "io", "iq", "ir", "is", "it", "je", "jm", "jo", "jobs", "jp", "ke", "kg", "kh", "ki", "km", "kn", "kp", "kr", "kw", "ky", "kz", "la", "lb", "lc", "li", "lk", "lr", "ls", "lt", "lu", "lv", "ly", "ma", "mc", "md", "me", "mg", "mh", "mil", "mk", "ml", "mm", "mn", "mo", "mobi", "mp", "mq", "mr", "ms", "mt", "mu", "museum", "mv", "mw", "mx", "my", "mz", "na", "name", "nc", "ne", "net", "nf", "ng", "ni", "nl", "no", "np", "nr", "nu", "nz", "om", "org", "pa", "pe", "pf", "pg", "ph", "pk", "pl", "pm", "pn", "pr", "pro", "ps", "pt", "pw", "py", "qa", "re", "ro", "rs", "ru", "rw", "sa", "sb", "sc", "sd", "se", "sg", "sh", "si", "sj", "sk", "sl", "sm", "sn", "so", "sr", "st", "su", "sv", "sy", "sz", "tc", "td", "tel", "tf", "tg", "th", "tj", "tk", "tl", "tm", "tn", "to", "tp", "tr", "travel", "tt", "tv", "tw", "tz", "ua", "ug", "uk", "us", "uy", "uz", "va", "vc", "ve", "vg", "vi", "vn", "vu", "wf", "ws", "xn--0zwm56d", "xn--11b5bs3a9aj6g", "xn--3e0b707e", "xn--45brj9c", "xn--80akhbyknj4f", "xn--90a3ac", "xn--9t4b11yi5a", "xn--clchc0ea0b2g2a9gcd", "xn--deba0ad", "xn--fiqs8s", "xn--fiqz9s", "xn--fpcrj9c3d", "xn--fzc2c9e2c", "xn--g6w251d", "xn--gecrj9c", "xn--h2brj9c", "xn--hgbk6aj7f53bba", "xn--hlcj6aya9esc7a", "xn--j6w193g", "xn--jxalpdlp", "xn--kgbechtv", "xn--kprw13d", "xn--kpry57d", "xn--lgbbat1ad8j", "xn--mgbaam7a8h", "xn--mgbayh7gpa", "xn--mgbbh1a71e", "xn--mgbc0a9azcg", "xn--mgberp4a5d4ar", "xn--o3cw4h", "xn--ogbpf8fl", "xn--p1ai", "xn--pgbs0dh", "xn--s9brj9c", "xn--wgbh1c", "xn--wgbl6a", "xn--xkc2al3hye2a", "xn--xkc2dl3a5ee0h", "xn--yfro4i67o", "xn--ygbi2ammx", "xn--zckzah", "xxx", "ye", "yt", "za", "zm", "zw"].join();

var casper = require('casper').create({
    verbose: true,
    logLevel: 'debug'
    //clientScripts:  ['~/fpbase/run/getters.js']
});

var url_to_visit = casper.cli.get(0);
var num_clicked_links = 0

var caps_name = (casper.cli.get(2) !== 'NO_SCREENSHOT') ? caps_name : '';
	
// TODO: handle NO_SCREENSHOT
if (!url_to_visit) {
    casper
        .echo("No URL is given. Quitting:")
        .exit(1)
    ;
}

casper.userAgent('Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)');
//casper.userAgent('Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.22 (KHTML, like Gecko) Ubuntu Chromium/25.0.1364.160 Chrome/25.0.1364.160 Safari/537.22');

casper.on('resource.received', function(resource) {
    casper.echo('received: '+resource.url);
});

casper.on('resource.requested', function(request) {
    casper.echo('requested: '+request.url);
});

casper.on('step.timeout', function() {
	casper.echo('Step timed out on ' + this.requestUrl);
});

casper.on('timeout', function() {
    casper.echo('Script timed out on ' + this.requestUrl);
});

casper.on('child.page.created', function(page) {
	casper.echo('Child page created' + this.requestUrl);    
});

casper.on('child.page.loaded', function(page) {
	casper.echo('Child page loaded' + this.requestUrl);    
});

casper.getElemsbyXPath = function(selector) {
	//TODO: add attrs parameter
    return this.evaluate(function(selector) {
    	//var links = __utils__.getElementsByXPath('//a|//*[@onclick]');
    	var elems = [];
    	elems = __utils__.getElementsByXPath(selector);
    	
		return Array.prototype.map.call(elems, function(link) {
            try {
            	return [link.getAttribute("id"), link.getAttribute("href"), link.getAttribute("onclick"), link.getBoundingClientRect()];
            } catch (err) {
            	return undefined;
            }
        });
    	
    }, selector);
};

var selectXPath = require('casper').selectXPath;


casper.getDomainFromURL = function(url_){
	//http://stackoverflow.com/questions/8253136/how-to-get-domain-name-only-using-javascript#answer-8253221
	//we revised the above code to return PS + 1 http://jsfiddle.net/hqBKd/55/
    var url_ = url_.replace('http://','').replace('https://','').split(/[/?#]/)[0];
    var parts = url_.split('.'),
        ln = parts.length,
        i = ln,
        minLength = parts[parts.length-1].length,
        part;

    while(part = parts[--i]){
        if (TLDs.indexOf(part) < 0 || part.length < minLength || i < ln-2 || i === 0){
            //return part;
        	return url_.substr(url_.indexOf(part));
        }
    }
}

casper.isExternalLink = function(href){
	var current_url = this.getCurrentUrl(), //address bar 
		current_domain = this.getDomainFromURL(current_url),
		requested_domain = current_domain;
	
	if(!href.match(/^https?\:/i)){
		return false;
	}
	
	if(url_to_visit !== current_url){ // if we're redirected 
		requested_domain = this.getDomainFromURL(url_to_visit);	
	}
	
	var href_domain = this.getDomainFromURL(href);
	
	if (!href_domain.match(current_domain) &&  !href_domain.match(requested_domain)){
		//this.log("External link: " + href + " with " + url_to_visit+ " and " + current_url);
		return true;
	}else{
		//this.log("URLs from same domain:  " + href + " with " + url_to_visit+ " and " + current_url + ' href_domain ' + href_domain + ' current_domain ' + current_domain+ ' requested_domain ' + requested_domain);
		return false;
	}
}

casper.find_and_click_links = function(){
	casper.each(LINK_LABELS, function(casper, label_string){
		casper.then(function(){
			this.click_to_xpath_selector('//a[contains(text(), "'+ label_string + '")]')
		})		
	})
	
	casper.each(LINK_URLS, function(casper, url_string){
		casper.then(function(){
			this.click_to_xpath_selector('//a[contains(@href,"' + url_string + '")]')
		})
	})
	
	
	this.then(function(){
		for (var i = 1; i <= MAX_LINKS_TO_CLICK - num_clicked_links; i++){
			this.click_to_xpath_selector("(//a|//*[@onclick])[position()=" + i + "]")
			
		}
	})

}
	
casper.click_to_xpath_selector = function(xpath){
	
	//casper.echo("Will reload homepage " + url_to_visit);
	
	this.thenOpen(url_to_visit, function() { // Reload the home page
		//casper.echo("Reloaded homepage " + url_to_visit);
		this.wait(WAIT_AFTER_RELOAD, function(){
			selector =  selectXPath(xpath);
			try{
				var el_info = this.getElementInfo(selector);
			}catch(e){
				return;
			}
			if ("href" in el_info.attributes){
				var href = el_info.attributes.href;
				//casper.echo("HREF is " + el_info.attributes.href);
				if(casper.isExternalLink(href)){
					return; // don't click if this is a cross domain link
				}
			}
		
			try{
				this.click(selector);
				num_clicked_links += 1;
				casper.echo("Clicked! " + selector + " - " + num_clicked_links + '.th link');
				this.wait(WAIT_AFTER_CLICK, function() {
			        //this.echo("Waited after click");
			    })
			}catch(e){
				casper.echo("Error while clicking " + selector);
			}	
		})
	});	
	
} 
casper.start(url_to_visit).then(function() {
	casper.log("Loaded " + url_to_visit, 'info');
	this.wait(WAIT_AFTER_LOAD, function(){
		if(caps_name){
			this.capture(caps_name, {
		        top: 0,
		        left: 0,
		        width: 800,
		        height: 600
		    });
		}
		casper.find_and_click_links();
		casper.log("Finished all steps!", 'info');		
	});
	
});


casper.run();
