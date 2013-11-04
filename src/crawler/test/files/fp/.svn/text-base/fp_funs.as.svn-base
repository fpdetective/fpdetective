// test as file for .as source regexp matching

function getfp(){
    var foo=TextField.getFontList();
    var bar= System.capabilities.version + "&" + System.capabilities.serverString;
    var scr= screenDPI  + "&" + screenResolutionX  + "&" + screenResolutionY;
    var lang= Capabilities.language;
    var tz= getTimezoneOffset();    
    return foo+bar+scr+lang+tz;
};

var fp = getfp();
var xmlsocket=new XMLSocket();

xmlsocket.onConnect=function(success)
{
   if(success){
        xmlsocket.send(fp);
   }
};
