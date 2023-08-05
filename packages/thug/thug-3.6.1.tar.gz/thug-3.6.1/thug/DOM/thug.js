/*
 * Window object 
 * Javascript objects visibility
 */

//this.eval     = window.eval;
this.unescape = window.unescape;
this.decodeURIComponent = window.decodeURIComponent;
this.console = window.console;
window = this;
window.top = this;

Document.prototype = window.document;
HTMLElement.prototype = window.document.createElement("p");
XMLHttpRequest.prototype = new XMLHttpRequest;

Object.defineProperty(window, "location", {
	set: function(value){
		window.setLocation(value);
	},
	get: function(){
		return window.getLocation();
	}
});
