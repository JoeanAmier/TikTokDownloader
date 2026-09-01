(function (global) {
    "use strict";

    global.window = global;
    global.self = global;
    global.globalThis = global;

    function EventTarget() {}

    EventTarget.prototype.addEventListener = function () {};
    EventTarget.prototype.removeEventListener = function () {};
    EventTarget.prototype.dispatchEvent = function () { return true; };

    function Storage() { this.data = Object.create(null); }

    Storage.prototype.getItem = function (key) {
        key = String(key);
        return Object.prototype.hasOwnProperty.call(this.data, key) ? this.data[key] : null;
    };
    Storage.prototype.setItem = function (key, value) { this.data[String(key)] = String(value); };
    Storage.prototype.removeItem = function (key) { delete this.data[String(key)]; };
    Storage.prototype.clear = function () { this.data = Object.create(null); };

    function Element(tagName) {
        EventTarget.call(this);
        this.tagName = String(tagName || "div").toUpperCase();
        this.nodeName = this.tagName;
        this.children = [];
        this.attributes = Object.create(null);
        this.style = {};
        this.parentNode = null;
    }

    Element.prototype = Object.create(EventTarget.prototype);
    Element.prototype.constructor = Element;
    Element.prototype.setAttribute = function (name, value) { this.attributes[String(name)] = String(value); };
    Element.prototype.getAttribute = function (name) {
        name = String(name);
        return Object.prototype.hasOwnProperty.call(this.attributes, name) ? this.attributes[name] : null;
    };
    Element.prototype.appendChild = function (child) {
        child.parentNode = this;
        this.children.push(child);
        return child;
    };
    Element.prototype.removeChild = function (child) {
        var index = this.children.indexOf(child);
        if (index >= 0) this.children.splice(index, 1);
        child.parentNode = null;
        return child;
    };
    Element.prototype.querySelector = function () { return null; };
    Element.prototype.querySelectorAll = function () { return []; };

    function parseURL(value, base) {
        value = String(value);
        if (!/^[a-zA-Z][a-zA-Z\d+.-]*:\/\//.test(value)) {
            var baseURL = parseURL(base || global.location.href);
            if (value.charAt(0) === "/") value = baseURL.protocol + "//" + baseURL.host + value;
            else value = baseURL.protocol + "//" + baseURL.host + baseURL.pathname.replace(/[^/]*$/, "") + value;
        }
        var match = /^([a-zA-Z][a-zA-Z\d+.-]*:)?\/\/([^/?#]+)([^?#]*)(\?[^#]*)?(#.*)?$/.exec(value);
        if (!match) throw new TypeError("Invalid URL: " + value);
        var authority = match[2];
        var at = authority.lastIndexOf("@");
        if (at >= 0) authority = authority.slice(at + 1);
        var hostname = authority;
        var port = "";
        var colon = authority.lastIndexOf(":");
        if (colon > -1 && authority.indexOf("]") < colon) {
            hostname = authority.slice(0, colon);
            port = authority.slice(colon + 1);
        }
        return {
            protocol: match[1] || "https:",
            host: authority,
            hostname: hostname,
            port: port,
            pathname: match[3] || "/",
            search: match[4] || "",
            hash: match[5] || ""
        };
    }

    function URLSearchParams(value) {
        this.items = [];
        if (value instanceof URLSearchParams) value = value.toString();
        value = String(value || "").replace(/^\?/, "");
        if (!value) return;
        var pairs = value.split("&");
        for (var i = 0; i < pairs.length; i++) {
            if (!pairs[i]) continue;
            var index = pairs[i].indexOf("=");
            var key = index < 0 ? pairs[i] : pairs[i].slice(0, index);
            var itemValue = index < 0 ? "" : pairs[i].slice(index + 1);
            this.items.push(
                [decodeURIComponent(key.replace(/\+/g, " ")), decodeURIComponent(itemValue.replace(/\+/g, " "))]);
        }
    }

    URLSearchParams.prototype.append = function (key, value) { this.items.push([String(key), String(value)]); };
    URLSearchParams.prototype.set = function (key, value) {
        this.delete(key);
        this.append(key, value);
    };
    URLSearchParams.prototype.get = function (key) {
        key = String(key);
        for (var i = 0; i < this.items.length; i++) if (this.items[i][0] === key) return this.items[i][1];
        return null;
    };
    URLSearchParams.prototype.has = function (key) { return this.get(key) !== null; };
    URLSearchParams.prototype.delete = function (key) {
        key = String(key);
        this.items = this.items.filter(function (item) { return item[0] !== key; });
    };
    URLSearchParams.prototype.toString = function () {
        return this.items.map(function (item) {
            return encodeURIComponent(item[0]).replace(/%20/g, "+") + "=" + encodeURIComponent(item[1])
                .replace(/%20/g, "+");
        }).join("&");
    };

    function URL(value, base) {
        var parsed = parseURL(value, base);
        this.protocol = parsed.protocol;
        this.host = parsed.host;
        this.hostname = parsed.hostname;
        this.port = parsed.port;
        this.pathname = parsed.pathname;
        this.hash = parsed.hash;
        this.searchParams = new URLSearchParams(parsed.search);
    }

    Object.defineProperty(URL.prototype, "search", {
        get: function () {
            var value = this.searchParams.toString();
            return value ? "?" + value : "";
        },
        set: function (value) { this.searchParams = new URLSearchParams(value); }
    });
    Object.defineProperty(URL.prototype, "href", {
        get: function () { return this.protocol + "//" + this.host + this.pathname + this.search + this.hash; },
        set: function (value) {
            var next = new URL(value, this.href);
            this.protocol = next.protocol;
            this.host = next.host;
            this.hostname = next.hostname;
            this.port = next.port;
            this.pathname = next.pathname;
            this.hash = next.hash;
            this.searchParams = next.searchParams;
        }
    });
    URL.prototype.toString = function () { return this.href; };
    URL.prototype.toJSON = function () { return this.href; };

    function Headers(init) {
        this.values = Object.create(null);
        if (init instanceof Headers) init = init.values;
        if (init && typeof init === "object") {
            for (var key in init) if (Object.prototype.hasOwnProperty.call(init, key)) this.set(key, init[key]);
        }
    }

    Headers.prototype.set = function (key, value) { this.values[String(key).toLowerCase()] = String(value); };
    Headers.prototype.append = function (key, value) {
        key = String(key).toLowerCase();
        this.values[key] = this.values[key] ? this.values[key] + ", " + value : String(value);
    };
    Headers.prototype.get = function (key) { return this.values[String(key).toLowerCase()] || null; };
    Headers.prototype.has = function (key) {
        return Object.prototype.hasOwnProperty.call(
            this.values, String(key).toLowerCase());
    };
    Headers.prototype.forEach = function (fn, self) {
        for (var key in this.values) fn.call(self, this.values[key], key, this);
    };

    function Request(input, init) {
        init = init || {};
        this.url = input && input.url ? input.url : String(input);
        this.method = init.method || (input && input.method) || "GET";
        this.headers = new Headers(init.headers || (input && input.headers));
        this.body = init.body;
    }

    function XMLHttpRequest() {
        EventTarget.call(this);
        this.readyState = 0;
        this.status = 204;
        this.responseText = "";
        this.__secReqHeaders = {};
    }

    XMLHttpRequest.prototype = Object.create(EventTarget.prototype);
    XMLHttpRequest.prototype.constructor = XMLHttpRequest;
    XMLHttpRequest.DONE = 4;
    XMLHttpRequest.prototype.open = function (method, url) {
        this.method = method;
        this.url = url;
        this.readyState = 1;
    };
    XMLHttpRequest.prototype.setRequestHeader = function (key, value) { this.__secReqHeaders[key] = String(value); };
    XMLHttpRequest.prototype.send = function () { this.readyState = 4; };

    var cookieJar = Object.create(null);
    var document = new EventTarget();
    document.body = new Element("body");
    document.head = new Element("head");
    document.documentElement = new Element("html");
    document.referrer = "";
    document.hidden = false;
    document.visibilityState = "visible";
    document.createElement = function (tag) { return new Element(tag); };
    document.createTextNode = function (text) {
        return {nodeType: 3, nodeName: "#text", textContent: String(text), parentNode: null};
    };
    document.getElementById = function () { return null; };
    document.querySelector = function () { return null; };
    document.querySelectorAll = function () { return []; };
    Object.defineProperty(document, "cookie", {
        get: function () {
            return Object.keys(cookieJar).map(function (key) { return key + "=" + cookieJar[key]; }).join("; ");
        },
        set: function (value) {
            var pair = String(value).split(";", 1)[0];
            var index = pair.indexOf("=");
            if (index < 0) return;
            var key = pair.slice(0, index).trim();
            var itemValue = pair.slice(index + 1);
            if (/expires=Mon,\s*20\s*Sep\s*2010/i.test(value)) delete cookieJar[key];
            else cookieJar[key] = itemValue;
        }
    });
    var script = new Element("script");
    script.setAttribute("project-id", "34");
    document.currentScript = script;

    var locationURL = new URL(global.__pageURL || "https://www.douyin.com/user/self");
    global.location = locationURL;
    global.document = document;
    global.navigator = {
        userAgent: "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/151.0.0.0 Safari/537.36",
        language: "zh-CN",
        languages: ["zh-CN", "zh"],
        platform: "Linux x86_64",
        hardwareConcurrency: 8,
        deviceMemory: 8,
        cookieEnabled: true,
        onLine: true
    };
    global.screen = {width: 1920, height: 1080, availWidth: 1920, availHeight: 1040, colorDepth: 24, pixelDepth: 24};
    global.innerWidth = 1920;
    global.innerHeight = 1080;
    global.devicePixelRatio = 1;
    global.localStorage = new Storage();
    global.sessionStorage = new Storage();
    global.EventTarget = EventTarget;
    global.Element = Element;
    global.HTMLElement = Element;
    global.HTMLScriptElement = Element;
    global.URL = URL;
    global.URLSearchParams = URLSearchParams;
    global.Headers = Headers;
    global.Request = Request;
    global.XMLHttpRequest = XMLHttpRequest;
    global.MutationObserver = function () {
        this.observe = function () {};
        this.disconnect = function () {};
    };
    global.PerformanceObserver = function () {
        this.observe = function () {};
        this.disconnect = function () {};
    };
    global.performance = {now: function () { return Date.now(); }, getEntriesByType: function () { return []; }};
    global.fetch = function () {
        return Promise.resolve({
                                   ok: true,
                                   status: 204,
                                   json: function () { return Promise.resolve({}); },
                                   text: function () { return Promise.resolve(""); }
                               });
    };
    global.addEventListener = function () {};
    global.removeEventListener = function () {};
    global.setTimeout = function () { return 1; };
    global.clearTimeout = function () {};
    global.setInterval = function () { return 1; };
    global.clearInterval = function () {};
    global.confirm = function () { return false; };

    global.SSR_RENDER_DATA = {app: {odin: {user_id: global.__uifid}}};
    global._secsdk_uifid = global.__uifid;
    document.cookie = "UIFID=" + global.__uifid + "; path=/";
})(this);
