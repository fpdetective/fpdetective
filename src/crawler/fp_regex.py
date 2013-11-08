
BLUECAVA = 1
INSIDEGRAPH = 2
THREATMETRIX = 3
IOVATION = 4
MAXMIND = 5
ANALYTICSENGINE = 6
COINBASE = 7
SITEBLACKBOX = 8
PERFERENCEMENT = 9
MYFREECAMS = 10
MINDSHARE = 11
AFKMEDIA = 12
CDNNET = 13
ANALYTICSPROS = 14
ANONYMIZER = 15
AAMI = 16
VIRWOX = 17
ISINGLES = 18
BBELEMENTS = 19
PIANOMEDIA = 20
ALIPAY = 21

FINGERPRINTER_REGEX = {'lookup.bluecava.com': BLUECAVA, # http://lookup.bluecava.com/v2/BCLD2.js?_=1388888888
                         'ds.bluecava.com/v50/AC/BCAC': BLUECAVA, # http://ds.bluecava.com/v50/AC/BCAC5.js                     
                         'inside-graph.com/ig.js': INSIDEGRAPH, 
                         'h.online-metrix.net': THREATMETRIX,
                         'mpsnare.iesnare.com': IOVATION, 
                         'device.maxmind.com': MAXMIND,
                         'maxmind.com/app/device.js': MAXMIND,
                         'analytics-engine.net/detector/fp.js': ANALYTICSENGINE,
                         'sl\d.analytics-engine.net/fingerprint': ANALYTICSENGINE,
                         'web-aupair.net/sites/default/files/fp/fp.js': ANALYTICSENGINE,
                         'coinbase\.com/assets/application\-[0-9a-z]{32}\.js': COINBASE,
                         'd3w52z135jkm97\.cloudfront\.net\/assets\/application\-[0-9a-z]{32}\.js': COINBASE,  # TODO cobine regexps
                         'sbbpg=sbbShell': SITEBLACKBOX,
                         'tags.master-perf-tools.com/V\d+test/tagv\d+.pkmin.js' : PERFERENCEMENT,
                         'mfc\d/lib/o-mfccore.js': MYFREECAMS, # http://www.myfreecams.com/mfc2/lib/o-mfccore.js?vcc=... 
                         'jslib/pomegranate.js': MINDSHARE,
                         'gmyze.com.*[fingerprint|ax].js': AFKMEDIA,
                         'cdn-net.com/cc.js': CDNNET,
                         'privacytool.org/AnonymityChecker/js/fontdetect.js': ANONYMIZER,
                         'analyticsengine.s3.amazonaws.com/archive/fingerprint.compiled.js': ANALYTICSPROS, # taken down. old url was http://dpp750yjcl65g.cloudfront.net/analyticsengine/util/fingerprint.compiled.js
                         'dscke.suncorp.com.au/datastream-web/resources/js/fp/fontlist-min.js': AAMI,
                         'virwox.com/affiliate_tracker.js': VIRWOX,
                         'isingles.co.uk/js/fprint/_core.js': ISINGLES,
                         '.bbelements.com.*flash/bbnaut.swf': BBELEMENTS,
                         'pianomedia.eu.*novosense.swf': PIANOMEDIA,
                         'alipay.com.*lsa.swf': ALIPAY
                         }
