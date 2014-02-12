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
ALIBABA = 21
MERCADOLIBRE = 22
LIGATUS = 23

FINGERPRINTER_REGEX = {'(lookup|ds|collective|clients)\.bluecava.com': BLUECAVA,
                         'inside-graph\.com/ig\.js': INSIDEGRAPH,
                         'online-metrix\.net': THREATMETRIX,
                         'mpsnare\.iesnare\.com': IOVATION,
                         '(d2fhjc7xo4fbfa.cloudfront.net|maxmind.com).*device.js': MAXMIND,
                         'analytics-engine\.net/detector/fp\.js': ANALYTICSENGINE,
                         'sl[0-9]\.analytics-engine\.net/fingerprint': ANALYTICSENGINE,
                         'web-aupair.net/sites/default/files/fp/fp\.js': ANALYTICSENGINE,
                         '(coinbase.com|d2o7j92jk8qjiw.cloudfront.net)/assets/application\-[0-9a-z]{32}\.js': COINBASE,
                         'sbbpg=sbbShell': SITEBLACKBOX,
                         'tags\.master-perf-tools\.com/V\d+test/tagv[0-9]+.pkmin\.js' : PERFERENCEMENT,
                         'mfc\d/lib/o-mfccore\.js': MYFREECAMS, 
                         'jslib/pomegranate\.js': MINDSHARE,
                         'gmyze\.com.*(fingerprint|ax)\.js': AFKMEDIA,
                         'cdn-net\.com/cc\.js': CDNNET,
                         'privacytool\.org/AnonymityChecker/js/fontdetect\.js': ANONYMIZER,
                         'analyticsengine\.s3\.amazonaws\.com/archive/fingerprint\.compiled\.js': ANALYTICSPROS, # taken down. old url was http://dpp750yjcl65g.cloudfront.net/analyticsengine/util/fingerprint.compiled.js
                         'dscke\.suncorp\.com\.au/datastream-web/resources/js/fp/fontlist-min\.js': AAMI,
                         'virwox\.com/affiliate_tracker\.js': VIRWOX,
                         'isingles\.co\.uk/js/fprint/_core\.js': ISINGLES,
                         '(ibillboard|bbelements).*bbnaut\.swf': BBELEMENTS,
                         'pianomedia\.eu.*novosense\.swf': PIANOMEDIA,
                         'ali(pay|baba).*lsa.swf': ALIBABA,
                         'mercadoli[b|v]re.*dpe-.*swf': MERCADOLIBRE,
                         'ligatus.com.*fingerprint.*js': LIGATUS,
                         
                         }
