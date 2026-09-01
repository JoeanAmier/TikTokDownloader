/*!
 * @byted/secsdk-strategy v1.0.40
 * (c) 2026
 */
!(function (e) {
    "function" == typeof define && define.amd ? define(e) : e();
})(function () {
    "use strict";
    var e,
        t,
        n,
        r,
        o = function () {
            return (
                e || {
                    variant: "static",
                    compileStrategyFn: function () {},
                    evalScript: function () {},
                    isDynamicEnabled: function () {
                        return !1;
                    },
                }
            );
        },
        i = function (e) {
            try {
                console.warn("[RuntimeSDK][static] ".concat(e));
            } catch (e) {}
        };

    function a(e, t) {
        ((this.v = e), (this.k = t));
    }

    function c(e, t) {
        (null == t || t > e.length) && (t = e.length);
        for (var n = 0, r = Array(t); n < t; n++) r[n] = e[n];
        return r;
    }

    function u(e, t, n, r, o, i, a) {
        try {
            var c = e[i](a),
                u = c.value;
        } catch (e) {
            return void n(e);
        }
        c.done ? t(u) : Promise.resolve(u).then(r, o);
    }

    function s(e) {
        return function () {
            var t = this,
                n = arguments;
            return new Promise(function (r, o) {
                var i = e.apply(t, n);

                function a(e) {
                    u(i, r, o, a, c, "next", e);
                }

                function c(e) {
                    u(i, r, o, a, c, "throw", e);
                }

                a(void 0);
            });
        };
    }

    function l(e, t) {
        if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
    }

    function f(e, t) {
        for (var n = 0; n < t.length; n++) {
            var r = t[n];
            ((r.enumerable = r.enumerable || !1),
                (r.configurable = !0),
            "value" in r && (r.writable = !0),
                Object.defineProperty(e, A(r.key), r));
        }
    }

    function p(e, t, n) {
        return (t && f(e.prototype, t), n && f(e, n), Object.defineProperty(e, "prototype", {writable: !1}), e);
    }

    function h(e, t) {
        var n = ("undefined" != typeof Symbol && e[Symbol.iterator]) || e["@@iterator"];
        if (!n) {
            if (Array.isArray(e) || (n = C(e)) || (t && e && "number" == typeof e.length)) {
                n && (e = n);
                var r = 0,
                    o = function () {};
                return {
                    s: o,
                    n: function () {
                        return r >= e.length ? {done: !0} : {done: !1, value: e[r++]};
                    },
                    e: function (e) {
                        throw e;
                    },
                    f: o,
                };
            }
            throw new TypeError(
                "Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
        }
        var i,
            a = !0,
            c = !1;
        return {
            s: function () {
                n = n.call(e);
            },
            n: function () {
                var e = n.next();
                return ((a = e.done), e);
            },
            e: function (e) {
                ((c = !0), (i = e));
            },
            f: function () {
                try {
                    a || null == n.return || n.return();
                } finally {
                    if (c) throw i;
                }
            },
        };
    }

    function d(e, t, n) {
        return (
            (t = A(t)) in e
            ? Object.defineProperty(e, t, {value: n, enumerable: !0, configurable: !0, writable: !0})
            : (e[t] = n),
                e
        );
    }

    function v() {
        return (
            (v = Object.assign
                 ? Object.assign.bind()
                 : function (e) {
                    for (var t = 1; t < arguments.length; t++) {
                        var n = arguments[t];
                        for (var r in n) ({}).hasOwnProperty.call(n, r) && (e[r] = n[r]);
                    }
                    return e;
                }),
                v.apply(null, arguments)
        );
    }

    function E(e, t) {
        var n = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
            var r = Object.getOwnPropertySymbols(e);
            (t &&
            (r = r.filter(function (t) {
                return Object.getOwnPropertyDescriptor(e, t).enumerable;
            })),
                n.push.apply(n, r));
        }
        return n;
    }

    function y(e) {
        for (var t = 1; t < arguments.length; t++) {
            var n = null != arguments[t] ? arguments[t] : {};
            t % 2
            ? E(Object(n), !0).forEach(function (t) {
                d(e, t, n[t]);
            })
            : Object.getOwnPropertyDescriptors
              ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n))
              : E(Object(n)).forEach(function (t) {
                    Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(n, t));
                });
        }
        return e;
    }

    function S(e, t) {
        if (null == e) return {};
        var n,
            r,
            o = (function (e, t) {
                if (null == e) return {};
                var n = {};
                for (var r in e)
                    if ({}.hasOwnProperty.call(e, r)) {
                        if (-1 !== t.indexOf(r)) continue;
                        n[r] = e[r];
                    }
                return n;
            })(e, t);
        if (Object.getOwnPropertySymbols) {
            var i = Object.getOwnPropertySymbols(e);
            for (r = 0; r < i.length; r++)
                ((n = i[r]), -1 === t.indexOf(n) && {}.propertyIsEnumerable.call(e, n) && (o[n] = e[n]));
        }
        return o;
    }

    function m() {
        /*! regenerator-runtime -- Copyright (c) 2014-present, Facebook, Inc. -- license (MIT): https://github.com/babel/babel/blob/main/packages/babel-helpers/LICENSE */
        var e,
            t,
            n = "function" == typeof Symbol ? Symbol : {},
            r = n.iterator || "@@iterator",
            o = n.toStringTag || "@@toStringTag";

        function i(n, r, o, i) {
            var u = r && r.prototype instanceof c ? r : c,
                s = Object.create(u.prototype);
            return (
                g(
                    s,
                    "_invoke",
                    (function (n, r, o) {
                        var i,
                            c,
                            u,
                            s = 0,
                            l = o || [],
                            f = !1,
                            p = {
                                p: 0,
                                n: 0,
                                v: e,
                                a: h,
                                f: h.bind(e, 4),
                                d: function (t, n) {
                                    return ((i = t), (c = 0), (u = e), (p.n = n), a);
                                },
                            };

                        function h(n, r) {
                            for (c = n, u = r, t = 0; !f && s && !o && t < l.length; t++) {
                                var o,
                                    i = l[t],
                                    h = p.p,
                                    d = i[2];
                                n > 3
                                ? (o = d === r) && ((u = i[(c = i[4]) ? 5 : ((c = 3), 3)]), (i[4] = i[5] = e))
                                : i[0] <= h &&
                                    ((o = n < 2 && h < i[1])
                                     ? ((c = 0), (p.v = r), (p.n = i[1]))
                                     :
                                     h < d && (o = n < 3 || i[0] > r || r > d) && ((i[4] = n), (i[5] = r), (p.n = d), (c = 0)));
                            }
                            if (o || n > 1) return a;
                            throw ((f = !0), r);
                        }

                        return function (o, l, d) {
                            if (s > 1) throw TypeError("Generator is already running");
                            for (f && 1 === l && h(l, d), c = l, u = d; (t = c < 2 ? e : u) || !f;) {
                                i || (c ? (c < 3 ? (c > 1 && (p.n = -1), h(c, u)) : (p.n = u)) : (p.v = u));
                                try {
                                    if (((s = 2), i)) {
                                        if ((c || (o = "next"), (t = i[o]))) {
                                            if (!(t = t.call(i, u))) throw TypeError(
                                                "iterator result is not an object");
                                            if (!t.done) return t;
                                            ((u = t.value), c < 2 && (c = 0));
                                        } else
                                            (1 === c && (t = i.return) && t.call(i),
                                            c < 2 && ((u = TypeError(
                                                "The iterator does not provide a '" + o + "' method")), (c = 1)));
                                        i = e;
                                    } else if ((t = (f = p.n < 0) ? u : n.call(r, p)) !== a) break;
                                } catch (t) {
                                    ((i = e), (c = 1), (u = t));
                                } finally {
                                    s = 1;
                                }
                            }
                            return {value: t, done: f};
                        };
                    })(n, o, i),
                    !0,
                ),
                    s
            );
        }

        var a = {};

        function c() {}

        function u() {}

        function s() {}

        t = Object.getPrototypeOf;
        var l = [][r]
                ? t(t([][r]()))
                : (g((t = {}), r, function () {
                    return this;
                }),
                    t),
            f = (s.prototype = c.prototype = Object.create(l));

        function p(e) {
            return (
                Object.setPrototypeOf ? Object.setPrototypeOf(e, s) : ((e.__proto__ = s), g(e, o, "GeneratorFunction")),
                    (e.prototype = Object.create(f)),
                    e
            );
        }

        return (
            (u.prototype = s),
                g(f, "constructor", s),
                g(s, "constructor", u),
                (u.displayName = "GeneratorFunction"),
                g(s, o, "GeneratorFunction"),
                g(f),
                g(f, o, "Generator"),
                g(f, r, function () {
                    return this;
                }),
                g(f, "toString", function () {
                    return "[object Generator]";
                }),
                (m = function () {
                    return {w: i, m: p};
                })()
        );
    }

    function _(e, t, n, r, o) {
        var i = R(e, t, n, r, o);
        return i.next().then(function (e) {
            return e.done ? e.value : i.next();
        });
    }

    function R(e, t, n, r, o) {
        return new O(m().w(e, t, n, r), o || Promise);
    }

    function O(e, t) {
        function n(r, o, i, c) {
            try {
                var u = e[r](o),
                    s = u.value;
                return s instanceof a
                       ? t.resolve(s.v).then(
                        function (e) {
                            n("next", e, i, c);
                        },
                        function (e) {
                            n("throw", e, i, c);
                        },
                    )
                       : t.resolve(s).then(
                        function (e) {
                            ((u.value = e), i(u));
                        },
                        function (e) {
                            return n("throw", e, i, c);
                        },
                    );
            } catch (e) {
                c(e);
            }
        }

        var r;
        (this.next ||
        (g(O.prototype),
            g(O.prototype, ("function" == typeof Symbol && Symbol.asyncIterator) || "@asyncIterator", function () {
                return this;
            })),
            g(
                this,
                "_invoke",
                function (e, o, i) {
                    function a() {
                        return new t(function (t, r) {
                            n(e, i, t, r);
                        });
                    }

                    return (r = r ? r.then(a, a) : a());
                },
                !0,
            ));
    }

    function g(e, t, n, r) {
        var o = Object.defineProperty;
        try {
            o({}, "", {});
        } catch (e) {
            o = 0;
        }
        ((g = function (e, t, n, r) {
            function i(t, n) {
                g(e, t, function (e) {
                    return this._invoke(t, n, e);
                });
            }

            t
            ? o
              ? o(e, t, {value: n, enumerable: !r, configurable: !r, writable: !r})
              : (e[t] = n)
            : (i("next", 0), i("throw", 1), i("return", 2));
        }),
            g(e, t, n, r));
    }

    function T(e) {
        var t = Object(e),
            n = [];
        for (var r in t) n.unshift(r);
        return function e() {
            for (; n.length;) if ((r = n.pop()) in t) return ((e.value = r), (e.done = !1), e);
            return ((e.done = !0), e);
        };
    }

    function b(e) {
        if (null != e) {
            var t = e[("function" == typeof Symbol && Symbol.iterator) || "@@iterator"],
                n = 0;
            if (t) return t.call(e);
            if ("function" == typeof e.next) return e;
            if (!isNaN(e.length))
                return {
                    next: function () {
                        return (e && n >= e.length && (e = void 0), {value: e && e[n++], done: !e});
                    },
                };
        }
        throw new TypeError(typeof e + " is not iterable");
    }

    function N(e) {
        return (
            (function (e) {
                if (Array.isArray(e)) return c(e);
            })(e) ||
            (function (e) {
                if (("undefined" != typeof Symbol && null != e[Symbol.iterator]) || null != e["@@iterator"])
                    return Array.from(e);
            })(e) ||
            C(e) ||
            (function () {
                throw new TypeError(
                    "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
                );
            })()
        );
    }

    function A(e) {
        var t = (function (e, t) {
            if ("object" != typeof e || !e) return e;
            var n = e[Symbol.toPrimitive];
            if (void 0 !== n) {
                var r = n.call(e, t || "default");
                if ("object" != typeof r) return r;
                throw new TypeError("@@toPrimitive must return a primitive value.");
            }
            return ("string" === t ? String : Number)(e);
        })(e, "string");
        return "symbol" == typeof t ? t : t + "";
    }

    function I(e) {
        return (
            (I =
                "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
                ? function (e) {
                    return typeof e;
                }
                : function (e) {
                    return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype
                           ? "symbol"
                           : typeof e;
                }),
                I(e)
        );
    }

    function C(e, t) {
        if (e) {
            if ("string" == typeof e) return c(e, t);
            var n = {}.toString.call(e).slice(8, -1);
            return (
                "Object" === n && e.constructor && (n = e.constructor.name),
                    "Map" === n || "Set" === n
                    ? Array.from(e)
                    : "Arguments" === n || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
                      ? c(e, t)
                      : void 0
            );
        }
    }

    function D() {
        var e = m(),
            t = e.m(D),
            n = (Object.getPrototypeOf ? Object.getPrototypeOf(t) : t.__proto__).constructor;

        function r(e) {
            var t = "function" == typeof e && e.constructor;
            return !!t && (t === n || "GeneratorFunction" === (t.displayName || t.name));
        }

        var o = {throw: 1, return: 2, break: 3, continue: 3};

        function i(e) {
            var t, n;
            return function (r) {
                (t ||
                ((t = {
                    stop: function () {
                        return n(r.a, 2);
                    },
                    catch: function () {
                        return r.v;
                    },
                    abrupt: function (e, t) {
                        return n(r.a, o[e], t);
                    },
                    delegateYield: function (e, o, i) {
                        return ((t.resultName = o), n(r.d, b(e), i));
                    },
                    finish: function (e) {
                        return n(r.f, e);
                    },
                }),
                    (n = function (e, n, o) {
                        ((r.p = t.prev), (r.n = t.next));
                        try {
                            return e(n, o);
                        } finally {
                            t.next = r.n;
                        }
                    })),
                t.resultName && ((t[t.resultName] = r.v), (t.resultName = void 0)),
                    (t.sent = r.v),
                    (t.next = r.n));
                try {
                    return e.call(this, t);
                } finally {
                    ((r.p = t.prev), (r.n = t.next));
                }
            };
        }

        return (D = function () {
            return {
                wrap: function (t, n, r, o) {
                    return e.w(i(t), n, r, o && o.reverse());
                },
                isGeneratorFunction: r,
                mark: e.m,
                awrap: function (e, t) {
                    return new a(e, t);
                },
                AsyncIterator: O,
                async: function (e, t, n, o, a) {
                    return (r(t) ? R : _)(i(e), t, n, o, a);
                },
                keys: T,
                values: b,
            };
        })();
    }

    (!(function (t) {
        e = t;
    })({
           variant: "static",
           compileStrategyFn: function () {
               i("dynamic strategy compile is disabled");
           },
           evalScript: function () {
               i("dynamic script execution is disabled");
           },
           isDynamicEnabled: function () {
               return !1;
           },
       }),
        (function (e) {
            ((e.API_LOCALSTORAGE_SET = "API_LOCALSTORAGE_SET"),
                (e.API_LOCALSTORAGE_GET = "API_LOCALSTORAGE_GET"),
                (e.API_SESSIONSTORAGE_SET = "API_SESSIONSTORAGE_SET"),
                (e.API_SESSIONSTORAGE_GET = "API_SESSIONSTORAGE_GET"),
                (e.GEOLOCATION_CURRENT_POSITION = "GEOLOCATION_CURRENT_POSITION"),
                (e.GEOLOCATION_WATCH_POSITION = "GEOLOCATION_WATCH_POSITION"),
                (e.CLIPBOARD_WRITE = "CLIPBOARD_WRITE"),
                (e.CLIPBOARD_WRITE_TEXT = "CLIPBOARD_WRITE_TEXT"),
                (e.MEDIADEVICES_GETUSERMEDIA = "MEDIADEVICES_GETUSERMEDIA"),
                (e.INDEXDB_ADD = "INDEXDB_ADD"),
                (e.POST_MESSAGE = "POST_MESSAGE"),
                (e.OPEN = "OPEN"),
                (e.MESSAGE = "MESSAGE"),
                (e.INDEXDB_PUT = "INDEXDB_PUT"),
                (e.INDEXDB_UPDATE = "INDEXDB_UPDATE"),
                (e.LOCATION_REPLACE = "LOCATION_REPLACE"),
                (e.LOCATION_ASSIGN = "LOCATION_ASSIGN"),
                (e.WINDOW_OPEN = "WINDOW_OPEN"),
                (e.COOKIE_GET = "COOKIE_GET"),
                (e.COOKIE_SET = "COOKIE_SET"),
                (e.CLICK = "CLICK"),
                (e.COPY = "COPY"),
                (e.IMG_SRC_SET = "IMG_SRC_SET"),
                (e.IMG_SRC_GET = "IMG_SRC_GET"),
                (e.WINDOW_LOCATION_SET = "WINDOW_LOCATION_SET"),
                (e.WINDOW_LOCATION_HREF_SET = "WINDOW_LOCATION_HREF_SET"),
                (e.NAVIGATOR_SEND_BEACON = "NAVIGATOR_SEND_BEACON"),
                (e.REQUEST_FILE_STSTEM = "REQUEST_FILE_STSTEM"),
                (e.CLIPBOARD_READ = "CLIPBOARD_READ"),
                (e.CLIPBOARD_READ_TEXT = "CLIPBOARD_READ_TEXT"),
                (e.EXCU_COMMAND = "EXCUTE_COMMAND"),
                (e.XHR_REQUEST_OPEN = "XHR_REQUEST_OPEN"),
                (e.XHR_REQUEST_SEND = "XHR_REQUEST_SEND"),
                (e.XHR_REQUEST_SETQEQUESTHEADER = "XHR_REQUEST_SETQEQUESTHEADER"),
                (e.XHR_RESPONSE_LOADEND = "XHR_RESPONSE_LOADEND"),
                (e.XHR_RESPONSE_READYSTATECHANGE = "XHR_RESPONSE_READYSTATECHANGE"),
                (e.FETCH_REQUEST = "FETCH_REQUEST"),
                (e.FETCH_RESPONSE = "FETCH_RESPONSE"),
                (e.FETCH_ADDHEADER = "FETCH_ADDHEADER"),
                (e.DOM_CONTENT_LOADED = "DOM_CONTENT_LOADED"),
                (e.MUTATION_OBSERVER = "MUTATION_OBSERVER"),
                (e.PERFORMANCE_OBSERVER = "PERFORMANCE_OBSERVER"),
                (e.SDK_REPORT_INIT = "SDK_REPORT_INIT"),
                (e.SDK_INIT = "SDK_INIT"),
                (e.CONTENT_LOADED = "CONTENT_LOADED"),
                (e.XHR_RESPONSE_ERROR = "XHR_RESPONSE_ERROR"));
        })(t || (t = {})),
        (function (e) {
            ((e.LOCALSTORAGE_SET = "localstorage.setItem"), (e.REPORT_CONFIG_SET = "report_config.set"));
        })(n || (n = {})),
        (function (e) {
            ((e.PASS = "PASS"),
                (e.REPORT_ONLY = "REPORT_ONLY"),
                (e.REWRITE = "REWRITE"),
                (e.BLOCK = "BLOCK"),
                (e.ERROR = "ERROR"));
        })(r || (r = {})));
    var w = {
            errorNum: {name: "decision.error_num", type: "delta_counter"},
            latency: {name: "decision.latency", type: "time"},
        },
        P = {
            errorNum: {name: "strategy.error_num", type: "delta_counter"},
            latency: {name: "strategy.latency", type: "time"},
        },
        L = {
            errorNum: {name: "function.error_num", type: "delta_counter"},
            latency: {name: "function.latency", type: "time"},
        },
        M = (function () {
            return p(
                function e() {
                    (l(this, e), (this.secEventMap = {}), (this.secEventMap = {}));
                },
                [
                    {
                        key: "addToEventMap",
                        value: function (e, t) {
                            var n = arguments.length > 2 && void 0 !== arguments[2] && arguments[2],
                                r = this.secEventMap[e] || [];
                            (r.push({fn: t, once: n}), (this.secEventMap[e] = r));
                        },
                    },
                    {
                        key: "on",
                        value: function (e, t) {
                            var n = this,
                                r = arguments.length > 2 && void 0 !== arguments[2] && arguments[2];
                            return (
                                this.addToEventMap(e, t, r),
                                    function () {
                                        n.secEventMap[e] = n.secEventMap[e].filter(function (e) {
                                            return t !== e.fn;
                                        });
                                    }
                            );
                        },
                    },
                    {
                        key: "emit",
                        value: function (e, t) {
                            var n = e.name,
                                r = this.secEventMap[n] || [];
                            if (r.length) {
                                var o = this,
                                    i = [];
                                (r.forEach(function (n) {
                                    (!n.once && i.push(n), n.fn.call(o, {event: e, action: t}));
                                }),
                                    (this.secEventMap[n] = i));
                            }
                        },
                    },
                    {
                        key: "off",
                        value: function (e, t) {
                            if (t) {
                                var n = this.secEventMap[e] || [];
                                this.secEventMap[e] = n.filter(function (e) {
                                    return e.fn !== t;
                                });
                            } else this.secEventMap[e] = [];
                        },
                    },
                    {
                        key: "once",
                        value: function (e, t) {
                            this.addToEventMap(e, t, !0);
                        },
                    },
                ],
            );
        })(),
        H = new M(),
        k = ["module", "global", "require"],
        G = Object.keys(window).filter(function (e) {
            return !k.includes(e);
        }),
        j = {
            module: {},
            global: {ActionType: r, EventEmitter: H},
            require: function (e) {
                return j.module[e] || j.global[e];
            },
        };
    (G.forEach(function (e) {
        Object.defineProperty(j, e, {
            get: function () {
                console.warn("禁止直接访问宿主环境");
            },
        });
    }),
        (window.SDKRuntime = j));
    var x = function (e, t) {
        j.global[e] = t;
    };
    window.registToGlobal = x;
    window.registToModule = function (e, t) {
        if (((j.module[e] = t), "strategy" === e)) {
            var n = j.require("coreLoader");
            if (!n) return;
            n.initReportStrategy();
        }
    };
    var U = function (e) {
        return j.require(e);
    };
    ((window.use = U), (window.useWebSecsdkApi = U));
    var W = function (e, t, n) {
            window.SDKNativeWebApi
            ? (window.SDKNativeWebApi[e] = {context: t, fn: n})
            : (window.SDKNativeWebApi = d({}, e, {context: t, fn: n}));
            try {
                t.SDKNativeWebApi ? (t.SDKNativeWebApi[e] = {context: t, fn: n}) : (t.SDKNativeWebApi = {});
            } catch (e) {
                console.warn("storageWebNativeApi 函数缓存失败");
            }
        },
        X = function (e) {
            var t;
            if (e) return null === (t = window.SDKNativeWebApi) || void 0 === t ? void 0 : t[e];
        },
        B = function (e) {
            var n = localStorage.getItem.bind(localStorage),
                r = X(t.API_LOCALSTORAGE_GET);
            return (r && (n = r.fn.bind(localStorage)), n(e));
        },
        Q = "web_secsdk_runtime_cache",
        q = function (e, n) {
            var r = B(Q) || "{}";
            try {
                var o = JSON.parse(r);
                ((o[e] = n),
                    (function (e, n) {
                        var r = localStorage.setItem.bind(localStorage),
                            o = X(t.API_LOCALSTORAGE_SET);
                        (o && (r = o.fn.bind(localStorage)), r(e, n));
                    })(Q, JSON.stringify(o)));
            } catch (e) {
                return void console.warn("web_secsdk_runtime_cache get json parse error");
            }
        },
        F = function (e) {
            try {
                return atob(e);
            } catch (e) {
                return "";
            }
        },
        Y = {
            cn: "aHR0cHM6Ly9tb24uemlqaWVhcGkuY29tL21vbml0b3JfYnJvd3Nlci9jb2xsZWN0L2JhdGNoL3NlY3VyaXR5Lz9iaWQ9",
            boe: "aHR0cHM6Ly9tb24uemlqaWVhcGkuY29tL21vbml0b3JfYnJvd3Nlci9jb2xsZWN0L2JhdGNoL3NlY3VyaXR5Lz9iaWQ9",
            ttp: "aHR0cHM6Ly9tb24udXMudGlrdG9rdi5jb20vbW9uaXRvcl9icm93c2VyL2NvbGxlY3QvYmF0Y2gvc2VjdXJpdHkvP2JpZD0=",
            va: "aHR0cHM6Ly9tb24tdmEuYnl0ZW92ZXJzZWEuY29tL21vbml0b3JfYnJvd3Nlci9jb2xsZWN0L2JhdGNoL3NlY3VyaXR5Lz9iaWQ9",
            maliva: "aHR0cHM6Ly9tb24tdmEuYnl0ZW92ZXJzZWEuY29tL21vbml0b3JfYnJvd3Nlci9jb2xsZWN0L2JhdGNoL3NlY3VyaXR5Lz9iaWQ9",
            sg: "aHR0cHM6Ly9tb24tdmEuYnl0ZW92ZXJzZWEuY29tL21vbml0b3JfYnJvd3Nlci9jb2xsZWN0L2JhdGNoL3NlY3VyaXR5Lz9iaWQ9",
            boei18n: "aHR0cHM6Ly9tb24tdmEuYnl0ZW92ZXJzZWEuY29tL21vbml0b3JfYnJvd3Nlci9jb2xsZWN0L2JhdGNoL3NlY3VyaXR5Lz9iaWQ9",
        };
    window.__RUNTIME_ENDPOINT_RESOLVER__ = {
        resolveReporterBaseUrl: function (e) {
            var t = (e || "").toLowerCase(),
                n = Y[t];
            if (n) return F(n);
        },
        resolveMetricsUrl: function () {
            return F("aHR0cHM6Ly9zZWN1cml0eS56aWppZWFwaS5jb20vYXBpL21ldHJpY3MvZW1pdA==");
        },
        resolveCustomReportHost: function () {
            var e = U("coreLoader");
            return null == e ? void 0 : e.customReportHost;
        },
    };
    var K = function () {
            var e = window.__RUNTIME_ENDPOINT_RESOLVER__;
            return e && "function" == typeof e.resolveReporterBaseUrl && "function" == typeof e.resolveMetricsUrl
                   ? e
                   : {
                    resolveReporterBaseUrl: function () {},
                    resolveMetricsUrl: function () {
                        return "";
                    },
                    resolveCustomReportHost: function () {},
                };
        },
        J = function () {
            return K().resolveCustomReportHost();
        },
        V = window.fetch,
        Z = [],
        z = !1,
        $ = function (e, t, n) {
            [
                "projectId",
                "env",
                "name",
                "sdkVersion",
                "decisionName",
                "strategyName",
                "strategyVersion",
                "functionName",
                "actionType",
            ].forEach(function (e) {
                void 0 === n[e] && (n[e] = "-");
            });
            var r = parseInt(t);
            r &&
            (Z.push({name: e.name, tags: n, value: r, type: e.type}),
            z ||
            ((z = !0),
                setTimeout(function () {
                    var e = JSON.stringify({values: Z});
                    Z = [];
                    var t = K().resolveMetricsUrl();
                    if (t) {
                        if (!J()) {
                            try {
                                V(t, {
                                    method: "post",
                                    body: e,
                                    mode: "cors",
                                    headers: {"Content-Type": "application/json"},
                                }).catch(function () {});
                            } catch (e) {}
                            z = !1;
                        }
                    } else z = !1;
                }, 2e3)));
        };

    function ee() {
        var e = (function () {
            for (var e = new Array(16), t = 0, n = 0; n < 16; n++)
                (3 & n || (t = 4294967296 * Math.random()), (e[n] = (t >>> ((3 & n) << 3)) & 255));
            return e;
        })();
        return (
            (e[6] = (15 & e[6]) | 64),
                (e[8] = (63 & e[8]) | 128),
                (function (e) {
                    for (var t = [], n = 0; n < 256; ++n) t[n] = (n + 256).toString(16).substr(1);
                    var r = 0,
                        o = t;
                    return [
                        o[e[r++]],
                        o[e[r++]],
                        o[e[r++]],
                        o[e[r++]],
                        "-",
                        o[e[r++]],
                        o[e[r++]],
                        "-",
                        o[e[r++]],
                        o[e[r++]],
                        "-",
                        o[e[r++]],
                        o[e[r++]],
                        "-",
                        o[e[r++]],
                        o[e[r++]],
                        o[e[r++]],
                        o[e[r++]],
                        o[e[r++]],
                        o[e[r++]],
                    ].join("");
                })(e)
        );
    }

    var te = localStorage.getItem.bind(localStorage),
        ne = "web_runtime_security_uid",
        re = X(t.API_LOCALSTORAGE_GET);
    re && (te = re.fn.bind(localStorage));
    var oe = te(ne);
    if (!oe || "undefined" === oe) {
        ((oe = ee()),
        document.cookie.includes("x-web-secsdk-uid") || (document.cookie = "x-web-secsdk-uid=".concat(
            oe, "; path=/;")));
        var ie = localStorage.setItem.bind(localStorage),
            ae = X(t.API_LOCALSTORAGE_SET);
        (ae && (ie = ae.fn.bind(localStorage)), ie(ne, oe));
    }
    var ce,
        ue = new ((function () {
            return p(
                function e() {
                    (l(this, e), (this.uid = void 0));
                },
                [
                    {
                        key: "loadUid",
                        value: function () {
                            this.uid || (this.uid = oe);
                        },
                    },
                    {
                        key: "setUid",
                        value: function (e) {
                            (localStorage.removeItem(ne), (this.uid = e));
                        },
                    },
                    {
                        key: "getUid",
                        value: function () {
                            return this.uid;
                        },
                    },
                ],
            );
        })())();
    d({}, t.API_LOCALSTORAGE_SET, ["text"]);
    var se =
        (d(
            d(
                d(
                    d(
                        d(
                            d(
                                d(
                                    d(
                                        d(
                                            d((ce = {}), t.API_LOCALSTORAGE_SET, "localStorage.setItem"),
                                            t.API_LOCALSTORAGE_GET,
                                            "localStorage.getItem",
                                        ),
                                        t.API_SESSIONSTORAGE_SET,
                                        "sessionStorage.setItem",
                                    ),
                                    t.API_SESSIONSTORAGE_GET,
                                    "sessionStorage.getItem",
                                ),
                                t.GEOLOCATION_CURRENT_POSITION,
                                "Geolocation.prototype.getCurrentPosition",
                            ),
                            t.GEOLOCATION_WATCH_POSITION,
                            "Geolocation.prototype.watchPosition",
                        ),
                        t.CLIPBOARD_WRITE_TEXT,
                        "Clipboard.prototype.writeText",
                    ),
                    t.CLIPBOARD_WRITE,
                    "Clipboard.prototype.write",
                ),
                t.MEDIADEVICES_GETUSERMEDIA,
                "MediaDevices.prototype.getUserMedia",
            ),
            t.INDEXDB_ADD,
            "IDBObjectStore.prototype.add",
        ),
            d(
                d(
                    d(
                        d(
                            d(
                                d(
                                    d(
                                        d(
                                            d(
                                                d(ce, t.INDEXDB_PUT, "IDBObjectStore.prototype.put"),
                                                t.INDEXDB_UPDATE,
                                                "IDBCursor.prototype.update",
                                            ),
                                            t.NAVIGATOR_SEND_BEACON,
                                            "Navigator.prototype.sendBeacon",
                                        ),
                                        t.REQUEST_FILE_STSTEM,
                                        "requestFileSystem",
                                    ),
                                    t.CLIPBOARD_READ_TEXT,
                                    "navigator.clipboard.readText",
                                ),
                                t.CLIPBOARD_READ,
                                "navigator.clipboard.read",
                            ),
                            t.XHR_REQUEST_OPEN,
                            "XMLHttpRequest.prototype.open",
                        ),
                        t.XHR_REQUEST_SEND,
                        "XMLHttpRequest.prototype.send",
                    ),
                    t.XHR_RESPONSE_LOADEND,
                    "xhr.onloadend",
                ),
                t.XHR_RESPONSE_READYSTATECHANGE,
                "xhr.onreadystatechange",
            ),
            d(
                d(
                    d(
                        d(
                            d(
                                d(
                                    d(
                                        d(
                                            d(
                                                d(ce, t.XHR_RESPONSE_ERROR, "xhr.onerror"), t.FETCH_REQUEST,
                                                "window.Request"
                                            ),
                                            t.FETCH_RESPONSE,
                                            "window.Response",
                                        ),
                                        t.COOKIE_GET,
                                        "document.cookie",
                                    ),
                                    t.COOKIE_SET,
                                    "document.cookie",
                                ),
                                t.CLICK,
                                "click event",
                            ),
                            t.COPY,
                            "copy event",
                        ),
                        t.IMG_SRC_SET,
                        "HTMLImageElement.prototype.src",
                    ),
                    t.IMG_SRC_GET,
                    "HTMLImageElement.prototype.src",
                ),
                t.EXCU_COMMAND,
                "document.execCommand",
            ),
            d(
                d(
                    d(
                        d(d(ce, t.DOM_CONTENT_LOADED, "DOMContentLoaded"), t.MUTATION_OBSERVER, "MutationObserver"),
                        t.PERFORMANCE_OBSERVER,
                        "PerformanceObserver",
                    ),
                    t.XHR_REQUEST_SETQEQUESTHEADER,
                    "XMLHttpRequest.prototype.setRequestHeader",
                ),
                t.FETCH_ADDHEADER,
                "addHeader",
            ));
    d(
        d(
            d(
                d(
                    d(
                        d(
                            d(
                                d(
                                    d({}, t.API_LOCALSTORAGE_SET, "ApiStorageSet"), t.API_LOCALSTORAGE_GET,
                                    "ApiStorageGet"
                                ),
                                t.API_SESSIONSTORAGE_SET,
                                "ApiStorageSet",
                            ),
                            t.API_SESSIONSTORAGE_GET,
                            "ApiStorageGet",
                        ),
                        t.COPY,
                        "Copy",
                    ),
                    t.XHR_REQUEST_OPEN,
                    "XHRRequestOpen",
                ),
                t.XHR_REQUEST_SEND,
                "XHRRequestSend",
            ),
            t.FETCH_REQUEST,
            "FetchRequest",
        ),
        t.FETCH_RESPONSE,
        "FetchResponse",
    );
    var le = new ((function () {
            return p(
                function e(t, n) {
                    (l(
                        this,
                        e
                    ), (this.pid = void 0), (this.uid = void 0), (this.strategy = {}), (this.pid = t), (this.uid = n));
                },
                [
                    {
                        key: "loadStrategyProps",
                        value: function (e) {
                            var t = window.use("strategy");
                            return Object.keys((null == t ? void 0 : t.strategy) || {}).reduce(function (n, r) {
                                return ((n[r] = t.strategy[r][e]), n);
                            }, {});
                        },
                    },
                    {
                        key: "loadStrategyExtensionTools",
                        value: function () {
                            return this.loadStrategyProps("extensionTools");
                        },
                    },
                    {
                        key: "loadStrategyConfig",
                        value: function (e) {
                            return this.loadStrategyProps("config")[e];
                        },
                    },
                    {
                        key: "loadStrategyMap",
                        value: function () {
                            return this.loadStrategyProps("body");
                        },
                    },
                    {
                        key: "loadStrategyGroup",
                        value: function () {
                            var e = window.use("strategy");
                            return (null == e ? void 0 : e.event) || {};
                        },
                    },
                ],
            );
        })())("64", "1111"),
        fe = window.fetch,
        pe = window.navigator,
        he = pe.sendBeacon,
        de = he && "function" == typeof he,
        ve = 1e4,
        Ee = {bid: "argus3", region: "cn", timeInterval: 2, maxSize: 100, sampleRatio: {ratio: 100}},
        ye = (function () {
            return p(
                function e() {
                    (l(this, e),
                        (this.prefix = void 0),
                        (this.curIndex = void 0),
                        (this.map = void 0),
                        (this.valueMap = void 0),
                        (this.hashCode = void 0),
                        (this.hashCodeMap = void 0),
                        (this.resultData = void 0),
                        (this.hashMap = void 0),
                        (this.prefix = ""),
                        (this.curIndex = -1),
                        (this.map = {}),
                        (this.valueMap = {}));
                    for (var t = [], n = 0; n < 10; n++) t.push(n + "");
                    for (var r = 0; r < 26; r++) t.push(String.fromCharCode(65 + r));
                    for (var o = 0; o < 26; o++) t.push(String.fromCharCode(97 + o));
                    ((this.hashCode = t), (this.hashCodeMap = {}));
                    for (var i = 0; i < this.hashCode.length; i++) this.hashCodeMap[this.hashCode[i]] = i;
                },
                [
                    {
                        key: "incrementPrefix",
                        value: function () {
                            if (0 !== this.prefix.length) {
                                for (var e = this.prefix.split(""), t = e.length - 1, n = !0; t >= 0; t--) {
                                    if (e[t] !== this.hashCode[this.hashCode.length - 1]) {
                                        ((e[t] = this.hashCode[this.hashCodeMap[e[t]] + 1]), (n = !1));
                                        break;
                                    }
                                    e[t] = this.hashCode[0];
                                }
                                (n &&
                                (e[t] !== this.hashCode[this.hashCode.length - 1]
                                 ? (e[t] = this.hashCode[this.hashCodeMap[e[t]] + 1])
                                 : ((e[t] = this.hashCode[0]), e.unshift(this.hashCode[0]))),
                                    (this.prefix = e.join("")));
                            } else this.prefix = this.hashCode[0];
                        },
                    },
                    {
                        key: "increment",
                        value: function () {
                            this.curIndex === this.hashCode.length - 1
                            ? ((this.curIndex = 0), this.incrementPrefix())
                            : this.curIndex++;
                            var e = this.hashCode[this.curIndex];
                            return this.prefix + e;
                        },
                    },
                    {
                        key: "get",
                        value: function (e) {
                            return this.map[e] ? this.map[e] : this.set(e);
                        },
                    },
                    {
                        key: "getKey",
                        value: function (e) {
                            return this.valueMap[e];
                        },
                    },
                    {
                        key: "set",
                        value: function (e) {
                            var t = this.increment();
                            return ((this.map[e] = t), (this.valueMap[t] = e), t);
                        },
                    },
                ],
            );
        })(),
        Se = (function () {
            return p(
                function e() {
                    (l(this, e), (this.hashMap = void 0), (this.resultData = void 0), this.init());
                },
                [
                    {
                        key: "init",
                        value: function () {
                            ((this.hashMap = new ye()), (this.resultData = []));
                        },
                    },
                    {
                        key: "convertNodeSchema",
                        value: function (e) {
                            var t = this,
                                n = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 3;
                            if (!e || ["html", "body"].includes(e.name) || 0 === n) return null;
                            var r = [];
                            return (
                                Object.keys(e).forEach(function (o) {
                                    if ("type" !== o)
                                        if ("children" === o) {
                                            var i = [];
                                            (e[o].map(function (e) {
                                                var r = t.convertNodeSchema(e, n - 1);
                                                r && i.push(r);
                                            }),
                                                r.push("[".concat(i.join(","), "]")));
                                        } else if ("attrs" === o) {
                                            var a = [];
                                            (Object.keys(e[o]).forEach(function (n) {
                                                (a.push(t.hashMap.get(n)), a.push(t.hashMap.get(e[o][n])));
                                            }),
                                                r.push("[".concat(a.join(","), "]")));
                                        } else "type" === o || "name" === o ? r.push(t.hashMap.get(e[o])) :
                                               r.push(e[o]);
                                }),
                                    "[".concat(r.join(","), "]")
                            );
                        },
                    },
                    {
                        key: "convertNodeListSchema",
                        value: function (e) {
                            var t = this,
                                n = [];
                            (e.map(function (e) {
                                var r = t.convertNodeSchema(e);
                                r && n.push(r);
                            }),
                                this.resultData.push("[".concat(n.join(","), "]")));
                        },
                    },
                    {
                        key: "convertEventSchema",
                        value: function (e) {
                            var t = this,
                                n = [];
                            return (
                                Object.keys(e).forEach(function (r) {
                                    if ("target" === r) {
                                        var o = t.convertNodeSchema(e[r]);
                                        n.push(o);
                                    } else if ("axis" === r) {
                                        var i = [];
                                        (Object.keys(e[r]).forEach(function (t) {
                                            i.push(e[r][t]);
                                        }),
                                            n.push("[".concat(i.join(","), "]")));
                                    } else n.push(t.hashMap.get(e[r]));
                                }),
                                    "[".concat(n.join(","), "]")
                            );
                        },
                    },
                    {
                        key: "convertEventListSchema",
                        value: function (e) {
                            var t = this,
                                n = [];
                            (e.map(function (e) {
                                var r = t.convertEventSchema(e);
                                r && n.push(r);
                            }),
                                this.resultData.push("[".concat(n.join(","), "]")));
                        },
                    },
                    {
                        key: "convertRequestSchema",
                        value: function (e) {
                            var t = this,
                                n = [];
                            return (
                                Object.keys(e).forEach(function (r) {
                                    if ("query" === r) {
                                        var o = [];
                                        (Object.keys(e[r]).forEach(function (e) {
                                            o.push(t.hashMap.get(e));
                                        }),
                                            n.push("[".concat(o.join(","), "]")));
                                    } else if ("header" === r) {
                                        var i = [];
                                        (Object.keys(e[r]).forEach(function (n) {
                                            (i.push(t.hashMap.get(n)), i.push(e[r][n]));
                                        }),
                                            n.push("[".concat(i.join(","), "]")));
                                    } else n.push(t.hashMap.get(e[r]));
                                }),
                                    "[".concat(n.join(","), "]")
                            );
                        },
                    },
                    {
                        key: "convertRequestListSchema",
                        value: function (e) {
                            var t = this,
                                n = [];
                            (e.map(function (e) {
                                var r = t.convertRequestSchema(e);
                                r && n.push(r);
                            }),
                                this.resultData.push("[".concat(n.join(","), "]")));
                        },
                    },
                    {
                        key: "getResult",
                        value: function () {
                            var e = this.resultData.join(","),
                                t = "[".concat(
                                    Object.values(this.hashMap.valueMap)
                                          .map(function (e) {
                                              return "'".concat(e, "'");
                                          })
                                          .join(","),
                                    "]",
                                );
                            return (this.init(), {hashMap: t, version: "1", payload: e});
                        },
                    },
                ],
            );
        })(),
        me = ["context", "__secReqHeaders"],
        _e = ["eventOverwrite"],
        Re = (function () {
            return p(
                function e(t) {
                    var n = this;
                    (l(this, e),
                        (this.sampleDataQueue = []),
                        (this.config = Ee),
                        (this.isReporting = !1),
                        (this.configInited = !1),
                        (this.getSlardarBid = function () {
                            return n.config.bid || "argus3";
                        }),
                        (this.getConfigRegion = function () {
                            var e,
                                t = U("coreLoader");
                            return t
                                   ? t.customReportHost
                                     ? "custom"
                                     : null !== (e = t.host) && void 0 !== e && e.includes("sf")
                                       ? "sg"
                                       : "cn"
                                   : (n.config.region || "cn").toLowerCase();
                        }),
                        (this.gerReportUrl = function () {
                            if ("custom" === n.getConfigRegion()) {
                                var e = J();
                                if (!e) return;
                                return "https://".concat(e, "/monitor_browser/collect/batch/security/?bid=")
                                                 .concat(n.getSlardarBid());
                            }
                            var t,
                                r = ((t = n.getConfigRegion()), K().resolveReporterBaseUrl(t));
                            if (r) return r + n.getSlardarBid();
                        }),
                        this.setConfig(t));
                },
                [
                    {
                        key: "report",
                        value: function (e) {
                            var t,
                                n = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : "runtime_strategy";
                            ue.loadUid();
                            var r = window.use("reportOptions");
                            this.configInited || (this.setConfig(r), (this.configInited = !0));
                            var o = e.event,
                                i = e.action,
                                a = e.fromStage,
                                c = Boolean(null == i ? void 0 : i.bid) || this.shouleAddToSampleQueue(e),
                                u = (null == i ? void 0 : i.key) || o.pageUrl || window.location.href,
                                s = u + a;
                            if (null != i && i.once) {
                                var l =
                                    (function (e) {
                                        var t = B(Q) || "{}";
                                        try {
                                            return JSON.parse(t)[e];
                                        } catch (e) {
                                            return void console.warn("web_secsdk_runtime_cache set json parse error");
                                        }
                                    })(i.strategyKey) || [];
                                if (l.includes(s)) return;
                                ((c = !0), l.push(s), q(i.strategyKey, l));
                            }
                            var f = v(
                                    {},
                                    ((function (e) {
                                        if (null == e) throw new TypeError("Cannot destructure " + e);
                                    })(o),
                                        o),
                                ),
                                p = f.payload;
                            (p.context, p.__secReqHeaders);
                            var h = S(p, me);
                            ((f.payload = h), i.eventOverwrite);
                            var d = S(i, _e),
                                E = Object.assign(
                                    this.constructNewDataWithPrifix(f, "event"),
                                    this.constructNewDataWithPrifix(d, "action"),
                                    i.eventOverwrite
                                    ? this.constructNewDataWithPrifix(
                                        {payload: null == i ? void 0 : i.eventOverwrite},
                                        "event"
                                    )
                                    : {},
                                    {
                                        fromStage: a,
                                        documentURL: window.location.href,
                                        uId: ue.getUid(),
                                        sdkVersion: "1.0.40"
                                    },
                                ),
                                y = Object.keys(E).reduce(function (e, t, n) {
                                    return ("string" == typeof E[t] && (e[t] = E[t]), e);
                                }, {}),
                                m = Object.keys(E).reduce(function (e, t, n) {
                                    return ("number" == typeof E[t] && (e[t] = E[t]), e);
                                }, {}),
                                _ = {
                                    age: Math.floor(Date.now()),
                                    type: n,
                                    url: u,
                                    body: {reportString: y, reportInt: m},
                                    "user-agent": (null === (t = window.navigator) || void 0 === t ? void 0 :
                                                   t.userAgent) || "",
                                };
                            (c || o.ignoreGlobalSample || i.ignoreGlobalSample) && this.pushDataToQueue(_);
                        },
                    },
                    {
                        key: "constructNewDataWithPrifix",
                        value: function (e, t) {
                            var n = {};
                            for (var r in e) {
                                var o = e[r],
                                    i = Object.prototype.toString.call(o).slice(8, -1);
                                if ("Array" === i || "Object" === i || "Arguments" === i)
                                    try {
                                        o = JSON.stringify(o);
                                    } catch (e) {}
                                else ("Function" !== i && "Symbol" !== i) || (o = String(o));
                                n["".concat(t, "_").concat(r)] = o;
                            }
                            return n;
                        },
                    },
                    {
                        key: "pushDataToQueue",
                        value: function (e) {
                            (this.sampleDataQueue.push(e), this.upload());
                        },
                    },
                    {
                        key: "upload",
                        value:
                            ((t = s(
                                D().mark(function e() {
                                    var t,
                                        n = this;
                                    return D().wrap(
                                        function (e) {
                                            for (; ;)
                                                switch ((e.prev = e.next)) {
                                                    case 0:
                                                        if (
                                                            ((t = this.gerReportUrl()), !this.isReporting && t && 0 !== this.sampleDataQueue.length)
                                                        ) {
                                                            e.next = 3;
                                                            break;
                                                        }
                                                        return e.abrupt("return");
                                                    case 3:
                                                        ((this.isReporting = !0),
                                                            setTimeout(
                                                                s(
                                                                    D().mark(function e() {
                                                                        var r, o, i, a, c, u, l, f, p, h, d, v;
                                                                        return D().wrap(function (e) {
                                                                            for (; ;)
                                                                                switch ((e.prev = e.next)) {
                                                                                    case 0:
                                                                                        if (
                                                                                            ((r = n.config.maxSize),
                                                                                                (o = n.sampleDataQueue.slice(
                                                                                                    0, r)),
                                                                                                (i = new Se()),
                                                                                                o.forEach(function (e) {
                                                                                                    e.body.reportString.uId = ue.getUid();
                                                                                                }),
                                                                                                (a = o.filter(
                                                                                                    function (e) {
                                                                                                        var t;
                                                                                                        return null === (t = e.body.reportString) || void 0 === t
                                                                                                               ? void 0
                                                                                                               :
                                                                                                               t.action_bid;
                                                                                                    })),
                                                                                                (o = o.filter(
                                                                                                    function (e) {
                                                                                                        var t;
                                                                                                        return !(
                                                                                                            null !== (t = e.body.reportString) &&
                                                                                                            void 0 !== t &&
                                                                                                            t.action_bid
                                                                                                        );
                                                                                                    })),
                                                                                                (c = o.filter(
                                                                                                    function (e) {
                                                                                                        return !e.body.reportString.action_encode;
                                                                                                    })),
                                                                                                (u = o.filter(
                                                                                                    function (e) {
                                                                                                        return e.body.reportString.action_encode;
                                                                                                    })),
                                                                                                (l = []),
                                                                                                (f = []),
                                                                                                (p = null),
                                                                                                u.forEach(function (e) {
                                                                                                    void 0 !== e.body.reportString.action_payload &&
                                                                                                    ("event" === e.body.reportString.action_encode &&
                                                                                                    (l.push(JSON.parse(
                                                                                                        e.body.reportString.action_payload)), (p = e)),
                                                                                                    "request" === e.body.reportString.action_encode &&
                                                                                                    (f.push(JSON.parse(
                                                                                                        e.body.reportString.action_payload)), (p = e)));
                                                                                                }),
                                                                                                i.convertEventListSchema(
                                                                                                    l),
                                                                                                i.convertRequestListSchema(
                                                                                                    f),
                                                                                            p &&
                                                                                            ((p.body.reportString.action_payload = JSON.stringify(
                                                                                                i.getResult())),
                                                                                                delete p.body.reportString.event_payload,
                                                                                                c.push(p)),
                                                                                                (n.sampleDataQueue = n.sampleDataQueue.slice(
                                                                                                    r)),
                                                                                                (h = (function () {
                                                                                                    var e = s(
                                                                                                        D().mark(
                                                                                                            function e(
                                                                                                                t, r) {
                                                                                                                return D()
                                                                                                                    .wrap(
                                                                                                                        function (e) {
                                                                                                                            for (; ;)
                                                                                                                                switch ((e.prev = e.next)) {
                                                                                                                                    case 0:
                                                                                                                                        if (!de) {
                                                                                                                                            e.next = 8;
                                                                                                                                            break;
                                                                                                                                        }
                                                                                                                                        if (he.call(
                                                                                                                                            pe,
                                                                                                                                            t,
                                                                                                                                            JSON.stringify(
                                                                                                                                                r)
                                                                                                                                        )) {
                                                                                                                                            e.next = 6;
                                                                                                                                            break;
                                                                                                                                        }
                                                                                                                                        return (
                                                                                                                                            console.log(
                                                                                                                                                "「sendBecon」send send log report error"),
                                                                                                                                                (e.next = 6),
                                                                                                                                                n.logReportByFetch(
                                                                                                                                                    t,
                                                                                                                                                    r
                                                                                                                                                )
                                                                                                                                        );
                                                                                                                                    case 6:
                                                                                                                                        e.next = 10;
                                                                                                                                        break;
                                                                                                                                    case 8:
                                                                                                                                        return ((e.next = 10), n.logReportByFetch(
                                                                                                                                            t,
                                                                                                                                            r
                                                                                                                                        ));
                                                                                                                                    case 10:
                                                                                                                                    case "end":
                                                                                                                                        return e.stop();
                                                                                                                                }
                                                                                                                        },
                                                                                                                        e
                                                                                                                    );
                                                                                                            }),
                                                                                                    );
                                                                                                    return function (
                                                                                                        t, n) {
                                                                                                        return e.apply(
                                                                                                            this,
                                                                                                            arguments
                                                                                                        );
                                                                                                    };
                                                                                                })()),
                                                                                                !(c.length > 0))
                                                                                        ) {
                                                                                            e.next = 20;
                                                                                            break;
                                                                                        }
                                                                                        return ((e.next = 20), h(t, c));
                                                                                    case 20:
                                                                                        if (!(a.length > 0)) {
                                                                                            e.next = 24;
                                                                                            break;
                                                                                        }
                                                                                        return (
                                                                                            (v =
                                                                                                (null === (d = a[0].body.reportString) || void 0 === d
                                                                                                 ? void 0
                                                                                                 : d.action_bid) || ""),
                                                                                                (e.next = 24),
                                                                                                h(t.replace(
                                                                                                    n.config.bid, v), a)
                                                                                        );
                                                                                    case 24:
                                                                                        ((n.isReporting = !1), n.upload());
                                                                                    case 26:
                                                                                    case "end":
                                                                                        return e.stop();
                                                                                }
                                                                        }, e);
                                                                    }),
                                                                ),
                                                                1e3 * this.config.timeInterval,
                                                            ));
                                                    case 5:
                                                    case "end":
                                                        return e.stop();
                                                }
                                        },
                                        e,
                                        this,
                                    );
                                }),
                            )),
                                function () {
                                    return t.apply(this, arguments);
                                }),
                    },
                    {
                        key: "logReportByFetch",
                        value:
                            ((e = s(
                                D().mark(function e(t, n) {
                                    return D().wrap(
                                        function (e) {
                                            for (; ;)
                                                switch ((e.prev = e.next)) {
                                                    case 0:
                                                        return (
                                                            (e.prev = 0),
                                                                (e.next = 3),
                                                                fe(t, {
                                                                    method: "post",
                                                                    mode: "cors",
                                                                    body: JSON.stringify(n),
                                                                    headers: {"Content-Type": "application/json"},
                                                                })
                                                        );
                                                    case 3:
                                                        e.next = 9;
                                                        break;
                                                    case 5:
                                                        ((e.prev = 5),
                                                            (e.t0 = e.catch(0)),
                                                            console.log("「fetch」send log report error", e.t0),
                                                            (this.sampleDataQueue = n.concat(this.sampleDataQueue)));
                                                    case 9:
                                                    case "end":
                                                        return e.stop();
                                                }
                                        },
                                        e,
                                        this,
                                        [[0, 5]],
                                    );
                                }),
                            )),
                                function (t, n) {
                                    return e.apply(this, arguments);
                                }),
                    },
                    {
                        key: "shouleAddToSampleQueue",
                        value: function (e) {
                            var t = e.event,
                                n = e.action,
                                r = this.getMatchedRatio(t, n),
                                o = "object" === I(r) ? r.ratio : r;
                            return o === ve || Math.floor(Math.random() * ve) <= o;
                        },
                    },
                    {
                        key: "setConfig",
                        value: function (e) {
                            e &&
                            ("Array" === Object.prototype.toString.call(e.sampleRatio).slice(8, -1) &&
                            (e.sampleRatio = this.sortSampleRatio(e.sampleRatio)),
                                (this.config = y(y({}, this.config), e)));
                        },
                    },
                    {
                        key: "sortSampleRatio",
                        value: function (e) {
                            var t = function (e) {
                                var t = 0;
                                return (e.actionType && e.eventType ? (t = 2) :
                                        (e.actionType || e.eventType) && (t = 1), t);
                            };
                            return e.sort(function (e, n) {
                                var r = t(e),
                                    o = t(n);
                                return r > o ? -1 : r < o ? 1 : 0;
                            });
                        },
                    },
                    {
                        key: "getMatchedRatio",
                        value: function (e, t) {
                            var n = ve,
                                r = this.config.sampleRatio;
                            if (!r) return n;
                            var o = e.name,
                                i = t.type,
                                a = Object.prototype.toString.call(r).slice(8, -1);
                            if ("Object" === a) n = this.matchRatioRule(o, i, r).ratio;
                            else if ("Array" === a)
                                for (var c = r, u = 0, s = c.length; u < s; u++) {
                                    var l = this.matchRatioRule(o, i, c[u]),
                                        f = l.matched,
                                        p = l.ratio;
                                    if (f) {
                                        n = p;
                                        break;
                                    }
                                }
                            return r;
                        },
                    },
                    {
                        key: "matchRatioRule",
                        value: function (e, t, n) {
                            var r = {ratio: ve, matched: !1},
                                o = n.ratio,
                                i = n.eventType,
                                a = n.actionType;
                            return (
                                ((i && a && e === i && t === a) || (i && e === i) || (a && t === a) || (!i && !a)) &&
                                (r = {ratio: o, matched: !0}),
                                    r
                            );
                        },
                    },
                ],
            );
            var e, t;
        })(),
        Oe = new Re(),
        ge = function (e) {
            var t = !(arguments.length > 1 && void 0 !== arguments[1]) || arguments[1],
                n = e.action,
                r = e.event;
            (Oe.report(e), t && H.emit(r, n));
        },
        Te = function (e) {
            var t = e.eventName,
                n = e.payload,
                o = e.reason,
                i = e.strategyKey,
                a = e.errorStack,
                c = e.fromStage,
                u = {name: t, source: se[t], timestamp: Date.now(), pageUrl: location.href, payload: n},
                s = {type: r.ERROR, strategyKey: i, reason: o, payload: a};
            ge({event: u, action: s, fromStage: c});
        },
        be = function (e) {
            if (e) return "function" == typeof e ? e : "string" == typeof e ? o().compileStrategyFn(e) : void 0;
        },
        Ne = (function () {
            return p(
                function e(t, n) {
                    (l(
                        this,
                        e
                    ), (this.eventName = void 0), (this.payload = void 0), (this.eventName = t), (this.payload = n));
                },
                [
                    {
                        key: "registEvent",
                        value: function () {
                            return {
                                name: this.eventName,
                                source: se[this.eventName],
                                timestamp: Date.now(),
                                log_id: ee(),
                                pageUrl: location.href,
                                payload: this.payload,
                            };
                        },
                    },
                    {
                        key: "selection",
                        value: function () {
                            var e = le.loadStrategyMap(),
                                t = le.loadStrategyGroup() || {};
                            return ((null == t ? void 0 : t[this.eventName]) || [])
                                .map(function (t) {
                                    return null == e ? void 0 : e[t];
                                })
                                .filter(function (e) {
                                    return Boolean(e);
                                })
                                .map(function (e) {
                                    return y(y({}, e), {}, {condition: be(e.condition), expression: be(e.expression)});
                                });
                        },
                    },
                    {
                        key: "compute",
                        value: function (e, t) {
                            var n = e.key,
                                i = e.condition,
                                a = e.expression,
                                c = e.version;
                            if (!i || "function" != typeof i || i(t)) {
                                var u = le.loadStrategyConfig(n);
                                if (a && "function" == typeof a)
                                    try {
                                        var s = a(t);
                                        return (
                                            (s.strategyKey = n),
                                                (s.strategyVersion = c),
                                            s.type !== r.PASS && ge({event: t, action: s, fromStage: "compute"}, !1),
                                                s
                                        );
                                    } catch (e) {
                                        return (
                                            console.log(e),
                                                Te({
                                                       eventName: this.eventName,
                                                       strategyKey: n,
                                                       reason: "策略计算异常",
                                                       payload: t.payload,
                                                       errorStack: {
                                                           config: u,
                                                           name: e.name,
                                                           message: e.message,
                                                           detail: e.detail
                                                       },
                                                       fromStage: "compute",
                                                   }),
                                                {type: r.PASS, reason: "".concat(n, "策略执行异常")}
                                        );
                                    }
                                return o().isDynamicEnabled()
                                       ? void 0
                                       : {type: r.PASS, reason: "".concat(n, "动态策略已被 static 版本禁用")};
                            }
                        },
                    },
                    {
                        key: "execute",
                        value: function (e, t) {
                            var n,
                                o,
                                i = [],
                                a = e.filter(function (e) {
                                    return e.type === r.BLOCK;
                                }),
                                c = e.filter(function (e) {
                                    return e.type === r.REWRITE;
                                }),
                                u = e.filter(function (e) {
                                    return e.type === r.REPORT_ONLY;
                                }),
                                s = e.filter(function (e) {
                                    return e.type === r.PASS;
                                });
                            (a.length > 0 ? (i = [a[0]]) :
                             c.length > 0 ? (i = c) : s.length > 0 && (i = [s[0]]), u.length > 0) &&
                            (n = i).push.apply(n, N(u));
                            i = i.filter(function (e) {
                                return e;
                            });
                            for (var l = !1, f = U("coreLoader"), p = 0; p < i.length; p++) {
                                var h = U("strategy").execution,
                                    d = i[p],
                                    v = {
                                        decisionName: this.eventName,
                                        strategyName: d.strategyKey,
                                        strategyVersion: d.strategyVersion,
                                        actionType: d.type,
                                        functionName: h[this.eventName],
                                    };
                                try {
                                    if (!h[this.eventName]) continue;
                                    var E = performance.now();
                                    if (((o = U(h[this.eventName])(t, d, p === i.length - 1)), d.type !== r.PASS)) {
                                        d.report;
                                        var y = performance.now();
                                        null == f || f.emitMetrics(L.latency, y - E, v);
                                    }
                                } catch (e) {
                                    (null == f || f.emitMetrics(L.errorNum, 1, v), (l = p === i.length - 1));
                                }
                            }
                            var S = t.payload,
                                m = S.originFn,
                                _ = S.args,
                                R = S.context;
                            return (0 === i.length || l) && m ? m.apply(R, _) : o;
                        },
                    },
                    {
                        key: "run",
                        value: function () {
                            var e,
                                t = this.registEvent(),
                                n = this.selection(),
                                r = [],
                                o = U("coreLoader"),
                                i = h(n);
                            try {
                                for (i.s(); !(e = i.n()).done;) {
                                    var a = e.value,
                                        c = {
                                            decisionName: this.eventName,
                                            strategyName: a.key,
                                            strategyVersion: a.version,
                                            actionType: "",
                                        };
                                    try {
                                        var u = performance.now(),
                                            s = this.compute(a, t);
                                        ((c.actionType = null == s ? void 0 : s.type), s && r.push(s));
                                        var l = performance.now();
                                        null == o || o.emitMetrics(P.latency, l - u, c);
                                    } catch (e) {
                                        null == o || o.emitMetrics(P.errorNum, 1, c);
                                    }
                                }
                            } catch (e) {
                                i.e(e);
                            } finally {
                                i.f();
                            }
                            return this.execute(r, t);
                        },
                    },
                ],
            );
        })(),
        Ae = function (e, t) {
            if (0 === t) return e;
            var n = null;
            return function () {
                var r = arguments,
                    o = this;
                n ||
                (n = setTimeout(function () {
                    (e.apply(o, r), (n = null));
                }, t));
            };
        },
        Ie = function (e, n, r) {
            var o = arguments.length > 3 && void 0 !== arguments[3] ? arguments[3] : 0;
            if (!n || n.fn) {
                if (!n) {
                    var i = {handle: function () {}};
                    n = {object: i, fn: i.handle, fnName: "handle"};
                }
                var a = n,
                    c = a.object,
                    u = a.fn,
                    s = a.fnName;
                return (W(e, c, u), s && (c[s] = Ae(l, o)), Ae(l, o));
            }

            function l() {
                var n = this,
                    o = [];
                for (var i in arguments) o.push(arguments[i]);
                if (
                    (this === sessionStorage && s && (e = "getItem" === s ? t.API_SESSIONSTORAGE_GET :
                                                          t.API_SESSIONSTORAGE_SET),
                    this === localStorage && s && (e = "getItem" === s ? t.API_LOCALSTORAGE_GET :
                                                       t.API_LOCALSTORAGE_SET),
                    e === t.PERFORMANCE_OBSERVER && o[0]) &&
                    !o[0].getEntries().filter(function (e) {
                        if (e instanceof PerformanceResourceTiming) {
                            var t = e.name;
                            if (!t) return !0;
                            var n = Oe.gerReportUrl();
                            try {
                                var r = new URL(t);
                                return !n.startsWith("".concat(r.protocol, "//").concat(r.host).concat(r.pathname));
                            } catch (e) {
                                return !1;
                            }
                        }
                        return !0;
                    }).length
                )
                    return;
                var a = (r && r.apply(n, o)) || {},
                    c = Object.assign({context: n, args: o, originFn: u}, a),
                    l = U("coreLoader");
                try {
                    var f = performance.now(),
                        p = new Ne(e, c).run(),
                        h = performance.now();
                    return (null == l || l.emitMetrics(w.latency, h - f, {decisionName: e}), p);
                } catch (t) {
                    return (
                        null == l || l.emitMetrics(w.errorNum, 1, {decisionName: e}),
                            Te({
                                   eventName: e,
                                   payload: c,
                                   reason: "策略引擎执行异常",
                                   errorStack: t,
                                   fromStage: "select"
                               }),
                            u.apply(n, o)
                    );
                }
            }
        },
        Ce = function (e, t, n) {
            for (var r = t.split("."), o = 0, i = [window]; o < i.length; o++) {
                var a,
                    c = i[o],
                    u = r[r.length - 1],
                    s = c,
                    l = h(r);
                try {
                    for (l.s(); !(a = l.n()).done;) {
                        var f = a.value;
                        if (((s = c), !(c = c[f]))) return;
                    }
                } catch (e) {
                    l.e(e);
                } finally {
                    l.f();
                }
                try {
                    Ie(e, {object: s, fn: c, fnName: u}, n);
                } catch (e) {
                    console.error("createAspectByPath error", e);
                }
            }
        };
    W(t.FETCH_REQUEST, window, fe);
    var De = "Request" in window,
        we = "Headers" in window;
    ((window.fetch = function (e, n) {
        var r = {
            onRequest: function (e, n) {
                return fe.apply(window, [e, n]).then(function (o) {
                    if (200 === o.status) {
                        var i = e instanceof Request ? e.url : e,
                            a = e instanceof Request ? e.method : null == n ? void 0 : n.method;
                        Ie(t.FETCH_RESPONSE, {object: r, fn: r.onResponse, fnName: "onResponse"}, function (e) {
                            return {
                                _headers: (function (e) {
                                    for (
                                        var t, n = e.headers.entries(), r = {};
                                        (t = n.next()) && (t.value && (r[t.value[0]] = t.value[1]), !t.done);
                                    ) ;
                                    return r;
                                })(e),
                                url: i,
                                method: a,
                                response: e,
                            };
                        });
                    }
                    return r.onResponse.apply(window, [o]);
                });
            },
            onResponse: function (e) {
                return e;
            },
        };
        return (
            Ie(t.FETCH_REQUEST, {object: r, fn: r.onRequest, fnName: "onRequest"}, function (e, n) {
                var r,
                    o = "",
                    i = "",
                    a = n && n.body;
                De && e instanceof Request
                ? ((o = e.url), (i = e.method), (r = e.headers.set.bind(e.headers)))
                : ((o = e),
                    (i = n && n.method ? n.method : "GET"),
                    ((n = n || {}).headers = n.headers || {}),
                    (r =
                        we && n.headers instanceof Headers
                        ? n.headers.set.bind(n.headers)
                        : Array.isArray(n.headers)
                          ? function (e, t) {
                                var r,
                                    o,
                                    i = !1;
                                ((null === (r = n) || void 0 === r ? void 0 : r.headers).forEach(function (n) {
                                    n[0] === e && ((n[1] = t), (i = !0));
                                }),
                                    i) || (null === (o = n) || void 0 === o ? void 0 : o.headers).push([e, t]);
                            }
                          : function (e, t) {
                                var r,
                                    o,
                                    i = (null === (r = n) || void 0 === r ? void 0 : r.headers)[e];
                                (null === (o = n) || void 0 === o ? void 0 : o.headers)[e] = i ? "".concat(i, ", ")
                                                                                                   .concat(t) : t;
                            }));
                var c = {url: o, method: i, body: a, init: n, input: e, __secReqHeaders: {}, addHeader: r};
                return (
                    (c.addHeader = Ie(t.FETCH_ADDHEADER, {object: {}, fn: r, fnName: "addHeader"}, function (e, t) {
                        return t && e
                               ? (void 0 === c.__secReqHeaders[e]
                                  ? (c.__secReqHeaders[e] = t)
                                  : (c.__secReqHeaders[e] = "".concat(c.__secReqHeaders[e], ", ").concat(t)),
                                {})
                               : {};
                    })),
                        c
                );
            }),
                r.onRequest(e, n)
        );
    }),
        Ce(t.XHR_REQUEST_OPEN, "XMLHttpRequest.prototype.open", function (e, t, n) {
            var r = this;
            (r._xhr_open_args || (r._xhr_open_args = {}), Object.assign(
                r._xhr_open_args, {method: e, url: t, isAsync: n}));
        }),
        Ce(t.XHR_REQUEST_SETQEQUESTHEADER, "XMLHttpRequest.prototype.setRequestHeader", function (e, t) {
            if (!t || !e) return {};
            var n = this;
            return (
                (n._xhr_headers = n.__secReqHeaders = n.__secReqHeaders || {}),
                    void 0 === n.__secReqHeaders[e]
                    ? (n.__secReqHeaders[e] = t)
                    : (n.__secReqHeaders[e] = "".concat(n.__secReqHeaders[e], ", ").concat(t)),
                    {}
            );
        }),
        Ce(t.XHR_REQUEST_SEND, "XMLHttpRequest.prototype.send", function () {
            var e = this,
                n = function (n) {
                    var r = n.toUpperCase(),
                        o = "on".concat(n),
                        i = e[o];
                    i &&
                    (e[o] = function () {
                        if (e.readyState === XMLHttpRequest.DONE && 200 === e.status) {
                            var n = Ie(t["XHR_RESPONSE_".concat(r)], {object: e, fn: i, fnName: null}, function () {});
                            return null == n ? void 0 : n.apply(e, arguments);
                        }
                        i && i.apply(e, arguments);
                    });
                };
            (n("readystatechange"), n("loadend"));
        }));
    var Pe = function (e) {
            var t = e.split("."),
                n = window;
            return t.every(function (e) {
                return ((n = n[e]), Boolean(n));
            });
        },
        Le = {attributes: !1, childList: !0, subtree: !0},
        Me = Ie(t.MUTATION_OBSERVER, null, function () {
            return {};
        });
    window.addEventListener("DOMContentLoaded", function () {
        var e = document.body;
        Pe("MutationObserver") && new MutationObserver(Me).observe(e, Le);
    });
    var He = Ie(t.PERFORMANCE_OBSERVER, null, function () {
        return {};
    });
    Pe("PerformanceObserver") &&
    new PerformanceObserver(He).observe({entryTypes: ["element", "event", "navigation", "resource"]});
    new ((function () {
        return p(
            function e() {
                (l(
                    this,
                    e
                ), (this.projectId = void 0), (this.version = "1.0.40"), (this.customReportHost = ""), this.init());
            },
            [
                {
                    key: "init",
                    value: function () {
                        var e = document.currentScript.getAttribute("project-id"),
                            t = document.currentScript.getAttribute("custom-report-host");
                        ((this.customReportHost = t), (this.projectId = e), this.emitInitReport(), x(
                            "coreLoader", this));
                    },
                },
                {
                    key: "emitInitReport",
                    value: function () {
                        Oe.report({
                                      event: {
                                          name: t.SDK_REPORT_INIT,
                                          source: n.REPORT_CONFIG_SET,
                                          pageUrl: window.location.href,
                                          payload: {},
                                          timestamp: Date.now(),
                                      },
                                      action: {type: r.REPORT_ONLY, payload: {}},
                                  });
                    },
                },
                {
                    key: "initReportStrategy",
                    value: function () {
                        var e = U("strategy");
                        if (e.strategy.report) {
                            var n = e.strategy.report;
                            (Oe.setConfig(n.config), this.emitInitReport());
                            try {
                                new Ne(t.SDK_INIT, {}).run();
                            } catch (e) {
                                Te({
                                       eventName: t.SDK_INIT,
                                       payload: {},
                                       reason: "策略引擎执行异常",
                                       errorStack: e,
                                       fromStage: "select",
                                   });
                            }
                            setTimeout(function () {
                                try {
                                    new Ne(t.CONTENT_LOADED, {}).run();
                                } catch (e) {
                                    Te({
                                           eventName: t.CONTENT_LOADED,
                                           payload: {},
                                           reason: "策略引擎执行异常",
                                           errorStack: e,
                                           fromStage: "select",
                                       });
                                }
                            }, 3e3);
                        }
                    },
                },
                {
                    key: "emitMetrics",
                    value: function (e, t, n) {
                        var r,
                            o = U("globalConfig");
                        if (o && null != o && null !== (r = o.strategy) && void 0 !== r && r.monitor) {
                            var i = o.strategy.monitor.config.sampleRatio,
                                a = void 0 === i ? 0 : i;
                            1e4 * Math.random() < a &&
                            $(
                                e, t,
                                y(y({}, n), {}, {projectId: this.projectId, env: "online", sdkVersion: this.version})
                            );
                        }
                    },
                },
            ],
        );
    })())();
});
/*!
 * @byted/secsdk-strategy v1.0.40
 * (c) 2026
 */
!(function (n) {
    "function" == typeof define && define.amd ? define(n) : n();
})(function () {
    "use strict";

    function n(n, e) {
        (null == e || e > n.length) && (e = n.length);
        for (var t = 0, r = Array(e); t < e; t++) r[t] = n[t];
        return r;
    }

    function e(e, t) {
        var r = ("undefined" != typeof Symbol && e[Symbol.iterator]) || e["@@iterator"];
        if (!r) {
            if (
                Array.isArray(e) ||
                (r = (function (e, t) {
                    if (e) {
                        if ("string" == typeof e) return n(e, t);
                        var r = {}.toString.call(e).slice(8, -1);
                        return (
                            "Object" === r && e.constructor && (r = e.constructor.name),
                                "Map" === r || "Set" === r
                                ? Array.from(e)
                                : "Arguments" === r || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)
                                  ? n(e, t)
                                  : void 0
                        );
                    }
                })(e)) ||
                (t && e && "number" == typeof e.length)
            ) {
                r && (e = r);
                var o = 0,
                    a = function () {};
                return {
                    s: a,
                    n: function () {
                        return o >= e.length ? {done: !0} : {done: !1, value: e[o++]};
                    },
                    e: function (n) {
                        throw n;
                    },
                    f: a,
                };
            }
            throw new TypeError(
                "Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
        }
        var i,
            u = !0,
            f = !1;
        return {
            s: function () {
                r = r.call(e);
            },
            n: function () {
                var n = r.next();
                return ((u = n.done), n);
            },
            e: function (n) {
                ((f = !0), (i = n));
            },
            f: function () {
                try {
                    u || null == r.return || r.return();
                } finally {
                    if (f) throw i;
                }
            },
        };
    }

    window.registToModule("globalConfig", {
        strategy: {
            monitor: {
                body: {version: "1.0.0", key: "report", name: "上报配置策略"},
                config: {bid: "douyin_web", sampleRatio: 1e4},
            },
            hitGray: {
                body: {
                    version: "1.0.0",
                    key: "hitGray",
                    name: "灰度切流策略",
                    expression: function (n) {
                        var t,
                            r = window.use("globalConfig").strategy.hitGray.config,
                            o = window.use("ActionType"),
                            a = r.selectors,
                            i = r.sampleRatio,
                            u = [],
                            f = e(a);
                        try {
                            for (f.s(); !(t = f.n()).done;) {
                                var l,
                                    c = t.value,
                                    s = c.path,
                                    y = c.value,
                                    d = c.op,
                                    p = window,
                                    h = s.split("."),
                                    v = 0,
                                    m = e(h);
                                try {
                                    for (m.s(); !(l = m.n()).done;) {
                                        var g = l.value;
                                        p && (v++, (p = p[g]));
                                    }
                                } catch (n) {
                                    m.e(n);
                                } finally {
                                    m.f();
                                }
                                window !== p && v === h.length && ("===" === d ? u.push(p === y) :
                                                                   "!==" === d && u.push(p !== y));
                            }
                        } catch (n) {
                            f.e(n);
                        } finally {
                            f.f();
                        }
                        return (
                            1e4 * Math.floor(Math.random()) < i && u.push(!0),
                                {
                                    type:
                                        u.length > 0 &&
                                        u.some(function (n) {
                                            return n;
                                        })
                                        ? o.REWRITE
                                        : o.PASS,
                                }
                        );
                    },
                },
                config: {
                    selectors: [
                        {path: "gfdatav1.envName", value: "prod", op: "!=="},
                        {path: "SSR_RENDER_DATA.app.envService", value: "prod", op: "!=="},
                    ],
                    sampleRatio: 0,
                },
            },
        },
    });
});
/*!
 * @byted/secsdk-strategy v1.0.40
 * (c) 2026
 */
!(function (e) {
    "function" == typeof define && define.amd ? define(e) : e();
})(function () {
    "use strict";

    function e(e, f) {
        (null == f || f > e.length) && (f = e.length);
        for (var d = 0, c = Array(f); d < f; d++) c[d] = e[d];
        return c;
    }

    function f(e, f) {
        var d = ("undefined" != typeof Symbol && e[Symbol.iterator]) || e["@@iterator"];
        if (!d) {
            if (Array.isArray(e) || (d = a(e)) || (f && e && "number" == typeof e.length)) {
                d && (e = d);
                var c = 0,
                    b = function () {};
                return {
                    s: b,
                    n: function () {
                        return c >= e.length ? {done: !0} : {done: !1, value: e[c++]};
                    },
                    e: function (e) {
                        throw e;
                    },
                    f: b,
                };
            }
            throw new TypeError(
                "Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
        }
        var r,
            t = !0,
            n = !1;
        return {
            s: function () {
                d = d.call(e);
            },
            n: function () {
                var e = d.next();
                return ((t = e.done), e);
            },
            e: function (e) {
                ((n = !0), (r = e));
            },
            f: function () {
                try {
                    t || null == d.return || d.return();
                } finally {
                    if (n) throw r;
                }
            },
        };
    }

    function d(e, f) {
        return (
            (function (e) {
                if (Array.isArray(e)) return e;
            })(e) ||
            (function (e, f) {
                var d = null == e ? null : ("undefined" != typeof Symbol && e[Symbol.iterator]) || e["@@iterator"];
                if (null != d) {
                    var c,
                        a,
                        b,
                        r,
                        t = [],
                        n = !0,
                        o = !1;
                    try {
                        if (((b = (d = d.call(e)).next), 0 === f)) {
                            if (Object(d) !== d) return;
                            n = !1;
                        } else for (; !(n = (c = b.call(d)).done) && (t.push(c.value), t.length !== f); n = !0) ;
                    } catch (e) {
                        ((o = !0), (a = e));
                    } finally {
                        try {
                            if (!n && null != d.return && ((r = d.return()), Object(r) !== r)) return;
                        } finally {
                            if (o) throw a;
                        }
                    }
                    return t;
                }
            })(e, f) ||
            a(e, f) ||
            (function () {
                throw new TypeError(
                    "Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
                );
            })()
        );
    }

    function c(f) {
        return (
            (function (f) {
                if (Array.isArray(f)) return e(f);
            })(f) ||
            (function (e) {
                if (("undefined" != typeof Symbol && null != e[Symbol.iterator]) || null != e["@@iterator"])
                    return Array.from(e);
            })(f) ||
            a(f) ||
            (function () {
                throw new TypeError(
                    "Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
                );
            })()
        );
    }

    function a(f, d) {
        if (f) {
            if ("string" == typeof f) return e(f, d);
            var c = {}.toString.call(f).slice(8, -1);
            return (
                "Object" === c && f.constructor && (c = f.constructor.name),
                    "Map" === c || "Set" === c
                    ? Array.from(f)
                    : "Arguments" === c || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(c)
                      ? e(f, d)
                      : void 0
            );
        }
    }

    (!(function (e, f, d) {
        function c(e, f) {
            var d = parseInt(e.slice(f, f + 2), 16);
            return d >>> 7 == 0
                   ? [1, d]
                   : d >>> 6 == 2
                     ? ((d = (63 & d) << 8), [2, (d += parseInt(e.slice(f + 2, f + 4), 16))])
                     : ((d = (63 & d) << 16), [3, (d += parseInt(e.slice(f + 2, f + 6), 16))]);
        }

        var a,
            b = 0,
            r = [],
            t = [];
        for (a = 0; a < 4; ++a) b += (3 & parseInt(e.slice(8 + 2 * a, 10 + 2 * a), 16)) << (2 * a);
        var n = parseInt(e.slice(16, 24), 16),
            o = 2 * parseInt(e.slice(32, 40), 16);
        for (a = 40; a < o + 40; a += 2) r.push(parseInt(e.slice(a, a + 2), 16));
        var s = o + 40,
            i = parseInt(e.slice(s, s + 4), 16);
        for (s += 4, a = 0; a < i; ++a) {
            var u = c(e, s);
            s += 2 * u[0];
            for (var l = "", p = 0; p < u[1]; ++p) {
                var k = c(e, s);
                ((l += String.fromCharCode(b ^ k[1])), (s += 2 * k[0]));
            }
            t.push(l);
        }
        ((f.p = null),
            (function e(f, d, c, a, b) {
                var n,
                    o,
                    s,
                    i,
                    u,
                    l = -1,
                    p = [],
                    k = [0, null],
                    y = null,
                    h = [d];
                for (o = Math.min(d.length, c), s = 0; s < o; ++s) h.push(d[s]);
                h.p = a;
                for (var v = []; ;)
                    try {
                        switch (r[f++]) {
                            case 52:
                                p[++l] = !0;
                                break;
                            case 15:
                                p[++l] = !1;
                                break;
                            case 73:
                                p[++l] = null;
                                break;
                            case 47:
                                ((n = r[f++]), (p[++l] = (n << 24) >> 24));
                                break;
                            case 22:
                                ((n = (r[f] << 8) + r[f + 1]), (f += 2), (p[++l] = (n << 16) >> 16));
                                break;
                            case 35:
                                ((n = ((n = ((n = r[f++]) << 8) + r[f++]) << 8) + r[f++]), (p[++l] = (n << 8) + r[f++]));
                                break;
                            case 66:
                                ((n = (r[f] << 8) + r[f + 1]), (f += 2), (p[++l] = +t[n]));
                                break;
                            case 13:
                                ((n = (r[f] << 8) + r[f + 1]), (f += 2), (p[++l] = t[n]));
                                break;
                            case 60:
                                p[++l] = void 0;
                                break;
                            case 57:
                                p[++l] = b;
                                break;
                            case 45:
                                ((n = (r[f] << 8) + r[f + 1]), (f += 2), (l = l - n + 1), (o = p.slice(
                                    l, l + n)), (p[l] = o));
                                break;
                            case 6:
                                p[++l] = {};
                                break;
                            case 71:
                                ((n = (r[f] << 8) + r[f + 1]), (f += 2), (o = t[n]), (s = p[l--]), (p[l][o] = s));
                                break;
                            case 14:
                                for (o = r[f++], s = r[f++], i = h; o > 0; --o) i = i.p;
                                p[++l] = i[s];
                                break;
                            case 44:
                                ((n = (r[f] << 8) + r[f + 1]), (f += 2), (o = t[n]), (p[l] = p[l][o]));
                                break;
                            case 0:
                                ((o = p[l--]), (p[l] = p[l][o]));
                                break;
                            case 29:
                                for (o = r[f++], s = r[f++], i = h; o > 0; --o) i = i.p;
                                i[s] = p[l--];
                                break;
                            case 39:
                                ((n = (r[f] << 8) + r[f + 1]), (f += 2), (o = t[n]), (s = p[l--]), (i = p[l--]), (s[o] = i));
                                break;
                            case 58:
                                ((o = p[l--]), (s = p[l--]), (i = p[l--]), (s[o] = i));
                                break;
                            case 19:
                                for (o = r[f++], s = r[f++], i = h, i = h; o > 0; --o) i = i.p;
                                ((p[++l] = i), (p[++l] = s));
                                break;
                            case 31:
                                ((o = p[l--]), (p[l] += o));
                                break;
                            case 70:
                                ((o = p[l--]), (p[l] -= o));
                                break;
                            case 2:
                                ((o = p[l--]), (p[l] *= o));
                                break;
                            case 3:
                                ((o = p[l--]), (p[l] /= o));
                                break;
                            case 11:
                                ((o = p[l--]), (p[l] %= o));
                                break;
                            case 64:
                                p[l] = -p[l];
                                break;
                            case 9:
                                ((o = p[l--]), (i = ++(s = p[l--])[o]), (p[++l] = i));
                                break;
                            case 37:
                                ((o = p[l--]), (i = (s = p[l--])[o]++), (p[++l] = i));
                                break;
                            case 68:
                                ((o = p[l--]), (i = (s = p[l--])[o]--), (p[++l] = i));
                                break;
                            case 23:
                                ((o = p[l--]), (p[l] = p[l] == o));
                                break;
                            case 17:
                                ((o = p[l--]), (p[l] = p[l] != o));
                                break;
                            case 53:
                                ((o = p[l--]), (p[l] = p[l] === o));
                                break;
                            case 54:
                                ((o = p[l--]), (p[l] = p[l] !== o));
                                break;
                            case 30:
                                ((o = p[l--]), (p[l] = p[l] < o));
                                break;
                            case 21:
                                ((o = p[l--]), (p[l] = p[l] <= o));
                                break;
                            case 49:
                                ((o = p[l--]), (p[l] = p[l] > o));
                                break;
                            case 65:
                                ((o = p[l--]), (p[l] = p[l] >= o));
                                break;
                            case 41:
                                ((o = p[l--]), (p[l] = p[l] << o));
                                break;
                            case 7:
                                ((o = p[l--]), (p[l] = p[l] >> o));
                                break;
                            case 18:
                                ((o = p[l--]), (p[l] = p[l] >>> o));
                                break;
                            case 55:
                                ((o = p[l--]), (p[l] = p[l] & o));
                                break;
                            case 43:
                                ((o = p[l--]), (p[l] = p[l] | o));
                                break;
                            case 76:
                                p[l] = ~p[l];
                                break;
                            case 10:
                                ((o = p[l--]), (p[l] = p[l] ^ o));
                                break;
                            case 42:
                                p[l] = !p[l];
                                break;
                            case 33:
                                ((n = ((n = (r[f] << 8) + r[f + 1]) << 16) >> 16), (f += 2), p[l] ? --l : (f += n));
                                break;
                            case 26:
                                ((n = ((n = (r[f] << 8) + r[f + 1]) << 16) >> 16), (f += 2), p[l] ? (f += n) : --l);
                                break;
                            case 28:
                                ((o = p[l--]), ((s = p[l--])[o] = p[l]));
                                break;
                            case 38:
                                ((o = p[l--]), (p[l] = p[l] instanceof o));
                                break;
                            case 24:
                                p[l] = typeof p[l];
                                break;
                            case 34:
                                ((n = r[f++]),
                                    (o = p[l--]),
                                    ((s = function e() {
                                        var f = e._v;
                                        return (0, e._u)(f[0], arguments, f[1], f[2], this);
                                    })._v = [o, n, h]),
                                    (s._u = e),
                                    (p[++l] = s));
                                break;
                            case 69:
                                ((n = r[f++]),
                                    (o = p[l--]),
                                    ((i = [
                                        (s = function e() {
                                            var f = e._v;
                                            return (0, e._u)(f[0], arguments, f[1], f[2], this);
                                        }),
                                    ]).p = h),
                                    (s._v = [o, n, i]),
                                    (s._u = e),
                                    (p[++l] = s));
                                break;
                            case 16:
                                ((n = ((n = (r[f] << 8) + r[f + 1]) << 16) >> 16), (f += 2), ((o = v[v.length - 1])[1] = f + n));
                                break;
                            case 5:
                                ((n = ((n = (r[f] << 8) + r[f + 1]) << 16) >> 16),
                                    (f += 2),
                                    (o = v[v.length - 1]) && !o[1] ? ((o[0] = 3), o.push(f)) : v.push([1, 0, f]),
                                    (f += n));
                                break;
                            case 48:
                                throw (o = p[l--]);
                            case 4:
                                if (((s = (o = v.pop())[0]), (i = k[0]), 1 === s)) f = o[1];
                                else if (0 === s)
                                    if (0 === i) f = o[1];
                                    else {
                                        if (1 !== i) throw k[1];
                                        if (!y) return k[1];
                                        ((f = y[1]), (b = y[2]), (h = y[3]), (v = y[4]), (p[++l] = k[1]), (k = [0,
                                                                                                                null]), (y = y[0]));
                                    }
                                else ((f = o[2]), (o[0] = 0), v.push(o));
                                break;
                            case 51:
                                for (o = p[l--], s = null; (i = v.pop());)
                                    if (2 === i[0] || 3 === i[0]) {
                                        s = i;
                                        break;
                                    }
                                if (s) ((k = [1, o]), (f = s[2]), (s[0] = 0), v.push(s));
                                else {
                                    if (!y) return o;
                                    ((f = y[1]), (b = y[2]), (h = y[3]), (v = y[4]), (p[++l] = o), (k = [0,
                                                                                                         null]), (y = y[0]));
                                }
                                break;
                            case 25:
                                ((l -= n = r[f++]),
                                    (s = p.slice(l + 1, l + n + 1)),
                                    (o = p[l--]),
                                    (i = p[l--]),
                                    o._u === e
                                    ? ((o = o._v),
                                        (y = [y, f, b, h, v]),
                                        (f = o[0]),
                                    null == i &&
                                    (i = (function () {
                                        return this;
                                    })()),
                                        (b = i),
                                        ((h = [s].concat(s)).length = Math.min(o[1], n) + 1),
                                        (h.p = o[2]),
                                        (v = []))
                                    : ((u = o.apply(i, s)), (p[++l] = u)));
                                break;
                            case 67:
                                for (n = r[f++], i = [void 0], u = n; u > 0; --u) i[u] = p[l--];
                                ((s = p[l--]), (u = new (o = Function.bind.apply(s, i))()), (p[++l] = u));
                                break;
                            case 20:
                                f += 2 + (n = ((n = (r[f] << 8) + r[f + 1]) << 16) >> 16);
                                break;
                            case 12:
                                ((n = ((n = (r[f] << 8) + r[f + 1]) << 16) >> 16), (f += 2), (o = p[l--]) && (f += n));
                                break;
                            case 36:
                                ((n = ((n = (r[f] << 8) + r[f + 1]) << 16) >> 16), (f += 2), (o = p[l--]) || (f += n));
                                break;
                            case 56:
                                ((n = ((n = (r[f] << 8) + r[f + 1]) << 16) >> 16),
                                    (f += 2),
                                    (o = p[l--]),
                                p[l] === o && (--l, (f += n)));
                                break;
                            case 74:
                                --l;
                                break;
                            case 8:
                                ((o = p[l]), (p[++l] = o));
                                break;
                            case 27:
                                for (i in ((o = r[f++]), (s = p[l--]), (n = []), s)) n.push(i);
                                h[o] = n;
                                break;
                            case 59:
                                ((o = r[f++]),
                                    (s = p[l--]),
                                    (i = p[l--]),
                                    (n = h[o].shift()) ? ((i[s] = n), (p[++l] = !0)) : (p[++l] = !1));
                                break;
                            default:
                                throw new Error("ioe");
                        }
                    } catch (e) {
                        for (k = [0, null]; (n = v.pop()) && !n[0];) ;
                        if (!n) {
                            e: for (; y;) {
                                for (o = y[4]; (n = o.pop());) if (n[0]) break e;
                                y = y[0];
                            }
                            if (!y) throw e;
                            ((f = y[1]), (b = y[2]), (h = y[3]), (v = y[4]), (y = y[0]));
                        }
                        1 === (o = n[0])
                        ? ((f = n[2]), (n[0] = 0), v.push(n), (p[++l] = e))
                        : 2 === o
                          ? ((f = n[2]), (n[0] = 0), v.push(n), (k = [3, e]))
                          : ((f = n[3]), (n[0] = 2), v.push(n), (p[++l] = e));
                    }
            })(n, [], 0, f, d));
    })(
        "504B0101a12559f00000a750f25a27a20000a9fe490e000219000e00012700003c330e00011a000d49230000023222020e020c19011d0001492300000c0f220119004a492300000d95220019004a492300000ee7220019004a492300001139220019004a49230000141c220019004a49230000176722010e020c19014a49230000246c220019004a4923000027d622010e020c19014a492300002cbe220019004a492300002d8c220019004a492300003c45220019004a492300003d7c22010e020c19014a49230000461222010e020c19014a492300004f4f220019004a492300005125220019004a492300005317220019004a0e00012c000b2c00df1a000a49230000549d220119004a492300005f22220019000e00012c00ec27010c49230000606d220019000e00012c00ec27010e492300006155220019000e00012c00ec27010f49230000632d220019000e00012c00ec2701114923000063ed220019000e00012c00ec27011206230000645d45024700f723000064d445014700f80e00012c00f727011306230000650245024700f7230000655d45014700f80e00012c00f727011406230000658b45024700f723000065c445014700f80e00012c00f72701170623000065e145024700f7230000661945014700f80e00012c00f727011606230000667a45004700f7230000667c45004700f80e00012c00f727011849230000667e220119004a492300006702220019004a492300006f7a220019004a492300008575220019004a4923000087fd220019004a49230000908d220019004a0e0001330e0300180d0001362100060e03002c00022400090e03002c00021d00030e0301180d0001362100060e03012c00022400090e03012c00021d00030e0302180d0001362100060e03022c00022400090e03022c00021d00030e00032a2100080e0300180d0001362100060e03002c00032400090e03002c00031d0003230000045d45001d00040e03052c00091a000a4923000004c6220019001d0005061d0006060e00060d000b1c1d00074923000004f6220019000e00070d00141c1d00080e0008082c0011062300000617450247000e23000006494501470012230000065a450147001a230000073a45004700192300000785450047001323000007ab450147002019010e00070d00211c1d0009060e00060d00221c1d000a0623000007ed4501470018230000087745014700260e000a0d00271c1d000b0623000008ee4501470018230000095e45014700260e000a0d002a1c1d000c0623000009c6450147001823000009f545014700260e000a0d002c1c1d000d0e0008082c0011062300000a0e450047002f2300000a2245014700312300000a5d45014700382300000b4445004700132f0047003419010e00070d00391c1d000e0e000e082c0011060e0008082c0011190047003a2300000b68450147000e2300000b83450047002f2300000b9b450147003c2300000bb0450147003e1602002f20034700322300000bcf450147003f2300000bec450147004119010e00070d00421c1d000f060e00060d00431c1d00100e0006330e02032400580e02032c0004180d00053524001f0500041d0001041000150e0203082c00040e05032f01430119012f000033040e02032c0006180d00053524001d0500041d0002041000130e0203082c00062f041901082c0007190033040e05040d00084301303c3323000004d822001d000123000004da2201333c330e00010e010127000a0e010143001d0002490e010127000a0e00023306230000052a4501470011230000059f450047000923000005c0450047000e23000005c2450147000c2300000608450047001333490e03053919011d00020e000124000d0e0002082c000c0e000119014a0e0002082c000d0d000e19012a1a000b392c000e0e00022c000e3524000d230000058922000e000227000e0e00020e00022c000e27000a390e000227000f0e0002330e01022c000f2c000e082c0010390e000019024a3c3339082c001119001d00010e00012c000e082c00100e00010e000019024a0e0001333c330e00011b031300023b0324001e0e0001082c000d0e0002190124000c0e00010e000200390e00023a14ffda0e0001082c000d0d0012190124000a0e00012c0012392700123c33392c000e2c000a082c0011391901330e00011a00032d0000390d00151c1d00010e00023c1124000a0e00023927001614000d0e00012c00172f0402392700163c330e00011a00030e020b082c001839190133392c00151d00020e00012c00151d0003392c00161d00040e00012c00161d000539082c001919004a0e00042f040b24006a2f001d00060e00060e00051e2400580e00030e00062f0212002f180e00062f040b2f080246121600ff371d00070e00020e00040e00061f2f0212000e00072f180e00040e00061f2f040b2f080246292b0e00020e00040e00061f2f02121c4a130006254a14ff9e1400352f001d00080e00080e00051e2400260e00030e00082f0212000e00020e00040e00081f2f02123a0e00082f041f1300081c4a14ffd0392c00160e00051f390d00161c4a3933392c00151d0001392c00161d00020e00010e00022f02120042001b2f200e00022f040b2f08024629370e00010e00022f02121c4a0e0201082c001c0e00022f040319010e00012700173c330e02082c0013082c001d3919011d0001392c0015082c001e2f0019010e00012700150e0001332d00001d00022f001d00030e00030e00011e24001e0e0002082c001f490e0204190019014a0e00032f041f1300031c4a14ffd80e02092c000e0e00020e00014302330e00012c00151d00020e00012c00161d00032d00001d00042f001d00050e00050e00031e2400560e00020e00052f0212002f180e00052f040b2f080246121600ff371d00060e0004082c001f0e00062f0412082c00122f10190119014a0e0004082c001f0e00062f0f37082c00122f10190119014a130005254a14ffa00e0004082c00230d00241901330e00012c00171d00022d00001d00032f001d00040e00040e00021e2400470e00030e00042f031200490e05060e0001082c00250e00042f0219022f1019022f180e00042f080b2f040246292b0e00030e00042f03121c4a0e00042f021f1300041c4a14ffaf0e02092c000e0e00030e00022f02034302330e00012c00151d00020e00012c00161d00032d00001d00042f001d00050e00050e00031e24003c0e00020e00052f0212002f180e00052f040b2f080246121600ff371d00060e0004082c001f0e0507082c00280e0006190119014a130005254a14ffba0e0004082c00230d00241901330e00012c00171d00022d00001d00032f001d00040e00040e00021e24003b0e00030e00042f0212000e0001082c00290e000419011600ff372f180e00042f040b2f080246292b0e00030e00042f02121c4a130004254a14ffbb0e02092c000e0e00030e000243023305000d1d00020e05040d002b4301300410001a490e0508490e05090e020c082c00180e000119011901190133043c330e020c082c0026490e050a490e050b0e0001190119011901330e02092c000e43003927002d2f003927002e3c330e0001180d00303524000f0e020d082c00260e000119011d0001392c002d082c001a0e000119014a392c002e0e00012c00161f390d002e1c4a3c33392c002d1d00030e00032c00151d00040e00032c00161d0005392c00321d00060e00062f04021d00070e00050e0007031d00080e00012400120e0201082c001c0e000819011d00081400190e0201082c00330e00082f002b392c0034462f0019021d00080e00080e0006021d00090e0201082c00350e00092f04020e000519021d000a0e000924004f2f001d000b0e000b0e00091e24001d39082c00360e00040e000b19024a0e000b0e00061f13000b1c4a14ffd90e0004082c00372f000e000919021d00020e00032c00160e000a460e00030d00161c4a0e02092c000e0e00020e000a4302330e02082c0013082c001d3919011d0001392c002d082c001319000e000127002d0e000133392c003a082c00110e000119013927003a39082c002f19004a3c330e020e2c002f082c001d3919014a39082c003b19004a3c3339082c00310e000119014a39082c003819004a39330e000124000b39082c00310e000119014a39082c003d19001d00020e0002332300000bd72202330e01012c000e0e00024301082c003e0e00011901332300000bf42202330e03102c00402c000e0e01010e00024302082c003e0e00011901330e01011d00020e00022c000b1d00030e00032c00141d00040e00032c00211d0005060e00020d00441c1d00060e0004082c0011062300000c8d450247000e19010e00060d00471c1d00070e0004082c0011062300000c9d450247000e2300000ccf45004700482300000d37450047001319010e00060d00211c1d00083c330e0001392700450e0002392700463c330e00011a00032d0000390d00151c1d00010e00023c1124000a0e00023927001614000d0e00012c00172f0802392700163c33392c00151d00010e00012c00171d00022d00001d00032f001d00040e00040e00021e2400320e00010e0004001d00050e0003082c001f0e00052c004519014a0e0003082c001f0e00052c004619014a130004254a14ffc40e0205082c00090e0003392c00161902330e02042c0013082c001d3919011d0001392c0015082c001e2f0019010e00010d00151c1d00020e00022c00171d00032f001d00040e00040e00031e24001c0e00020e000400082c001319000e00020e00043a130004254a14ffda0e0001330e030d180d0005362400023c330e01011d00010e00012c000b1d00020e00022c00211d00030e00032c000e1d00042300000ddf22010e00030d000e1c1d00050e00030e000527000a3c330e00010e040d2624000b0e040e0e000143011d00010e00010e040f261a00120e0410180d0001362100070e00010e0410261a00070e00010e0411261a00070e00010e0412261a00070e00010e0413261a00070e00010e0403261a00070e00010e0414261a00070e00010e04152624001a0e040e0e00012c00490e00012c004a0e00012c004b43031d00010e00010e040e262400640e00012c004b1d00022d00001d00032f001d00040e00040e00021e2400320e00030e00042f0212000e00010e0004002f180e00042f040b2f080246292b0e00030e00042f02121c4a130004254a14ffc40e0104082c001d390e00030e000219034a14000e0e0104082c0010390e000019024a3c33230000112122011d00060e01011d00010e00012c000b1d00020e00022c00211d00030e00012c00221d0004062300000f5545014700182300000fcd45014700260e00040d004c1c0e00040d004d1c1d0005062300001035450147001823000010b345014700260e000427004e3c330e00012c00151d00020e00012c00161d00032d00001d00042f001d00050e00050e00031e2400440e00020e00052f0212002f100e00052f040b2f08024612230000ffff371d00060e0004082c001f0e0507082c00280e0006190119014a0e00052f021f1300051c4a14ffb20e0004082c00230d00241901330e00012c00171d00022d00001d00032f001d00040e00040e00021e2400370e00030e00042f0112000e0001082c00290e000419012f100e00042f020b2f100246292b0e00030e00042f01121c4a130004254a14ffbf0e0203082c00090e00030e00022f02021902330e00012c00151d00020e00012c00161d00032d00001d00042f001d00050e00050e00031e24004a490e02060e00020e00052f0212002f100e00052f040b2f08024612230000ffff3719011d00060e0004082c001f0e0507082c00280e0006190119014a0e00052f021f1300051c4a14ffac0e0004082c00230d00241901330e00012c00171d00022d00001d00032f001d00040e00040e00021e24003d0e00030e00042f011200490e02060e0001082c00290e000419012f100e00042f020b2f1002462919012b0e00030e00042f01121c4a130004254a14ffb90e0203082c00090e00030e00022f02021902330e00012f082942004f370e00012f08122300ff00ff372b33230000136c22031d00060e01011d00010e00012c000b1d00020e00022c00211d00030e00012c00221d000406230000118b450147001823000012d345014700260d00554700500e00040d00561c1d00053c330e00012c00151d00020e00012c00161d0003392c00501d00040e0001082c001919004a2d00001d00052f001d00060e00060e00031e2400d30e00020e00062f0212002f180e00062f040b2f080246121600ff371d00070e00020e00062f011f2f0212002f180e00062f011f2f040b2f080246121600ff371d00080e00020e00062f021f2f0212002f180e00062f021f2f040b2f080246121600ff371d00090e00072f10290e00082f08292b0e00092b1d000a2f001d000b0e000b2f041e21000f0e00060e000b420051021f0e00031e24002b0e0005082c001f0e0004082c00520e000a2f062f030e000b4602122f3f37190119014a13000b254a14ffba0e00062f031f1300061c4a14ff230e0004082c00522f4019011d000c0e000c24001c0e00052c00172f040b2400100e0005082c001f0e000c19014a14ffe40e0005082c00230d00241901330e00012c00171d0002392c00501d0003392c00531d00040e00042a2400382d0000390d00531c1d00042f001d00050e00050e00032c00171e24001b0e00050e00040e0003082c00290e000519013a130005254a14ffd80e0003082c00522f4019011d00060e000624001f0e0001082c00540e000619011d00070e00072f0140362400060e00071d0002490e02060e00010e00020e00041903332d00001d00042f001d00052f001d00060e00060e00021e2400860e00062f040b2400750e00030e0001082c00290e00062f01461901000e00062f040b2f0202291d00070e00030e0001082c00290e00061901002f060e00062f040b2f020246121d00080e00070e00082b1d00090e00040e00052f0212000e00092f180e00052f040b2f080246292b0e00040e00052f02121c4a130005254a130006254a14ff700e0103082c00090e00040e000519023323000016b722031d00060e01011d00010e00012c000b1d00020e00022c00211d00030e00012c00221d0004062300001474450147001823000015ed45014700260d00554700500d00584700570e00040d00591c1d00053c330e00002c00172f01312100080e00002f01003c362400090e00002f0100140001341d00020e00012c00151d00030e00012c00161d00040e0002240007392c0057140004392c00501d00050e0001082c001919004a2d00001d00062f001d00070e00070e00041e2400d30e00030e00072f0212002f180e00072f040b2f080246121600ff371d00080e00030e00072f011f2f0212002f180e00072f011f2f040b2f080246121600ff371d00090e00030e00072f021f2f0212002f180e00072f021f2f040b2f080246121600ff371d000a0e00082f10290e00092f08292b0e000a2b1d000b2f001d000c0e000c2f041e21000f0e00070e000c420051021f0e00041e24002b0e0006082c001f0e0005082c00520e000b2f062f030e000c4602122f3f37190119014a13000c254a14ffba0e00072f031f1300071c4a14ff230e0005082c00522f4019011d000d0e000d24001c0e00062c00172f040b2400100e0006082c001f0e000d19014a14ffe40e0006082c00230d00241901330e00002c00172f01312100080e00002f01003c362400090e00002f0100140001341d00020e00012c00171d00030e0002240007392c0057140004392c00501d0004392c00531d00050e00052a2400382d0000390d00531c1d00052f001d00060e00060e00042c00171e24001b0e00060e00050e0004082c00290e000619013a130006254a14ffd80e0004082c00522f4019011d00070e000724001f0e0001082c00540e000719011d00080e00082f0140362400060e00081d0003490e02060e00010e00030e00051903332d00001d00042f001d00052f001d00060e00060e00021e2400860e00062f040b2400750e00030e0001082c00290e00062f01461901000e00062f040b2f0202291d00070e00030e0001082c00290e00061901002f060e00062f040b2f020246121d00080e00070e00082b1d00090e00040e00052f0212000e00092f180e00052f040b2f080246292b0e00040e00052f02121c4a130005254a130006254a14ff700e0103082c00090e00040e0005190233230000239d22071d000923000023d322071d000a230000240922071d000b230000243a22071d000c0e01011d00020e00022c000b1d00030e00032c00211d00040e00032c00421d00050e00022c00431d00062d00001d000749230000182c220019004a0e0005082c001106230000186a450047003b230000188b4502470036230000222d450047003d2300002379450047001319010e00060d00611c1d00080e0005082c003f0e000819010e00022700610e0005082c00410e000819010e00022700623c332f001d00010e00012f401e24002e0e0101082c005a0e0101082c005b0e00012f011f1901190142005c022f002b0e01070e00013a130001254a14ffc93c330e02042c000e236745230142005d42005e23103254762d000443013927005f3c332f001d00030e00032f101e2400480e00020e00031f1d00040e00010e0004001d00050e00052f08290e00052f18122b2300ff00ff370e00052f18290e00052f08122b42004f372b0e00010e00043a130003254a14ffaf392c005f2c00151d00060e00010e00022f001f001d00070e00010e00022f011f001d00080e00010e00022f021f001d00090e00010e00022f031f001d000a0e00010e00022f041f001d000b0e00010e00022f051f001d000c0e00010e00022f061f001d000d0e00010e00022f071f001d000e0e00010e00022f081f001d000f0e00010e00022f091f001d00100e00010e00022f0a1f001d00110e00010e00022f0b1f001d00120e00010e00022f0c1f001d00130e00010e00022f0d1f001d00140e00010e00022f0e1f001d00150e00010e00022f0f1f001d00160e00062f00001d00170e00062f01001d00180e00062f02001d00190e00062f03001d001a490e02090e00170e00180e00190e001a0e00072f070e02072f000019071d0017490e02090e001a0e00170e00180e00190e00082f0c0e02072f010019071d001a490e02090e00190e001a0e00170e00180e00092f110e02072f020019071d0019490e02090e00180e00190e001a0e00170e000a2f160e02072f030019071d0018490e02090e00170e00180e00190e001a0e000b2f070e02072f040019071d0017490e02090e001a0e00170e00180e00190e000c2f0c0e02072f050019071d001a490e02090e00190e001a0e00170e00180e000d2f110e02072f060019071d0019490e02090e00180e00190e001a0e00170e000e2f160e02072f070019071d0018490e02090e00170e00180e00190e001a0e000f2f070e02072f080019071d0017490e02090e001a0e00170e00180e00190e00102f0c0e02072f090019071d001a490e02090e00190e001a0e00170e00180e00112f110e02072f0a0019071d0019490e02090e00180e00190e001a0e00170e00122f160e02072f0b0019071d0018490e02090e00170e00180e00190e001a0e00132f070e02072f0c0019071d0017490e02090e001a0e00170e00180e00190e00142f0c0e02072f0d0019071d001a490e02090e00190e001a0e00170e00180e00152f110e02072f0e0019071d0019490e02090e00180e00190e001a0e00170e00162f160e02072f0f0019071d0018490e020a0e00170e00180e00190e001a0e00082f050e02072f100019071d0017490e020a0e001a0e00170e00180e00190e000d2f090e02072f110019071d001a490e020a0e00190e001a0e00170e00180e00122f0e0e02072f120019071d0019490e020a0e00180e00190e001a0e00170e00072f140e02072f130019071d0018490e020a0e00170e00180e00190e001a0e000c2f050e02072f140019071d0017490e020a0e001a0e00170e00180e00190e00112f090e02072f150019071d001a490e020a0e00190e001a0e00170e00180e00162f0e0e02072f160019071d0019490e020a0e00180e00190e001a0e00170e000b2f140e02072f170019071d0018490e020a0e00170e00180e00190e001a0e00102f050e02072f180019071d0017490e020a0e001a0e00170e00180e00190e00152f090e02072f190019071d001a490e020a0e00190e001a0e00170e00180e000a2f0e0e02072f1a0019071d0019490e020a0e00180e00190e001a0e00170e000f2f140e02072f1b0019071d0018490e020a0e00170e00180e00190e001a0e00142f050e02072f1c0019071d0017490e020a0e001a0e00170e00180e00190e00092f090e02072f1d0019071d001a490e020a0e00190e001a0e00170e00180e000e2f0e0e02072f1e0019071d0019490e020a0e00180e00190e001a0e00170e00132f140e02072f1f0019071d0018490e020b0e00170e00180e00190e001a0e000c2f040e02072f200019071d0017490e020b0e001a0e00170e00180e00190e000f2f0b0e02072f210019071d001a490e020b0e00190e001a0e00170e00180e00122f100e02072f220019071d0019490e020b0e00180e00190e001a0e00170e00152f170e02072f230019071d0018490e020b0e00170e00180e00190e001a0e00082f040e02072f240019071d0017490e020b0e001a0e00170e00180e00190e000b2f0b0e02072f250019071d001a490e020b0e00190e001a0e00170e00180e000e2f100e02072f260019071d0019490e020b0e00180e00190e001a0e00170e00112f170e02072f270019071d0018490e020b0e00170e00180e00190e001a0e00142f040e02072f280019071d0017490e020b0e001a0e00170e00180e00190e00072f0b0e02072f290019071d001a490e020b0e00190e001a0e00170e00180e000a2f100e02072f2a0019071d0019490e020b0e00180e00190e001a0e00170e000d2f170e02072f2b0019071d0018490e020b0e00170e00180e00190e001a0e00102f040e02072f2c0019071d0017490e020b0e001a0e00170e00180e00190e00132f0b0e02072f2d0019071d001a490e020b0e00190e001a0e00170e00180e00162f100e02072f2e0019071d0019490e020b0e00180e00190e001a0e00170e00092f170e02072f2f0019071d0018490e020c0e00170e00180e00190e001a0e00072f060e02072f300019071d0017490e020c0e001a0e00170e00180e00190e000e2f0a0e02072f310019071d001a490e020c0e00190e001a0e00170e00180e00152f0f0e02072f320019071d0019490e020c0e00180e00190e001a0e00170e000c2f150e02072f330019071d0018490e020c0e00170e00180e00190e001a0e00132f060e02072f340019071d0017490e020c0e001a0e00170e00180e00190e000a2f0a0e02072f350019071d001a490e020c0e00190e001a0e00170e00180e00112f0f0e02072f360019071d0019490e020c0e00180e00190e001a0e00170e00082f150e02072f370019071d0018490e020c0e00170e00180e00190e001a0e000f2f060e02072f380019071d0017490e020c0e001a0e00170e00180e00190e00162f0a0e02072f390019071d001a490e020c0e00190e001a0e00170e00180e000d2f0f0e02072f3a0019071d0019490e020c0e00180e00190e001a0e00170e00142f150e02072f3b0019071d0018490e020c0e00170e00180e00190e001a0e000b2f060e02072f3c0019071d0017490e020c0e001a0e00170e00180e00190e00122f0a0e02072f3d0019071d001a490e020c0e00190e001a0e00170e00180e00092f0f0e02072f3e0019071d0019490e020c0e00180e00190e001a0e00170e00102f150e02072f3f0019071d00180e00062f00000e00171f2f002b0e00062f003a0e00062f01000e00181f2f002b0e00062f013a0e00062f02000e00191f2f002b0e00062f023a0e00062f03000e001a1f2f002b0e00062f033a3c33392c002d1d00010e00012c00151d0002392c002e2f08021d00030e00012c00162f08021d00040e00020e00042f0512001600802f180e00042f200b46292b0e00020e00042f05121c4a0e0201082c00600e000342005c0319011d00050e00031d00060e00052f08290e00052f18122b2300ff00ff370e00052f18290e00052f08122b42004f372b0e00020e00042f401f2f09122f04292f0f1f3a0e00062f08290e00062f18122b2300ff00ff370e00062f18290e00062f08122b42004f372b0e00020e00042f401f2f09122f04292f0e1f3a0e00022c00172f011f2f04020e000127001639082c003819004a392c005f1d00070e00072c00151d00082f001d00090e00092f041e24003e0e00080e0009001d000a0e000a2f08290e000a2f18122b2300ff00ff370e000a2f18290e000a2f08122b42004f372b0e00080e00093a130009254a14ffb90e0007330e02052c0013082c001d3919011d0001392c005f082c001319000e000127005f0e0001330e00010e00020e0003370e00024c0e0004372b1f0e00051f0e00071f1d00080e00080e0006290e00082f200e000646122b0e00021f330e00010e00020e0004370e00030e00044c372b1f0e00051f0e00071f1d00080e00080e0006290e00082f200e000646122b0e00021f330e00010e00020e00030a0e00040a1f0e00051f0e00071f1d00080e00080e0006290e00082f200e000646122b0e00021f330e00010e00030e00020e00044c2b0a1f0e00051f0e00071f1d00080e00080e0006290e00082f200e000646122b0e00021f330e01011d00010e00012c000b1d00020e00022c00211d00030e00022c00421d00040e00012c00431d00052d00001d00060e0004082c00110623000024fe450047003b230000252245024700362300002714450047003d23000027b2450047001319010e00050d00641c1d00070e0004082c003f0e000719010e00012700640e0004082c00410e000719010e00012700653c330e02032c000e236745230142005d42005e23103254764200632d000543013927005f3c33392c005f2c00151d00030e00032f00001d00040e00032f01001d00050e00032f02001d00060e00032f03001d00070e00032f04001d00082f001d00090e00092f501e24014c0e00092f101e2400180e00010e00020e00091f002f002b0e02060e00093a1400420e02060e00092f0346000e02060e00092f0846000a0e02060e00092f0e46000a0e02060e00092f1046000a1d000a0e000a2f01290e000a2f1f122b0e02060e00093a0e00042f05290e00042f1b122b0e00081f0e02060e0009001f1d000b0e00092f141e2400220e000b0e00050e0006370e00054c0e0007372b235a8279991f1f13000b1c4a1400720e00092f281e24001d0e000b0e00050e00060a0e00070a236ed9eba11f1f13000b1c4a14004c0e00092f3c1e2400290e000b0e00050e0006370e00050e0007372b0e00060e0007372b2370e44324461f13000b1c4a14001a0e000b0e00050e00060a0e00070a23359d3e2a461f13000b1c4a0e00071d00080e00061d00070e00052f1e290e00052f02122b1d00060e00041d00050e000b1d0004130009254a14feab0e00032f00000e00041f2f002b0e00032f003a0e00032f01000e00051f2f002b0e00032f013a0e00032f02000e00061f2f002b0e00032f023a0e00032f03000e00071f2f002b0e00032f033a0e00032f04000e00081f2f002b0e00032f043a3c33392c002d1d00010e00012c00151d0002392c002e2f08021d00030e00012c00162f08021d00040e00020e00042f0512001600802f180e00042f200b46292b0e00020e00042f05121c4a0e050c082c00600e000342005c0319010e00020e00042f401f2f09122f04292f0e1f3a0e00030e00020e00042f401f2f09122f04292f0f1f3a0e00022c00172f04020e000127001639082c003819004a392c005f330e02042c0013082c001d3919011d0001392c005f082c001319000e000127005f0e0001330e01011d00020e00022c000b1d00030e00032c00211d00040e00032c00421d00050e00022c00431d00062d00001d00072d00001d000849230000287f220019004a2d00001d00090e0005082c001106230000294d450047003b230000296645024700362300002bfc450047003d2300002c9a450047001319010e00060d00681c1d000a0e0005082c003f0e000a19010e00022700680e0005082c00410e000a19010e00022700693c33230000290622011d0001230000293b22011d00022f021d00032f001d00040e00042f401e24005e490e00010e0003190124004a0e00042f081e24001e490e00020e0101082c00670e00032f012f0203190219010e01070e00043a490e00020e0101082c00670e00032f012f0303190219010e01080e00043a130004254a130003254a14ff993c330e0201082c00660e000119011d00022f021d00030e00030e0002152400150e00010e00030b2a2400020f33130003254a14ffe134330e00010e00012f002b4642005c022f002b330e02042c000e0e0207082c001e2f00190143013927005f3c33392c005f2c00151d00030e00032f00001d00040e00032f01001d00050e00032f02001d00060e00032f03001d00070e00032f04001d00080e00032f05001d00090e00032f06001d000a0e00032f07001d000b2f001d000c0e000c2f401e24019c0e000c2f101e2400180e00010e00020e000c1f002f002b0e02090e000c3a1400880e02090e000c2f0f46001d000d0e000d2f19290e000d2f07122b0e000d2f0e290e000d2f12122b0a0e000d2f03120a1d000e0e02090e000c2f0246001d000f0e000f2f0f290e000f2f11122b0e000f2f0d290e000f2f13122b0a0e000f2f0a120a1d00100e000e0e02090e000c2f0746001f0e00101f0e02090e000c2f1046001f0e02090e000c3a0e00080e0009370e00084c0e000a370a1d00110e00040e0005370e00040e0006370a0e00050e0006370a1d00120e00042f1e290e00042f02122b0e00042f13290e00042f0d122b0a0e00042f0a290e00042f16122b0a1d00130e00082f1a290e00082f06122b0e00082f15290e00082f0b122b0a0e00082f07290e00082f19122b0a1d00140e000b0e00141f0e00111f0e02080e000c001f0e02090e000c001f1d00150e00130e00121f1d00160e000a1d000b0e00091d000a0e00081d00090e00070e00151f2f002b1d00080e00061d00070e00051d00060e00041d00050e00150e00161f2f002b1d000413000c254a14fe5b0e00032f00000e00041f2f002b0e00032f003a0e00032f01000e00051f2f002b0e00032f013a0e00032f02000e00061f2f002b0e00032f023a0e00032f03000e00071f2f002b0e00032f033a0e00032f04000e00081f2f002b0e00032f043a0e00032f05000e00091f2f002b0e00032f053a0e00032f06000e000a1f2f002b0e00032f063a0e00032f07000e000b1f2f002b0e00032f073a3c33392c002d1d00010e00012c00151d0002392c002e2f08021d00030e00012c00162f08021d00040e00020e00042f0512001600802f180e00042f200b46292b0e00020e00042f05121c4a0e0201082c00600e000342005c0319010e00020e00042f401f2f09122f04292f0e1f3a0e00030e00020e00042f401f2f09122f04292f0f1f3a0e00022c00172f04020e000127001639082c003819004a392c005f330e02052c0013082c001d3919011d0001392c005f082c001319000e000127005f0e0001330e01011d00010e00012c000b1d00020e00022c00211d00030e00012c00431d00040e00042c00681d00050e0005082c0011062300002d36450047003b2300002d67450047003d19010e00040d006e1c1d00060e0005082c003f0e000619010e000127006e0e0005082c00410e000619010e000127006f3c330e02032c000e42006a23367cd507233070dd1742006b42006c23685815112364f98fa742006d2d000843013927005f3c330e02052c003d082c001d3919011d00010e00012c00162f04460e00010d00161c4a0e00013323000032b822001d00080e01011d00010e00012c000b1d00020e00022c00421d00030e00012c00441d00040e00042c00471d00050e00042c00211d00060e00012c00431d0007490e000823428a2f984200701902490e000823713744912323ef65cd1902490e00084200714200721902490e00084200734200741902490e0008233956c25b4200751902490e00082359f111f14200761902490e00084200774200781902490e000842007942007a1902490e000842007b42007c1902490e00082312835b012345706fbe1902490e000823243185be234ee4b28c1902490e000823550c7dc342007d1902490e00082372be5d7442007e1902490e000842007f233b1696b11902490e00084200802325c712351902490e00084200814200821902490e00084200834200841902490e000842008523384f25e31902490e0008230fc19dc64200861902490e000823240ca1cc2377ac9c651902490e0008232de92c6f23592b02751902490e0008234a7484aa236ea6e4831902490e0008235cb0a9dc4200871902490e00082376f988da4200881902490e000842008942008a1902490e000842008b232db432101902490e000842008c42008d1902490e000842008e42008f1902490e0008420090233da88fc21902490e00084200914200921902490e00082306ca63514200931902490e00082314292967230a0e6e701902490e00082327b70a852346d22ffc1902490e0008232e1b2138235c26c9261902490e0008234d2c6dfc235ac42aed1902490e00082353380d134200941902490e000823650a73544200951902490e000823766a0abb233c77b2a81902490e00084200962347edaee61902490e0008420097231482353b1902490e0008420098234cf103641902490e000842009942009a1902490e000842009b42009c1902490e000842009d230654be301902490e000842009e42009f1902490e00084200a0235565a9101902490e00084200a1235771202a1902490e000823106aa0702332bbd1b81902490e00082319a4c1164200a21902490e0008231e376c08235141ab531902490e0008232748774c4200a31902490e00082334b0bcb54200a41902490e000823391c0cb34200a51902490e0008234ed8aa4a4200a61902490e0008235b9cca4f237763e3731902490e000823682e6ff34200a71902490e000823748f82ee235defb2fc1902490e00082378a5636f2343172f601902490e00084200a84200a91902490e00084200aa231a6439ec1902490e00084200ab2323631e281902490e00084200ac4200ad1902490e00084200ae4200af1902490e00084200b04200b11902490e00084200b24200b31902490e00084200b42321c0c2071902490e00084200b54200b61902490e00084200b74200b81902490e00082306f067aa2372176fba1902490e0008230a637dc54200b91902490e000823113f98044200ba1902490e0008231b710b3523131c471b1902490e00082328db77f52323047d841902490e00082332caab7b2340c724931902490e0008233c9ebe0a2315c9bebc1902490e000823431d67c44200bb1902490e0008234cc5d4be4200bc1902490e000823597f299c4200bd1902490e0008235fcb6fab233ad6faec1902490e0008236c44198c234a47581719022d00501d00092d00001d000a492300003304220019004a0e0003082c0011062300003329450047003b23000033ba45024700362300003b75450047003d2300003c2145004700131604002f200347003219010e00070d00c61c1d000b0e0003082c003f0e000b19010e00012700c60e0003082c00410e000b19010e00012700c73c330e00002c00171d00010e04160e000143011d00022f001d00030e00030e00011e2400160e00000e0003000e00020e00033a130003254a14ffe00e01052c0009082c00100e01050e00001902332f001d00010e00012f501e240015490e010819000e010a0e00013a130001254a14ffe23c330e02062c000e0e02052c000e236a09e6674200be43020e02052c000e4200bf4200c043020e02052c000e233c6ef3724200c143020e02052c000e4200c2235f1d36f143020e02052c000e23510e527f4200c343020e02052c000e4200c4232b3e6c1f43020e02052c000e231f83d9ab4200c543020e02052c000e235be0cd1923137e217943022d000843013927005f3c33392c005f2c00151d00030e00032f00001d00040e00032f01001d00050e00032f02001d00060e00032f03001d00070e00032f04001d00080e00032f05001d00090e00032f06001d000a0e00032f07001d000b0e00042c00451d000c0e00042c00461d000d0e00052c00451d000e0e00052c00461d000f0e00062c00451d00100e00062c00461d00110e00072c00451d00120e00072c00461d00130e00082c00451d00140e00082c00461d00150e00092c00451d00160e00092c00461d00170e000a2c00451d00180e000a2c00461d00190e000b2c00451d001a0e000b2c00461d001b0e000c1d001c0e000d1d001d0e000e1d001e0e000f1d001f0e00101d00200e00111d00210e00121d00220e00131d00230e00141d00240e00151d00250e00161d00260e00171d00270e00181d00280e00191d00290e001a1d002a0e001b1d002b2f001d002c0e002c2f501e2404b90e020a0e002c001d002f0e002c2f101e24003c0e00010e00020e002c2f02021f002f002b0e002f0d00451c1d002e0e00010e00020e002c2f02021f2f011f002f002b0e002f0d00461c1d002d1401b40e020a0e002c2f0f46001d00300e00302c00451d00310e00302c00461d00320e00312f01120e00322f1f292b0e00312f08120e00322f18292b0a0e00312f07120a1d00330e00322f01120e00312f1f292b0e00322f08120e00312f18292b0a0e00322f07120e00312f19292b0a1d00340e020a0e002c2f0246001d00350e00352c00451d00360e00352c00461d00370e00362f13120e00372f0d292b0e00362f03290e00372f1d122b0a0e00362f06120a1d00380e00372f13120e00362f0d292b0e00372f03290e00362f1d122b0a0e00372f06120e00362f1a292b0a1d00390e020a0e002c2f0746001d003a0e003a2c00451d003b0e003a2c00461d003c0e020a0e002c2f1046001d003d0e003d2c00451d003e0e003d2c00461d003f0e00340e003c1f1d002d0e00330e003b1f0e002d2f00120e00342f00121e2400052f011400022f001f1d002e0e002d0e00391f1d002d0e002e0e00381f0e002d2f00120e00392f00121e2400052f011400022f001f1d002e0e002d0e003f1f1d002d0e002e0e003e1f0e002d2f00120e003f2f00121e2400052f011400022f001f1d002e0e002e0e002f2700450e002d0e002f2700460e00240e0026370e00244c0e0028370a1d00400e00250e0027370e00254c0e0029370a1d00410e001c0e001e370e001c0e0020370a0e001e0e0020370a1d00420e001d0e001f370e001d0e0021370a0e001f0e0021370a1d00430e001c2f1c120e001d2f04292b0e001c2f1e290e001d2f02122b0a0e001c2f19290e001d2f07122b0a1d00440e001d2f1c120e001c2f04292b0e001d2f1e290e001c2f02122b0a0e001d2f19290e001c2f07122b0a1d00450e00242f0e120e00252f12292b0e00242f12120e00252f0e292b0a0e00242f17290e00252f09122b0a1d00460e00252f0e120e00242f12292b0e00252f12120e00242f0e292b0a0e00252f17290e00242f09122b0a1d00470e02090e002c001d00480e00482c00451d00490e00482c00461d004a0e002b0e00471f1d004b0e002a0e00461f0e004b2f00120e002b2f00121e2400052f011400022f001f1d004c0e004b0e00411f1d004b0e004c0e00401f0e004b2f00120e00412f00121e2400052f011400022f001f1d004c0e004b0e004a1f1d004b0e004c0e00491f0e004b2f00120e004a2f00121e2400052f011400022f001f1d004c0e004b0e002d1f1d004b0e004c0e002e1f0e004b2f00120e002d2f00121e2400052f011400022f001f1d004c0e00450e00431f1d004d0e00440e00421f0e004d2f00120e00452f00121e2400052f011400022f001f1d004e0e00281d002a0e00291d002b0e00261d00280e00271d00290e00241d00260e00251d00270e00230e004b1f2f002b1d00250e00220e004c1f0e00252f00120e00232f00121e2400052f011400022f001f2f002b1d00240e00201d00220e00211d00230e001e1d00200e001f1d00210e001c1d001e0e001d1d001f0e004b0e004d1f2f002b1d001d0e004c0e004e1f0e001d2f00120e004b2f00121e2400052f011400022f001f2f002b1d001c13002c254a14fb3e0e000d0e001d1f0e00040d00461c1d000d0e000c0e001c1f0e000d2f00120e001d2f00121e2400052f011400022f001f0e00042700450e000f0e001f1f0e00050d00461c1d000f0e000e0e001e1f0e000f2f00120e001f2f00121e2400052f011400022f001f0e00052700450e00110e00211f0e00060d00461c1d00110e00100e00201f0e00112f00120e00212f00121e2400052f011400022f001f0e00062700450e00130e00231f0e00070d00461c1d00130e00120e00221f0e00132f00120e00232f00121e2400052f011400022f001f0e00072700450e00150e00251f0e00080d00461c1d00150e00140e00241f0e00152f00120e00252f00121e2400052f011400022f001f0e00082700450e00170e00271f0e00090d00461c1d00170e00160e00261f0e00172f00120e00272f00121e2400052f011400022f001f0e00092700450e00190e00291f0e000a0d00461c1d00190e00180e00281f0e00192f00120e00292f00121e2400052f011400022f001f0e000a2700450e001b0e002b1f0e000b0d00461c1d001b0e001a0e002a1f0e001b2f00120e002b2f00121e2400052f011400022f001f0e000b2700453c33392c002d1d00010e00012c00151d0002392c002e2f08021d00030e00012c00162f08021d00040e00020e00042f0512001600802f180e00042f200b46292b0e00020e00042f05121c4a0e050c082c00600e000342005c0319010e00020e00041600801f2f0a122f05292f1e1f3a0e00030e00020e00041600801f2f0a122f05292f1f1f3a0e00022c00172f04020e000127001639082c003819004a392c005f082c004819001d00050e0005330e02032c0013082c001d3919011d0001392c005f082c001319000e000127005f0e0001330e01011d00010e00012c00441d00020e00022c00471d00030e00022c00211d00040e00012c00431d00050e00052c00c61d00060e0006082c0011062300003cc6450047003b2300003d57450047003d19010e00050d00cc1c1d00070e0006082c003f0e000719010e00012700cc0e0006082c00410e000719010e00012700cd3c330e02042c000e0e02032c000e4200c842006a43020e02032c000e23629a292a23367cd50743020e02032c000e4200c9233070dd1743020e02032c000e23152fecd842006b43020e02032c000e236733266742006c43020e02032c000e4200ca236858151143020e02032c000e4200cb2364f98fa743020e02032c000e2347b5481d42006d43022d000843013927005f3c330e02062c003d082c001d3919011d00010e00012c00162f10460e00010d00161c4a0e0001330e01011d00020e00022c000b1d00030e00032c00211d00040e00032c00421d00050e00022c00441d00060e00062c00471d00070e00022c00431d00082d00001d00092d00001d000a2d00001d000b492300003e5e220019004a2d00001d000c492300003fd1220019004a0e0005082c0011060e00052c003a082c0011061602004700ce190147003a2300003ff9450047003b23000040404502470036230000443f450047003d23000045be450047001319010e00080d00d01c1d000d0e0005082c003f0e000d19010e00022700d00e0005082c00410e000d19010e00022700d13c332f011d00012f001d00022f001d00030e00032f181e2400510e00032f011f0e00032f021f022f02032f400b0e01090e00012f050e0002021f3a0e00022f050b1d00042f020e0001022f030e0002021f2f050b1d00050e00041d00010e00051d0002130003254a14ffa62f001d00010e00012f051e2400432f001d00020e00022f051e24002d0e00022f020e0001022f030e0002021f2f050b2f05021f0e010a0e00012f050e0002021f3a130002254a14ffca130001254a14ffb42f011d00062f001d00070e00072f181e2400a42f001d00082f001d00092f001d000a0e000a2f071e24006e0e00062f01372400392f010e000a292f01461d000b0e000b2f201e2400120e00092f010e000b290a1300091c4a1400120e00082f010e000b2f2046290a1300081c4a0e00061600803724000f0e00062f01292f710a1d000614000b0e00062f01291300061c4a13000a254a14ff890e0107082c00090e00080e000919020e010b0e00073a130007254a14ff533c332f001d00010e00012f191e2400180e0107082c000919000e010c0e00013a130001254a14ffdf3c332d0000390d00cf1c1d00012f001d00020e00022f191e2400170e02072c000e43000e00010e00023a130002254a14ffe01606402f02392c003a2c00ce02462f2003392700323c33392c00cf1d0003392c00322f02031d00042f001d00050e00050e00041e2400ab0e00010e00022f020e0005021f001d00060e00010e00022f020e0005021f2f011f001d00070e00062f08290e00062f18122b2300ff00ff370e00062f18290e00062f08122b42004f372b1d00060e00072f08290e00072f18122b2300ff00ff370e00072f18290e00072f08122b42004f372b1d00070e00030e0005001d00080e00082c00450e00070a0e00080d00451c4a0e00082c00460e00060a0e00080d00461c4a130005254a14ff4b2f001d00090e00092f181e2403242f001d000a0e000a2f051e2400732f001d000b2f001d000c2f001d000d0e000d2f051e2400370e00030e000a2f050e000d021f001d00080e000b0e00082c00450a13000b1c4a0e000c0e00082c00460a13000c1c4a13000d254a14ffc00e020c0e000a001d000e0e000b0e000e2700450e000c0e000e27004613000a254a14ff842f001d000a0e000a2f051e2400b30e020c0e000a2f041f2f050b001d000f0e020c0e000a2f011f2f050b001d00100e00102c00451d00110e00102c00461d00120e000f2c00450e00112f01290e00122f1f122b0a1d000b0e000f2c00460e00122f01290e00112f1f122b0a1d000c2f001d000d0e000d2f051e24003d0e00030e000a2f050e000d021f001d00080e00082c00450e000b0a0e00080d00451c4a0e00082c00460e000c0a0e00080d00461c4a13000d254a14ffba13000a254a14ff442f011d00130e00132f191e2400b40e00030e0013001d00080e00082c00451d00140e00082c00461d00150e02090e0013001d00160e00162f201e24002d0e00140e0016290e00152f200e001646122b1d000b0e00150e0016290e00142f200e001646122b1d000c1400300e00150e00162f2046290e00142f400e001646122b1d000b0e00140e00162f2046290e00152f400e001646122b1d000c0e020c0e020a0e001300001d00170e000b0e00172700450e000c0e0017270046130013254a14ff430e020c2f00001d00180e00032f00001d00190e00192c00450e00182700450e00192c00460e00182700462f001d000a0e000a2f051e2400a32f001d000d0e000d2f051e24008d0e000a2f050e000d021f1d00130e00030e0013001d00080e020c0e0013001d001a0e020c0e000a2f011f2f050b2f050e000d021f001d001b0e020c0e000a2f021f2f050b2f050e000d021f001d001c0e001a2c00450e001b2c00454c0e001c2c0045370a0e00082700450e001a2c00460e001b2c00464c0e001c2c0046370a0e000827004613000d254a14ff6a13000a254a14ff540e00032f00001d00080e020b0e0009001d001d0e00082c00450e001d2c00450a0e00080d00451c4a0e00082c00460e001d2c00460a0e00080d00461c4a130009254a14fcd33c33392c002d1d00010e00012c00151d0002392c002e2f08021d00030e00012c00162f08021d0004392c00322f20021d00050e00020e00042f0512002f012f180e00042f200b46292b0e00020e00042f05121c4a0e00020e0201082c001c0e00042f011f0e00050319010e0005022f05122f0146001600802b0e00020e0201082c001c0e00042f011f0e00050319010e0005022f05122f01461c4a0e00022c00172f04020e000127001639082c003819004a392c00cf1d0006392c003a2c00ce2f08031d00070e00072f08031d00082d00001d00092f001d000a0e000a0e00081e24008e0e00060e000a001d000b0e000b2c00451d000c0e000b2c00461d000d0e000c2f08290e000c2f18122b2300ff00ff370e000c2f18290e000c2f08122b42004f372b1d000c0e000d2f08290e000d2f18122b2300ff00ff370e000d2f18290e000d2f08122b42004f372b1d000d0e0009082c001f0e000d19014a0e0009082c001f0e000c19014a13000a254a14ff680e02042c000e0e00090e00074302330e02052c0013082c001d3919011d0001392c00cf082c001e2f0019010e00010d00cf1c1d00022f001d00030e00032f191e24001c0e00020e000300082c001319000e00020e00033a130003254a14ffdb0e0001332300004ef422031d000e2300004f0022031d000f2300004f1122031d00102300004f1e22031d00112300004f2f22031d00122300004f3c22021d00130e01011d00020e00022c000b1d00030e00032c00211d00040e00032c00421d00050e00022c00431d00060e0004082c00092f002f012f022f032f042f052f062f072f082f092f0a2f0b2f0c2f0d2f0e2f0f2f072f042f0d2f012f0a2f062f0f2f032f0c2f002f092f052f022f0e2f0b2f082f032f0a2f0e2f042f092f0f2f082f012f022f072f002f062f0d2f0b2f052f0c2f012f092f0b2f0a2f002f082f0c2f042f0d2f032f072f0f2f0e2f052f062f022f042f002f052f092f072f0c2f022f0a2f0e2f012f032f082f0b2f062f0f2f0d2d005019011d00070e0004082c00092f052f0e2f072f002f092f022f0b2f042f0d2f062f0f2f082f012f0a2f032f0c2f062f0b2f032f072f002f0d2f052f0a2f0e2f0f2f082f0c2f042f092f012f022f0f2f052f012f032f072f0e2f062f092f0b2f082f0c2f022f0a2f002f042f0d2f082f062f042f012f032f0b2f0f2f002f052f0c2f022f0d2f092f072f0a2f0e2f0c2f0f2f0a2f042f012f052f082f072f062f022f0d2f0e2f002f032f092f0b2d005019011d00080e0004082c00092f0b2f0e2f0f2f0c2f052f082f072f092f0b2f0d2f0e2f0f2f062f072f092f082f072f062f082f0d2f0b2f092f072f0f2f072f0c2f0f2f092f0b2f072f0d2f0c2f0b2f0d2f062f072f0e2f092f0d2f0f2f0e2f082f0d2f062f052f0c2f072f052f0b2f0c2f0e2f0f2f0e2f0f2f092f082f092f0e2f052f062f082f062f052f0c2f092f0f2f052f0b2f062f082f0d2f0c2f052f0c2f0d2f0e2f0b2f082f052f062d005019011d00090e0004082c00092f082f092f092f0b2f0d2f0f2f0f2f052f072f072f082f0b2f0e2f0e2f0c2f062f092f0d2f0f2f072f0c2f082f092f0b2f072f072f0c2f072f062f0f2f0d2f0b2f092f072f0f2f0b2f082f062f062f0e2f0c2f0d2f052f0e2f0d2f0d2f072f052f0f2f052f082f0b2f0e2f0e2f062f0e2f062f092f0c2f092f0c2f052f0f2f082f082f052f0c2f092f0c2f052f0e2f062f082f0d2f062f052f0f2f0d2f0b2f0b2d005019011d000a0e0004082c00092f00235a827999236ed9eba14200d24200d32d000519011d000b0e0004082c00092350a28be6235c4dd124236d703ef3237a6d76e92f002d000519011d000c0e0005082c00110623000049dc450047003b2300004a0145024700362300004dd5450047003d2300004ed0450047001319010e00060d00d41c1d000d0e0005082c003f0e000d19010e00022700d40e0005082c00410e000d19010e00022700d53c330e0204082c0009236745230142005d42005e23103254764200632d000519013927005f3c332f001d00030e00032f101e2400480e00020e00031f1d00040e00010e0004001d00050e00052f08290e00052f18122b2300ff00ff370e00052f18290e00052f08122b42004f372b0e00010e00043a130003254a14ffaf392c005f2c00151d00060e020b2c00151d00070e020c2c00151d00080e02072c00151d00090e02082c00151d000a0e02092c00151d000b0e020a2c00151d000c0e00062f000013000d1c1d00120e00062f010013000e1c1d00130e00062f020013000f1c1d00140e00062f03001300101c1d00150e00062f04001300111c1d00162f001d00030e00032f501e2402740e000d0e00010e00020e00090e0003001f001f2f002b1d00170e00032f101e2400220e0017490e020e0e000e0e000f0e001019030e00072f00001f1f1300171c4a1400a00e00032f201e2400220e0017490e020f0e000e0e000f0e001019030e00072f01001f1f1300171c4a1400750e00032f301e2400220e0017490e02100e000e0e000f0e001019030e00072f02001f1f1300171c4a14004a0e00032f401e2400220e0017490e02110e000e0e000f0e001019030e00072f03001f1f1300171c4a14001f0e0017490e02120e000e0e000f0e001019030e00072f04001f1f1300171c4a0e00172f002b1d0017490e02130e00170e000b0e00030019021d00170e00170e00111f2f002b1d00170e00111d000d0e00101d0011490e02130e000f2f0a19021d00100e000e1d000f0e00171d000e0e00120e00010e00020e000a0e0003001f001f2f002b1d00170e00032f101e2400220e0017490e02120e00130e00140e001519030e00082f00001f1f1300171c4a1400a00e00032f201e2400220e0017490e02110e00130e00140e001519030e00082f01001f1f1300171c4a1400750e00032f301e2400220e0017490e02100e00130e00140e001519030e00082f02001f1f1300171c4a14004a0e00032f401e2400220e0017490e020f0e00130e00140e001519030e00082f03001f1f1300171c4a14001f0e0017490e020e0e00130e00140e001519030e00082f04001f1f1300171c4a0e00172f002b1d0017490e02130e00170e000c0e00030019021d00170e00170e00161f2f002b1d00170e00161d00120e00151d0016490e02130e00142f0a19021d00150e00131d00140e00171d00130e00032f011f1300031c4a14fd830e00062f01000e000f1f0e00151f2f002b1d00170e00062f02000e00101f0e00161f2f002b0e00062f013a0e00062f03000e00111f0e00121f2f002b0e00062f023a0e00062f04000e000d1f0e00131f2f002b0e00062f033a0e00062f00000e000e1f0e00141f2f002b0e00062f043a0e00170e00062f003a3c33392c002d1d00010e00012c00151d0002392c002e2f08021d00030e00012c00162f08021d00040e00020e00042f0512001600802f180e00042f200b46292b0e00020e00042f05121c4a0e00032f08290e00032f18122b2300ff00ff370e00032f18290e00032f08122b42004f372b0e00020e00042f401f2f09122f04292f0e1f3a0e00022c00172f011f2f04020e000127001639082c003819004a392c005f1d00050e00052c00151d00062f001d00070e00072f051e24003e0e00060e0007001d00080e00082f08290e00082f18122b2300ff00ff370e00082f18290e00082f08122b42004f372b0e00060e00073a130007254a14ffb90e0005330e02052c0013082c001d3919011d0001392c005f082c001319000e000127005f0e0001330e00010e00020a0e00030a330e00010e0002370e00014c0e0003372b330e00010e00024c2b0e00030a330e00010e0003370e00020e00034c372b330e00010e00020e00034c2b0a330e00010e0002290e00012f200e000246122b330e01011d00010e00012c000b1d00020e00022c00141d00030e00012c00221d00040e00042c002c1d00050e00012c00431d00060e0003082c0011062300004fc0450247000e23000050b1450047002f23000050d2450147003c23000050e2450147003e19010e00060d00401c1d00073c330e00012c000e4300390d00d61c1d00010e0002180d00303524000f0e0205082c00260e000219011d00020e00012c00321d00030e00032f04021d00040e00022c00160e00043124000f0e0001082c003e0e000219011d00020e0002082c001919004a0e0002082c00131900390d00d71c1d00050e0002082c00131900390d00d81c1d00060e00052c00151d00070e00062c00151d00082f001d00090e00090e00031e2400320e00070e000900235c5c5c5c0a0e00070e00091c4a0e00080e00090023363636360a0e00080e00091c4a130009254a14ffc40e00040e00060d00161c0e000527001639082c002f19004a3c33392c00d61d00010e0001082c002f19004a0e0001082c003c392c00d819014a3c33392c00d6082c003c0e000119014a3933392c00d61d00020e0002082c003e0e000119011d00030e0002082c002f19004a0e0002082c003e392c00d7082c00131900082c001a0e0003190119011d00040e0004330e01011d00010e00012c000b1d00020e00022c00141d00030e00022c00211d00040e00012c00431d00050e00052c00641d00060e00052c00401d00070e0003082c0011060e0003082c0011061600802f20034700d90e00064700da2f014700db190147003a23000051b9450147000e23000051cc45024700dc19010e00050d00dd1c1d000823000052fe22030e00012700dd3c33392c003a082c00110e000119013927003a3c33392c003a1d00030e0207082c00090e00032c00da0e000119021d00040e0204082c000919001d00050e0204082c00092f012d000119011d00060e00052c00151d00070e00062c00151d00080e00032c00d91d00090e00032c00db1d000a0e00072c00170e00091e2400b80e0004082c003c0e00021901082c003e0e000619011d000b0e0004082c002f19004a0e000b2c00151d000c0e000c2c00171d000d0e000b1d000e2f011d000f0e000f0e000a1e2400580e0004082c003e0e000e19011d000e0e0004082c002f19004a0e000e2c00151d00102f001d00110e00110e000d1e24001f0e000c0e0011000e00100e0011000a0e000c0e00111c4a130011254a14ffd713000f254a14ff9e0e0005082c001a0e000b19014a0e00082f00254a14ff3b0e00092f04020e00052700160e0005330e0108082c00090e00031901082c00dc0e00010e00021902330e01011d00010e00012c000b1d00020e00022c00141d00030e00022c00211d00040e00012c00431d00050e00052c00611d00060e0003082c0011060e0003082c0011061600802f20034700d90e00064700da2f014700db190147003a23000053a2450147000e23000053b545024700dc19010e00050d00de1c1d0007230000548422030e00012700de3c33392c003a082c00110e000119013927003a3c33392c003a1d00040e00042c00da082c000919001d00050e0204082c000919001d00060e00062c00151d00070e00042c00d91d00080e00042c00db1d00090e00072c00170e00081e2400750e000324000d0e0005082c003c0e000319014a0e0005082c003c0e00011901082c003e0e000219011d00030e0005082c002f19004a2f011d000a0e000a0e00091e2400210e0005082c003e0e000319011d00030e0005082c002f19004a13000a254a14ffd50e0006082c001a0e000319014a14ff7e0e00082f04020e00062700160e0006330e0107082c00090e00031901082c00dc0e00010e00021902330e01011d00020e00022c000b1d00030e00032c00141d00040e00032c00211d00050e00032c00391d00060e00022c00221d00070e00072c002c1d00080e00072c00561d00090e00022c00431d000a0e000a2c00de1d000b0e0006082c0011060e0004082c0011190047003a230000576545024700e1230000577745024700e32300005789450347000e23000057b2450047002f23000057ca45014700e623000057dd450147003e1600802f20034700d91600802f20034700e72f014700e02f024700e24923000057fc2200190047003f19010e00030d00df1c1d000c0e000c082c0011062300005874450047003d2f0147003219010e00030d00eb1c1d000d060e00020d00ec1c1d000e0e0004082c001106230000588b45024700e1230000589c45024700e323000058ad450247000e19010e00030d00f11c1d000f4923000058bd220019000e000e0d00f61c1d0010060e00020d00f71c1d0011062300005a0545024700f72300005a8b45014700f80e00110d00f91c1d00120e000c082c0011060e000c2c003a082c0011060e00104700ec0e00124700fa190147003a2300005ab9450047002f2300005b6045024700362300005b73450047003d1600802f200347003219010e00030d00fe1c1d00130e0004082c0011062300005bd5450147000e2300005be2450147001219010e00030d01001c1d0014060e00020d01011c1d0015062300005bf445014700182300005c4d45014700260e00150d01041c1d00160e0004082c0011060e0004082c0011060e0016470101190147003a2300005cd245044700e82300005d5645044700e92300005d9b450247010719010e00030d01081c1d0017060e00020d01091c1d0018062300005dbd450447010a0e00180d01041c1d00190e0017082c0011060e00172c003a082c0011060e0019470109190147003a2300005e4245044700e82300005eac45044700e919010e00030d010b1c1d001a3c3339082c0009392c00e00e00010e000219033339082c0009392c00e20e00010e0002190333392c003a082c00110e000319013927003a0e0001392700e40e0002392700e539082c002f19004a3c330e02062c002f082c001d3919014a39082c003b19004a3c3339082c00310e000119014a39082c00381900330e000124000b39082c00310e000119014a39082c003d19001d00020e000233230000580e22011d000123000058262201330e0001180d0030352400070e021a331400040e0217333c3306230000583c45034700e8230000585845034700e933490e03010e00021901082c00e80e02010e00010e00020e0003190433490e03010e00021901082c00e90e02010e00010e00020e000319043339082c0038490e05170d00ea190119011d00010e000133392c00ed082c00090e00010e0002190233392c00ee082c00090e00010e00021902330e0001392700ef0e0002392700f03c3323000059ab22031d00020e010f082c001119001d00010e0001082c001106230000590b45024700f419010e00012700ed0e0001082c001106230000595845024700f419010e00012700ee0e000133392c00ef1d00030e00032c00321d00040e0202082c001d390e00010e00020e000419044a0e0003082c00f20e00010e000219024a0e0001082c001e0e00020e00020e00041f1902392700f33c33392c00ef1d00030e00032c00321d00040e0001082c001e0e00020e00020e00041f19021d00050e0003082c00f50e00010e000219024a0e0202082c001d390e00010e00020e000419044a0e0005392700f33c33392c00f01d00050e000524000e0e00051d00043c392700f0140007392c00f31d00042f001d00060e00060e00031e2400270e00010e00020e00061f000e00040e0006000a0e00010e00020e00061f1c4a130006254a14ffcf3c330e00022f04021d00030e00030e00012c00160e00030b461d00040e00042f18290e00042f10292b0e00042f08292b0e00042b1d00052d00001d00062f001d00070e00070e00041e24001b0e0006082c001f0e000519014a0e00072f041f1300071c4a14ffdb0e0205082c00090e00060e000419021d00080e0001082c001a0e000819014a3c330e00012c00150e00012c00162f01462f0212001600ff371d00020e00012c00160e0002460e00010d00161c4a3c330e020c2c002f082c001d3919014a392c003a1d00020e00022c00fb1d00030e00022c00ec1d0004392c00e4392c00e01724000c0e00042c00e11d000114000f0e00042c00e31d00012f0139270034392c00fc21000b392c00fc2c00fd0e00011724001b392c00fc082c000e390e00032100060e00032c001519024a1400270e0001082c001d0e0004390e00032100060e00032c00151903392700fc0e0001392c00fc2700fd3c33392c00fc082c00f40e00010e000219024a3c33392c003a2c00fa1d0002392c00e4392c00e0172400280e0002082c00f7392c002d392c003219024a39082c0038490e05170d00ea190119011d000114002039082c0038490e05170d00ea190119011d00010e0002082c00f80e000119014a0e00013339082c000c0e000119014a3c330e00011a0004392c00ff082c0018391901330e00012c01021d00030e00012c01031d00040e000424002e0e0205082c00092353616c742365645f5f2d00021901082c001a0e00041901082c001a0e000319011d00021400060e00031d00020e0002082c00120e02091901330e0209082c00260e000119011d00030e00032c00151d00040e00042f00002353616c741721000c0e00042f01002365645f5f172400380e0205082c00090e0004082c001e2f022f04190219011d00020e0004082c00372f002f0419024a0e00032c00162f10460e00030d00161c4a0e0214082c0009060e00034701020e0002470103190133392c003a082c00110e000419011d00040e0001082c00e10e00030e000419021d00050e0005082c003e0e000219011d00060e00052c003a1d00070e0214082c0009060e00064701020e00034701050e00072c00fb4700fb0e00014701060e00072c00ec4700ec0e00072c00fa4700fa0e00012c00324700320e00042c01014700ff190133392c003a082c00110e000419011d000439082c01070e00020e00042c010119021d00020e0001082c00e30e00030e00041902082c003e0e00022c010219011d00050e0005330e0001180d0030352400110e0002082c00260e0001391902331400040e0001333c330e00042a2400110e0205082c00202f402f080319011d00040e020b082c0009060e00020e00031f4700d91901082c00dc0e00010e000419021d00050e0205082c00090e00052c0015082c001e0e000219010e00032f040219021d00060e00022f04020e00052700160e0214082c0009060e00054701050e00064700fb0e0004470103190133392c003a082c00110e000419011d00040e00042c0109082c010a0e00030e00012c00d90e00012c00e719031d00050e00052c00fb0e00042700fb0e02172c00e8082c001d390e00010e00020e00052c01050e000419051d00060e0006082c000c0e000519014a0e000633392c003a082c00110e000419011d000439082c01070e00020e00042c010119021d00020e00042c0109082c010a0e00030e00012c00d90e00012c00e70e00022c010319041d00050e00052c00fb0e00042700fb0e02172c00e9082c001d390e00010e00020e00052c01050e000419051d00060e0006332300005ffc22041d00020e01012c000b2c00f1082c001119001d00010e0001082c0011062300005f7645024700f419010e00012700ed0e0001082c0011062300005fb645024700f419010e00012700ee0e000133392c00ef1d00030e00032c00321d00040e0202082c001d390e00010e00020e00040e000319054a0e0001082c001e0e00020e00020e00041f1902392700f33c33392c00ef1d00030e00032c00321d00040e0001082c001e0e00020e00020e00041f19021d00050e0202082c001d390e00010e00020e00040e000319054a0e0005392700f33c33392c00f01d00060e00062400160e0006082c001e2f0019011d00053c392700f0140007392c00f31d00050e0004082c00f20e00052f0019024a2f001d00070e00070e00031e2400270e00010e00020e00071f000e00050e0007000a0e00010e00020e00071f1c4a130007254a14ffcf3c330e01012c000b2c00f1082c001119001d00010e0001082c00110623000060aa45024700f419010e00010d00ed1c1d00020e00020e00012700ee0e000133392c00ef1d00030e00032c00321d0004392c00f01d0005392c010d1d00060e00052400180e0005082c001e2f001901390d010d1c1d00063c392700f00e0006082c001e2f0019011d00070e0003082c00f20e00072f0019024a0e00060e00042f0146002f011f2f002b0e00060e00042f01463a2f001d00080e00080e00041e2400270e00010e00020e00081f000e00070e0008000a0e00010e00020e00081f1c4a130008254a14ffcf3c3323000061a622011d0002230000626422011d00030e01012c000b2c00f1082c001119001d00010e0001082c001106230000629245024700f419010e00010d00ed1c1d00040e00040e00012700ee0e0001330e00012f18071600ff371600ff3524009b0e00012f10071600ff371d00020e00012f08071600ff371d00030e00011600ff371d00040e00021600ff352400362f001d00020e00031600ff3524001f2f001d00030e00041600ff352400082f001d0004140005130004094a140005130003094a140005130002094a2f001d00010e00010e00022f10291f1300011c4a0e00010e00032f08291f1300011c4a0e00010e00041f1300011c4a14000e0e00012f012f18291f1300011c4a0e000133490e01020e00012f000019010e00012f001c2f0035240012490e01020e00012f010019010e00012f013a0e000133392c00ef1d00030e00032c00321d0004392c00f01d0005392c010d1d00060e00052400180e0005082c001e2f001901390d010d1c1d00063c392700f0490e02030e000619014a0e0006082c001e2f0019011d00070e0003082c00f20e00072f0019024a2f001d00080e00080e00041e2400270e00010e00020e00081f000e00070e0008000a0e00010e00020e00081f1c4a130008254a14ffcf3c330e01012c000b2c00f1082c001119001d00010e0001082c001106230000636a45024700f419010e00010d00ed1c1d00020e00020e00012700ee0e000133392c00ef1d00030e00032c00321d0004392c00f01d0005392c01101d00060e00052400180e0005082c001e2f001901390d01101c1d00063c392700f00e0003082c00f20e00062f0019024a2f001d00070e00070e00041e2400270e00010e00020e00071f000e00060e0007000a0e00010e00020e00071f1c4a130007254a14ffcf3c330e01012c000b2c00f1082c001119001d00010e0001082c001106230000643745024700f419010e00012700ed0e0001082c001106230000644a45024700f419010e00012700ee0e000133392c00ef082c00f20e00010e000219024a3c33392c00ef082c00f50e00010e000219024a3c330e00012c00161d00030e00022f04021d00040e00040e00030e00040b461d00050e00030e00051f2f01461d00060e0001082c001919004a0e00012c00150e00062f0212000e00052f180e00062f040b2f080246292b0e00012c00150e00062f02121c4a0e00012c00160e00051f0e00010d00161c4a3c330e00012c00150e00012c00162f01462f0212001600ff371d00020e00012c00160e0002460e00010d00161c4a3c330e00022f04021d00030e00030e00012c00160e00030b461d00040e0001082c001a0e02012c000b2c0021082c00200e00042f014619011901082c001a0e02012c000b2c0021082c00090e00042f18292d00012f01190219014a3c330e00012c00150e00012c00162f01462f0212001600ff371d00020e00012c00160e0002460e00010d00161c4a3c330e0001082c001a0e02012c000b2c0021082c00094201152d00012f01190219014a0e02012c00f72c0116082c00f70e00010e000219024a3c330e02012c00f72c0116082c00f80e000119014a0e00010d0016444a3c330e00022f04021d00030e0001082c001919004a0e00012c00160e00030e00012c00160e00030b1a00030e0003461f0e00010d00161c4a3c330e00012c00151d00020e00012c00162f01461d00030e00012c00162f01461d00030e00032f00412400350e00020e00032f0212002f180e00032f040b2f080246121600ff3724000f0e00032f011f0e0001270016140008130003444a14ffc23c333c333c330e01011d00020e00022c000b1d00030e00032c01001d00040e00022c00221d00050e00052c00271d00060e00022c01011d00070623000066d2450147001823000066e245014700260e00070d00271c1d00083c330e00012c0102082c00120e02061901330e0206082c00260e000119011d00020e0204082c0009060e00024701021901330e01011d00010e00012c000b1d00020e00022c00fe1d00030e00012c00431d00042d00001d00052d00001d00062d00001d00072d00001d00082d00001d00092d00001d000a2d00001d000b2d00001d000c2d00001d000d2d00001d000e4923000067e0220019004a2f002f012f022f042f082f102f202f401600802f1b2f362d000b1d000f0e0003082c00110623000069c0450047003b2300006bf945024700f22300006c1c45024700f52300006c9b450847011d1601002f20034700d919010e00040d011e1c1d00100e0003082c003f0e001019010e000127011e3c332d00001d00012f001d00020e00021601001e2400330e00021600801e2400100e00022f01290e00010e00023a1400110e00022f012916011b0a0e00010e00023a130002254a14ffc32f001d00032f001d00042f001d00020e00021601001e24017d0e00040e00042f01290a0e00042f02290a0e00042f03290a0e00042f04290a1d00050e00052f08120e00051600ff370a2f630a1d00050e00050e01050e00033a0e00030e01060e00053a0e00010e0003001d00060e00010e0006001d00070e00010e0007001d00080e00010e000500160101020e00052301010100020a1d00090e00092f18290e00092f08122b0e01070e00033a0e00092f10290e00092f10122b0e01080e00033a0e00092f08290e00092f18122b0e01090e00033a0e00090e010a0e00033a0e00082301010101020e00072300010001020a0e0006160101020a0e00032301010100020a1d00090e00092f18290e00092f08122b0e010b0e00053a0e00092f10290e00092f10122b0e010c0e00053a0e00092f08290e00092f18122b0e010d0e00053a0e00090e010e0e00053a0e00032a24000c2f011300041c1d000314002e0e00060e00010e00010e00010e00080e00060a0000000a1d00030e00040e00010e00010e000400000a1300041c4a130002254a14fe793c33392c0119210009392c011a392c00e5352400023c33392c00e5390d011a1c1d00020e00022c00151d00030e00022c00162f04031d00040e00042f061f390d01191c1d00050e00052f011f2f04021d00062d0000390d011b1c1d00072f001d00080e00080e00061e2401140e00080e00041e2400110e00030e0008000e00070e00083a1400f10e00070e00082f0146001d00010e00080e00040b2a24006d0e00012f08290e00012f18122b1d00010e02050e00012f1812002f18290e02050e00012f10121600ff37002f10292b0e02050e00012f08121600ff37002f08292b0e02050e00011600ff37002b1d00010e00010e020f0e00080e0004032f002b002f18290a1300011c4a1400560e00042f063121000a0e00080e00040b2f04172400400e02050e00012f1812002f18290e02050e00012f10121600ff37002f10292b0e02050e00012f08121600ff37002f08292b0e02050e00011600ff37002b1d00010e00070e00080e000446000e00010a0e00070e00083a130008254a14fee22d0000390d011c1c1d00092f001d000a0e000a0e00061e24009f0e00060e000a461d00080e000a2f040b24000d0e00070e0008001d000114000d0e00070e00082f0446001d00010e000a2f041e1a00060e00082f041524000d0e00010e00090e000a3a14004b0e020b0e02050e00012f181200000e020c0e02050e00012f10121600ff3700000a0e020d0e02050e00012f08121600ff3700000a0e020e0e02050e00011600ff3700000a0e00090e000a3a13000a254a14ff573c3339082c011d0e00010e0002392c011b0e02070e02080e02090e020a0e020519084a3c330e00010e00022f011f001d00030e00010e00022f031f000e00010e00022f011f3a0e00030e00010e00022f031f3a39082c011d0e00010e0002392c011c0e020b0e020c0e020d0e020e0e020619084a0e00010e00022f011f001d00030e00010e00022f031f000e00010e00022f011f3a0e00030e00010e00022f031f3a3c33392c01191d00090e00010e0002000e00032f00000a1d000a0e00010e00022f011f000e00032f01000a1d000b0e00010e00022f021f000e00032f02000a1d000c0e00010e00022f031f000e00032f03000a1d000d2f041d000e2f011d000f0e000f0e00091e2401200e00040e000a2f1812000e00050e000b2f10121600ff37000a0e00060e000c2f08121600ff37000a0e00070e000d1600ff37000a0e000313000e25000a1d00100e00040e000b2f1812000e00050e000c2f10121600ff37000a0e00060e000d2f08121600ff37000a0e00070e000a1600ff37000a0e000313000e25000a1d00110e00040e000c2f1812000e00050e000d2f10121600ff37000a0e00060e000a2f08121600ff37000a0e00070e000b1600ff37000a0e000313000e25000a1d00120e00040e000d2f1812000e00050e000a2f10121600ff37000a0e00060e000b2f08121600ff37000a0e00070e000c1600ff37000a0e000313000e25000a1d00130e00101d000a0e00111d000b0e00121d000c0e00131d000d13000f254a14fed60e00080e000a2f1812002f18290e00080e000b2f10121600ff37002f10292b0e00080e000c2f08121600ff37002f08292b0e00080e000d1600ff37002b0e000313000e25000a1d00100e00080e000b2f1812002f18290e00080e000c2f10121600ff37002f10292b0e00080e000d2f08121600ff37002f08292b0e00080e000a1600ff37002b0e000313000e25000a1d00110e00080e000c2f1812002f18290e00080e000d2f10121600ff37002f10292b0e00080e000a2f08121600ff37002f08292b0e00080e000b1600ff37002b0e000313000e25000a1d00120e00080e000d2f1812002f18290e00080e000a2f10121600ff37002f10292b0e00080e000b2f08121600ff37002f08292b0e00080e000c1600ff37002b0e000313000e25000a1d00130e00100e00010e00023a0e00110e00010e00022f011f3a0e00120e00010e00022f021f3a0e00130e00010e00022f031f3a3c3323000083ad22021d000c23000083e322021d000d0e01011d00010e00012c000b1d00020e00022c00211d00030e00022c00fe1d00040e00012c00431d00052f392f312f292f212f192f112f092f012f3a2f322f2a2f222f1a2f122f0a2f022f3b2f332f2b2f232f1b2f132f0b2f032f3c2f342f2c2f242f3f2f372f2f2f272f1f2f172f0f2f072f3e2f362f2e2f262f1e2f162f0e2f062f3d2f352f2d2f252f1d2f152f0d2f052f1c2f142f0c2f042d00381d00062f0e2f112f0b2f182f012f052f032f1c2f0f2f062f152f0a2f172f132f0c2f042f1a2f082f102f072f1b2f142f0d2f022f292f342f1f2f252f2f2f372f1e2f282f332f2d2f212f302f2c2f312f272f382f222f352f2e2f2a2f322f242f1d2f202d00301d00072f012f022f042f062f082f0a2f0c2f0e2f0f2f112f132f152f172f192f1b2f1c2d00101d000806230080820047011f230000800047012023008080024701212f02470122160200470123230080820247012423008002024701252300800000470126160202470115230080020047012723000082004701282300808000470129230000800247012a230080000247012b2f0047012c230000820247012d2f0047012e230080820247012f23000082024701302300008000470131230080820047013216020047013323008080024701342f024701352300800200470136230000820047013723008080004701382300800202470139230080000247013a230000800247013b16020247013c230080000047013d230000800047013e2f0247013f23008082004701402300800000470141230080800247014223000082004701431602004701442300800202470145230080820247014623008080004701472300800002470148230000820247014916020247014a230080020047014b230000800247014c2f0047014d230080820247014e230080800047014f2300800000470150160200470151230000800047015223008000024701532f024701542300008202470155230000800247015623008002024701571602024701582300808200470159230080020047015a2f0047015b230000820047015c230080800247015d06234008401047011f16400047015e230008000047015f23400800104701602340000010470161234008400047016223400040004701632f10470164230008400047012e23400040104701652340000000470166230008401047016723000800104701682f0047016916401047016a234008000047016b234000400047016c230008401047016d2f1047016e234000401047016f234008401047017023400000004701712300080000470172234008001047017323000800104701742f00470175164000470176234008000047017723400000104701782300084000470179234008400047017a16401047017b2f00470120234008001047017c234000401047017d234008400047017e234008000047017f2f10470180230008401047018116400047018216401047012f2300080000470183230008001047018423400000104701852300084000470186234000400047018723400000004701882340084010470189230008401047018a230008000047018b234008000047018c16400047018d234000400047018e234008401047018f2f10470190234000000047019123400840004701922340000010470193234000401047019423000800104701952f00470196164010470197234008001047019823000840004701990616010447011f2f0047019a230400010047019b230001010447019c230001000447019d230400000447019e230401010447019f23040100004701a0230400000047016c23040101004701a123000101004701a223040100044701a323040001044701a423000100004701a52f044701a61601004701a723040101004701a823040100044701a92f004701aa23040001004701ab23040000044701ac23000100004701ad23000100044701ae1601044701af2f044701b01601004701b123040100004701b223000101044701b323000101004701b423040001044701b523040101044701b623040000004701b7230401010047015e23000100044701b823000100004701b923040001004701ba1601004701bb23040101044701bc23040000044701bd2f004701be230400010447016d23040000004701bf2f044701c023000101004701c123040100004701c21601044701c323000101044701c423040100044701c523040000004701c61601044701c723040101004701c82f004701c923000100044701ca23040001004701cb1601004701cc23040100044701cd23000100004701ce23040101044701cf23000101044701d023040000044701d123040001044701d223040100004701d32f044701d423000101004701d5064201d647011f4201d74701d823004010404701d94201da4701db2f004701dc23004010004701dd4201de4701df23004000404701e04201154701a823004000004701e12f404701e24201e34701e44201e54701e61610404701e71610004701e84201e94701ea4201d74701eb2f404701ec4201e54701ed4201e34701ee23004010004701ef4201e94701f02f004701f14201da4701f21610004701f34201d64701f423004000004701f51610404701f64201154701f723004000404701f823004010404701f94201de4701fa230040004047019a23004010004701fb4201de4701fc2f004701fd1610404701fe4201e54701ff4201d64702004201d74702014201e94701a94201154702024201da47020323004010404702044201e347020523004000004702062f404702071610004702084201da4702094201e947020a2f0047020b230040100047020c230040004047020d42011547020e4201d747020f2f404702104201de4702111610004702124201e34702134201e54702141610404702154201d6470216230040000047021723004010404702180616008047011f2301040000470219230004000047021a232000000047021b232004008047021c230100008047021d232100008047021e230004008047021f23010000004701eb23200400004702202320000080470221232104008047022223210400004702232f004702242301040080470225232100000047022623010400804702272321000080470228160080470229230104000047022a230004000047022b232004008047022c232104000047022d232000000047022e232004000047022f2f0047023023210400804702312301000080470232232000008047023323210000004702342301000000470235230004008047023623000400004701d816008047023723200000004702382321000080470239230100008047023a232104000047023b232004008047023c230100000047023d23210400804701ec232100000047023e230104000047023f2320040000470240230004008047024123200000804702422f00470243230104008047024423210000804702452301000000470246230104000047024723200400804702482320000000470249230104008047024a16008047024b232104000047024c230004008047024d232104008047024e2f0047024f2321000000470250230100008047025123000400004702522320040000470253232000008047025406231000000847011f1620004702552310200000470256231020200847025723100020004702582300200000470259230020000847025a231000000047025b2f00470227231000200847025c230020200047025d2f0847025e231020000847025f23002020084702601620084702612310202000470262231020000047026323102020084702642f08470265230020000047026623002020084702672310000008470268231000200047026916200847026a230020000847026b16200047026c231000200847026d231020000847026e2f0047026f231020200047027023002020004702712310000000470272231000200047021923102000084702732310202008470274162008470275230020000047027623100000004702772310000008470278230020200047027923002020084702282f0047027a2f0847027b231020000047027c16200047027d231000200847027e231020200047027f23002000084702802f084702812300202000470282230020000047028323100000084702842310002000470285162008470286231020200847028723102000004702882310202000470289231020000847028a16200047028b230020200847028c230020000847028d2f0047028e231000000047028f231000200847029006230010000047011f2302000401470291160400470292230010040147029323021004014702942f004702952f014702962302100001470297230200040047026323001000014702982302000001470299230210040047029a230210000047029b16040147029c230010040047029d230200000047029e230210000147029f2f004702a023020004014702a123021004004702a223001000004702a323020000014702a423020000004702a51604014702a623001004014702a723020004004702a823021000004702a923001000014702aa1604004702ab23021004014702ac2f014702ad23001004004702ae230200000047025523001000004702af23020004014702b023021000014702b123001000014702b223020004004702b323021004004702b423001004014702b516040147026423021004014702b623001004004702b72f014702b82f004702b923021000004702ba23020000014702bb1604004702bc23001004004702bd23020004014702be23021000014702bf2f014702c023020000004702c123001000004702c21604014702c323021004004702c423020000014702c523021000004702c62f004702c723021004014702c823001004014702c91604004702ca23020004004702cb23001000014702cc06230800082047011f230002000047013e23080000004702cd2f204702ce23000200204702cf23080208204702d023080208004702d11608004702d2230802000047029f23080008004702d323000208004702d423080200204702d51608204702d62f004702d723080000204702d823000208204702d9160800470115230802082047014623080008204702da23080000004702db23080200004702dc23000208004702dd23000208204702de2f204702df23080000204702e01608204702e123000200204702e223080208004702e32f004702e423080200204702e523080008004702e623000200004702e7230002082047029123080208004702e82f204702e91608004702ea23080008004702eb23080000204702ec23080200204702ed23000200004702ee2f004702a023000200204702ef23080200004702f023080008204702f123080208204702f223000208004702f31608204702f423080000004702f523000200004702f61608004702f723080200204702f823000208204702f92f204702fa23080200004702fb23080000004702fc23080008204702fd23080208204702fe23080000204702ff23080008004703002f004703012300020800470302160820470303230002002047030423080208004703052d00081d000942015d231f8000002301f8000023001f8000230001f800161f801601f84203052d00081d000a0e0004082c0011062300008047450047003b230000820545024700f2230000821945024700f5230000822d450347011d2f402f20034700d92f402f20034700e72f402f200347003219010e00050d030a1c1d000b0e0004082c003f0e000b19010e000127030a0e0004082c0011062300008419450047003b230000850b45024700f2230000854045024700f51600c02f20034700d92f402f20034700e72f402f200347003219010e00050d030f1c1d000e0e0004082c003f0e000e19010e000127030f3c33392c00e51d00010e00012c00151d00022d00001d00032f001d00040e00042f381e2400330e02060e0004002f01461d00050e00020e00052f0512002f1f0e00052f200b46122f01370e00030e00043a130004254a14ffc42d0000390d03061c1d00062f001d00070e00072f101e24011a2d00000e00060e00071c1d00080e02080e0007001d00092f001d00040e00042f181e24008a0e00080e00042f06032f002b000e00030e02070e0004002f01460e00091f2f1c0b002f1f0e00042f060b46292b0e00080e00042f06032f002b1c4a0e00082f040e00042f06032f002b1f000e00032f1c0e02070e00042f181f002f01460e00091f2f1c0b1f002f1f0e00042f060b46292b0e00082f040e00042f06032f002b1f1c4a130004254a14ff6d0e00082f00002f01290e00082f00002f1f122b0e00082f003a2f011d00040e00042f071e2400230e00080e0004000e00042f01462f04022f031f120e00080e00043a130004254a14ffd40e00082f07002f05290e00082f07002f1b122b0e00082f073a130007254a14fedd2d0000390d03071c1d000a2f001d00040e00042f101e2400190e00062f0f0e000446000e000a0e00043a130004254a14ffde3c3339082c011d0e00010e0002392c030619034a3c3339082c011d0e00010e0002392c030719034a3c330e00010e000200392703080e00010e00022f011f00392703090e020c082c001d392f04230f0f0f0f19034a0e020c082c001d392f10230000ffff19034a0e020d082c001d392f02233333333319034a0e020d082c001d392f082300ff00ff19034a0e020c082c001d392f01235555555519034a2f001d00040e00042f101e2400740e00030e0004001d0005392c03081d0006392c03091d00072f001d00082f001d00090e00092f081e24002f0e00080e02090e0009000e00070e00050e0009000a0e020a0e000900372f0012002b1300081c4a130009254a14ffc80e0007392703080e00060e00080a39270309130004254a14ff83392c03081d000a392c0309392703080e000a392703090e020c082c001d392f01235555555519034a0e020d082c001d392f082300ff00ff19034a0e020d082c001d392f02233333333319034a0e020c082c001d392f10230000ffff19034a0e020c082c001d392f04230f0f0f0f19034a392c03080e00010e00023a392c03090e00010e00022f011f3a3c33392c03080e000112392c03090a0e0002371d0003392c03090e00030a390d03091c4a392c03080e00030e0001290a390d03081c4a3c33392c03090e000112392c03080a0e0002371d0003392c03080e00030a390d03081c4a392c03090e00030e0001290a390d03091c4a3c33392c00e51d00010e00012c00151d00020e00022c00172f02362100090e00022c00172f04362100090e00022c00172f061e2400090e05040d030b4301300e0002082c001e2f002f0219021d00030e00022c00172f041e2400100e0002082c001e2f002f02190214000d0e0002082c001e2f022f0419021d00040e00022c00172f061e2400100e0002082c001e2f002f02190214000d0e0002082c001e2f042f0619021d00050e020b082c00e10e0203082c00090e0003190119013927030c0e020b082c00e10e0203082c00090e0004190119013927030d0e020b082c00e10e0203082c00090e0005190119013927030e3c33392c030c082c00f20e00010e000219024a392c030d082c00f50e00010e000219024a392c030e082c00f20e00010e000219024a3c33392c030e082c00f50e00010e000219024a392c030d082c00f20e00010e000219024a392c030c082c00f50e00010e000219024a3c33230000871a22001d00060e01011d00010e00012c000b1d00020e00022c00eb1d00030e00012c00431d00040e0003082c0011062300008630450047003b23000086fe45024700361601002f20034700d92f004700e719010e00040d03131c1d00050e0003082c003f0e000519010e00012703130e0005082c0011060e00052c003a082c0011061600c0470314190147003a23000087c7450047003b19010e00040d03151c1d00070e0003082c003f0e000719010e00012703153c33392c00e51d00010e00012c00151d00020e00012c00161d00032d0000390d03101c1d00042f001d00050e00051601001e2400120e00050e00040e00053a130005254a14ffe42f001d00052f001d00060e00051601001e2400680e00050e00030b1d00070e00020e00072f0212002f180e00072f040b2f080246121600ff371d00080e00060e00040e0005001f0e00081f1601000b1d00060e00040e0005001d00090e00040e0006000e00040e00053a0e00090e00040e00063a130005254a14ff8e2f00390d03111c392703123c330e00010e0002000e0206082c001d3919010a0e00010e00021c4a3c33392c03101d0001392c03121d0002392c03111d00032f001d00042f001d00050e00052f041e2400730e00022f011f1601000b1d00020e00030e00010e0002001f1601000b1d00030e00010e0002001d00060e00010e0003000e00010e00023a0e00060e00010e00033a0e00040e00010e00010e0002000e00010e0003001f1601000b002f180e00052f080246292b1300041c4a130005254a14ff840e0002392703120e0003392703110e0004330e02052c003b082c001d3919014a392c003a2c03141d00010e00012f00312400130e0206082c001d3919014a130001444a14ffe43c332300008cae22001d00090e01011d00010e00012c000b1d00020e00022c00eb1d00030e00012c00431d00042d00001d00052d00001d00062d00001d00070e0003082c0011062300008887450047003b2300008ba945024700361600802f20034700322f402f20034700e719010e00040d031a1c1d00080e0003082c003f0e000819010e000127031a3c33392c00e52c00151d0001392c003a2c00fb1d00022f001d00030e00032f041e2400440e00010e0003002f08290e00010e0003002f18122b2300ff00ff370e00010e0003002f18290e00010e0003002f08122b42004f372b0e00010e00033a130003254a14ffb30e00012f00000e00012f03002f10290e00012f02002f10122b0e00012f01000e00012f00002f10290e00012f03002f10122b0e00012f02000e00012f01002f10290e00012f00002f10122b0e00012f03000e00012f02002f10290e00012f01002f10122b2d0008390d03161c1d00040e00012f02002f10290e00012f02002f10122b0e00012f0000420317370e00012f0100230000ffff372b0e00012f03002f10290e00012f03002f10122b0e00012f0100420317370e00012f0200230000ffff372b0e00012f00002f10290e00012f00002f10122b0e00012f0200420317370e00012f0300230000ffff372b0e00012f01002f10290e00012f01002f10122b0e00012f0300420317370e00012f0000230000ffff372b2d0008390d03181c1d00052f00392703192f001d00030e00032f041e2400130e0209082c001d3919014a130003254a14ffe42f001d00030e00032f081e2400250e00050e0003000e00040e00032f041f2f0737000a0e00050e00031c4a130003254a14ffd20e00022401380e00022c00151d00060e00062f00001d00070e00062f01001d00080e00072f08290e00072f18122b2300ff00ff370e00072f18290e00072f08122b42004f372b1d00090e00082f08290e00082f18122b2300ff00ff370e00082f18290e00082f08122b42004f372b1d000a0e00092f10120e000a420317372b1d000b0e000a2f10290e0009230000ffff372b1d000c0e00052f00000e00090a0e00052f001c4a0e00052f01000e000b0a0e00052f011c4a0e00052f02000e000a0a0e00052f021c4a0e00052f03000e000c0a0e00052f031c4a0e00052f04000e00090a0e00052f041c4a0e00052f05000e000b0a0e00052f051c4a0e00052f06000e000a0a0e00052f061c4a0e00052f07000e000c0a0e00052f071c4a2f001d00030e00032f041e2400130e0209082c001d3919014a130003254a14ffe43c33392c03161d00030e0209082c001d3919014a0e00032f00000e00032f05002f10120a0e00032f03002f10290a0e02052f003a0e00032f02000e00032f07002f10120a0e00032f05002f10290a0e02052f013a0e00032f04000e00032f01002f10120a0e00032f07002f10290a0e02052f023a0e00032f06000e00032f03002f10120a0e00032f01002f10290a0e02052f033a2f001d00040e00042f041e2400630e02050e0004002f08290e02050e0004002f18122b2300ff00ff370e02050e0004002f18290e02050e0004002f08122b42004f372b0e02050e00043a0e00010e00020e00041f000e02050e0004000a0e00010e00020e00041f1c4a130004254a14ff943c33392c03161d0001392c03181d00022f001d00030e00032f081e2400160e00020e0003000e01060e00033a130003254a14ffe10e00022f0000234d34d34d1f392c03191f2f002b0e00022f003a0e00022f010042031b1f0e00022f00002f00120e01062f00002f00121e2400052f011400022f001f2f002b0e00022f013a0e00022f02002334d34d341f0e00022f01002f00120e01062f01002f00121e2400052f011400022f001f2f002b0e00022f023a0e00022f0300234d34d34d1f0e00022f02002f00120e01062f02002f00121e2400052f011400022f001f2f002b0e00022f033a0e00022f040042031b1f0e00022f03002f00120e01062f03002f00121e2400052f011400022f001f2f002b0e00022f043a0e00022f05002334d34d341f0e00022f04002f00120e01062f04002f00121e2400052f011400022f001f2f002b0e00022f053a0e00022f0600234d34d34d1f0e00022f05002f00120e01062f05002f00121e2400052f011400022f001f2f002b0e00022f063a0e00022f070042031b1f0e00022f06002f00120e01062f06002f00121e2400052f011400022f001f2f002b0e00022f073a0e00022f07002f00120e01062f07002f00121e2400052f011400022f00392703192f001d00030e00032f081e24007f0e00010e0003000e00020e0003001f1d00040e0004230000ffff371d00050e00042f10121d00060e00050e0005022f11120e00050e0006021f2f0f120e00060e0006021f1d00070e0004420317370e0004022f002b0e0004230000ffff370e0004022f002b1f1d00080e00070e00080a0e01070e00033a130003254a14ff780e01072f00000e01072f07002f10290e01072f07002f10122b1f0e01072f06002f10290e01072f06002f10122b1f2f002b0e00012f003a0e01072f01000e01072f00002f08290e01072f00002f18122b1f0e01072f07001f2f002b0e00012f013a0e01072f02000e01072f01002f10290e01072f01002f10122b1f0e01072f00002f10290e01072f00002f10122b1f2f002b0e00012f023a0e01072f03000e01072f02002f08290e01072f02002f18122b1f0e01072f01001f2f002b0e00012f033a0e01072f04000e01072f03002f10290e01072f03002f10122b1f0e01072f02002f10290e01072f02002f10122b1f2f002b0e00012f043a0e01072f05000e01072f04002f08290e01072f04002f18122b1f0e01072f03001f2f002b0e00012f053a0e01072f06000e01072f05002f10290e01072f05002f10122b1f0e01072f04002f10290e01072f04002f10122b1f2f002b0e00012f063a0e01072f07000e01072f06002f08290e01072f06002f18122b1f0e01072f05001f2f002b0e00012f073a3c3323000094ec22001d00090e01011d00010e00012c000b1d00020e00022c00eb1d00030e00012c00431d00042d00001d00052d00001d00062d00001d00070e0003082c0011062300009117450047003b23000093e745024700361600802f20034700322f402f20034700e719010e00040d031c1c1d00080e0003082c003f0e000819010e000127031c3c33392c00e52c00151d0001392c003a2c00fb1d00020e00012f00000e00012f03002f10290e00012f02002f10122b0e00012f01000e00012f00002f10290e00012f03002f10122b0e00012f02000e00012f01002f10290e00012f00002f10122b0e00012f03000e00012f02002f10290e00012f01002f10122b2d0008390d03161c1d00030e00012f02002f10290e00012f02002f10122b0e00012f0000420317370e00012f0100230000ffff372b0e00012f03002f10290e00012f03002f10122b0e00012f0100420317370e00012f0200230000ffff372b0e00012f00002f10290e00012f00002f10122b0e00012f0200420317370e00012f0300230000ffff372b0e00012f01002f10290e00012f01002f10122b0e00012f0300420317370e00012f0000230000ffff372b2d0008390d03181c1d00042f00392703192f001d00050e00052f041e2400130e0209082c001d3919014a130005254a14ffe42f001d00050e00052f081e2400250e00040e0005000e00030e00052f041f2f0737000a0e00040e00051c4a130005254a14ffd20e00022401380e00022c00151d00060e00062f00001d00070e00062f01001d00080e00072f08290e00072f18122b2300ff00ff370e00072f18290e00072f08122b42004f372b1d00090e00082f08290e00082f18122b2300ff00ff370e00082f18290e00082f08122b42004f372b1d000a0e00092f10120e000a420317372b1d000b0e000a2f10290e0009230000ffff372b1d000c0e00042f00000e00090a0e00042f001c4a0e00042f01000e000b0a0e00042f011c4a0e00042f02000e000a0a0e00042f021c4a0e00042f03000e000c0a0e00042f031c4a0e00042f04000e00090a0e00042f041c4a0e00042f05000e000b0a0e00042f051c4a0e00042f06000e000a0a0e00042f061c4a0e00042f07000e000c0a0e00042f071c4a2f001d00050e00052f041e2400130e0209082c001d3919014a130005254a14ffe43c33392c03161d00030e0209082c001d3919014a0e00032f00000e00032f05002f10120a0e00032f03002f10290a0e02052f003a0e00032f02000e00032f07002f10120a0e00032f05002f10290a0e02052f013a0e00032f04000e00032f01002f10120a0e00032f07002f10290a0e02052f023a0e00032f06000e00032f03002f10120a0e00032f01002f10290a0e02052f033a2f001d00040e00042f041e2400630e02050e0004002f08290e02050e0004002f18122b2300ff00ff370e02050e0004002f18290e02050e0004002f08122b42004f372b0e02050e00043a0e00010e00020e00041f000e02050e0004000a0e00010e00020e00041f1c4a130004254a14ff943c33392c03161d0001392c03181d00022f001d00030e00032f081e2400160e00020e0003000e01060e00033a130003254a14ffe10e00022f0000234d34d34d1f392c03191f2f002b0e00022f003a0e00022f010042031b1f0e00022f00002f00120e01062f00002f00121e2400052f011400022f001f2f002b0e00022f013a0e00022f02002334d34d341f0e00022f01002f00120e01062f01002f00121e2400052f011400022f001f2f002b0e00022f023a0e00022f0300234d34d34d1f0e00022f02002f00120e01062f02002f00121e2400052f011400022f001f2f002b0e00022f033a0e00022f040042031b1f0e00022f03002f00120e01062f03002f00121e2400052f011400022f001f2f002b0e00022f043a0e00022f05002334d34d341f0e00022f04002f00120e01062f04002f00121e2400052f011400022f001f2f002b0e00022f053a0e00022f0600234d34d34d1f0e00022f05002f00120e01062f05002f00121e2400052f011400022f001f2f002b0e00022f063a0e00022f070042031b1f0e00022f06002f00120e01062f06002f00121e2400052f011400022f001f2f002b0e00022f073a0e00022f07002f00120e01062f07002f00121e2400052f011400022f00392703192f001d00030e00032f081e24007f0e00010e0003000e00020e0003001f1d00040e0004230000ffff371d00050e00042f10121d00060e00050e0005022f11120e00050e0006021f2f0f120e00060e0006021f1d00070e0004420317370e0004022f002b0e0004230000ffff370e0004022f002b1f1d00080e00070e00080a0e01070e00033a130003254a14ff780e01072f00000e01072f07002f10290e01072f07002f10122b1f0e01072f06002f10290e01072f06002f10122b1f2f002b0e00012f003a0e01072f01000e01072f00002f08290e01072f00002f18122b1f0e01072f07001f2f002b0e00012f013a0e01072f02000e01072f01002f10290e01072f01002f10122b1f0e01072f00002f10290e01072f00002f10122b1f2f002b0e00012f023a0e01072f03000e01072f02002f08290e01072f02002f18122b1f0e01072f01001f2f002b0e00012f033a0e01072f04000e01072f03002f10290e01072f03002f10122b1f0e01072f02002f10290e01072f02002f10122b1f2f002b0e00012f043a0e01072f05000e01072f04002f08290e01072f04002f18122b1f0e01072f03001f2f002b0e00012f053a0e01072f06000e01072f05002f10290e01072f05002f10122b1f0e01072f04002f10290e01072f04002f10122b1f2f002b0e00012f063a0e01072f07000e01072f06002f08290e01072f06002f18122b1f0e01072f05001f2f002b0e00012f073a3c330e00012c00151d00020e00012c00161d00030e030e0e000343011d00042f001d00050e00050e00031e2400300e00020e00052f0212002f180e00052f040b2f080246121600ff371d00060e00060e00040e00053a130005254a14ffc60e0004330e00012c00171d00022d00001d00032f001d00040e00040e00021e2400360e00030e00042f0212000e00010e0004001600ff372f180e00042f040b2f080246292b0e00030e00042f02121c4a130004254a14ffc00e03002c00002c000b2c0021082c00090e00030e00021902330e00012c00161d00020e00012c00151d00030e020e0e000243011d00042f001d00052f001d00063424008b0e00050e00023524000314007e0e000313000625001d00070e000742031e372f18120e0004130005253a0e00050e0002352400031400540e00072300ff0000372f10120e0004130005253a0e00050e0002352400031400330e0007230000ff00372f08120e0004130005253a0e00050e0002352400031400120e00071600ff370e0004130005253a14ff710e0004330e03002c0000082c00c60e000119011d0002490e02100e00021901330e00002c00172f02312100080e00002f02003c362400090e00002f02001400022f001d00030e00002c00172f03312100080e00002f03003c362400090e00002f03001400022f001d00040e00041d00050e00031d00060e00050e00012c00171e21000a0e00060e00022c00171e24001b0e00020e0006000e00010e00053a130005254a130006254a14ffcb3c330e00002c00172f00312100080e00002f00003c362400090e00002f00001400022f101d00010e030e0e000143011d00020e0002082c031f2f0019014a0e000233490e02130e00012c00170e00022c00171f19011d0003490e02120e00030e000119024a490e02120e00030e00022f000e00012c001719044a0e0003330e02030e02040e02050e02060e02070e02082d00061d00010e030e0e000143011d00020e0002330e030e0e020143011d00012f001d00020e00020e00012c00171e24002b490e03060d0024082c001a0e030c082c002019001600ff02190119010e00010e00023a130002254a14ffc80e0001330e00011d00022f001d00030e00030e02091e24004b490e02130e00022c00172f011f19011d0004490e02120e00040e00022f0019034a0e020d0e0003000e020e0e0003000a0e00040e00042c00172f01463a0e00041d0002130003254a14ffab0e000233490e02110e020f082c00260e0001190119011d0002490e02170e000219011d0003490e02110e020f082c00260e0003190119011d0004490e021319001d0005490e021319001d0006490e02120e00050e000419024a490e02120e00060e00042f1019034a0e020f082c00260e000519011d00070e020f082c00260e000619011d0008060e00074701050e00084700fb332d00001d00020e00012c00171d00032f001d00040e00040e00031e2401390e0001082c00290e000419011d00050e00052300010000412100090e0005230010ffff1524005c0e0002082c001f0e00052f12072f07371600f02b19014a0e0002082c001f0e00052f0c072f3f371600802b19014a0e0002082c001f0e00052f06072f3f371600802b19014a0e0002082c001f0e00052f3f371600802b19014a1400ae0e0005160800412100090e0005230000ffff152400450e0002082c001f0e00052f0c072f0f371600e02b19014a0e0002082c001f0e00052f06072f3f371600802b19014a0e0002082c001f0e00052f3f371600802b19014a1400530e0005160080412100070e00051607ff1524002e0e0002082c001f0e00052f06072f1f371600c02b19014a0e0002082c001f0e00052f3f371600802b19014a1400110e0002082c001f0e00051600ff3719014a130004254a14febd0e0002332d00001d00022f001d00030e00030e00012c00171e2401030e0001082c00290e000319011d00040e00041600801e2400100e0002082c001f0e000419014a1400d20e00041608001e2400210e0002082c001f1600c00e00042f06072b1600800e00042f3f372b19024a1400a70e0004230000d8001e1a00090e0004230000e0004124002e0e0002082c001f1600e00e00042f0c072b1600800e00042f06072f3f372b1600800e00042f3f372b19034a140061130003254a23000100000e00041603ff372f0a290e0001082c00290e000319011603ff372b1f1d00040e0002082c001f1600f00e00042f12072b1600800e00042f0c072f3f372b1600800e00042f06072f3f372b1600800e00042f3f372b19044a130003254a14fef00e0002332f001d00030e00030e00012c00171e2400120e00020e00010e00033a130003254a14ffe13c330e00002c00172f01312100080e00002f01003c362400090e00002f01001400030e020a1d00020e00020e00012c00170e00020b461d0003490e02130e000319011d0004490e021b0e00040e000319024a490e02140e00010e00041902330e00012c004b1d00020d03200d03210d03220d03230d03240d03250d03260d03270d03280d03290d032a0d032b0d032c0d032d0d032e0d032f0d03300d03310d03320d03330d03340d03350d03360d03370d03380d03390d033a0d033b0d033c0d033d0d033e0d033f0d03400d03410d03420d03430d03440d03450d03460d03470d03480d03490d034a0d034b0d034c0d034d0d034e0d034f0d03500d03510d03520d03530d011f0d013e0d02cd0d02ce0d02cf0d02d00d02d10d02d20d029f0d02d30d03540d03552d00401d00030d00241d00042f001d00050e00020e0005462f034124007a0e00010e0005001d00060e00010e00052f011f001d00070e00010e00052f021f001d00080e00040e00030e00062f0212000e00030e00062f03372f04290e00072f04122b001f0e00030e00072f0f372f02290e00082f06122b001f0e00030e00082f3f37001f1f1300041c4a0e00052f031f1300051c4a14ff790e00020e0005461d00090e00092f013524003a0e00010e0005001d000a0e00040d0024082c001a0e00030e000a2f0212000e00030e000a2f03372f0429001f0d035619021f1300041c4a1400620e00092f02352400590e00010e0005001d000b0e00010e00052f011f001d000c0e00040d0024082c001a0e00030e000b2f0212000e00030e000b2f03372f04290e000c2f04122b001f0e00030e000c2f0f372f0229001f0d035719021f1300041c4a0e000433230000a30a45011d00022d00001d00030e0318180d000535240015490e0002490e03180e0001190119011d00031400ae0e0001082c03590e031b0d035a0d035b43020d002419021d00012f001d00042f001d00050e00040e00012c00171e24007d0e00052f00172400031400620e0003082c001f0e020b082c00540e0001082c00520e00042f0146190119010e030c082c00672f022f02400e0005022f081f19022f0146370e00052f0202290e020b082c00540e0001082c00520e0004190119012f060e00052f020246122b19014a130004092f040b1300051c4a14ff760e00032c00171d00060e030e0e000643011d00072f001d00080e00080e00061e2400160e00030e0008000e00070e00083a130008254a14ffe00e0007332d00001d00022f001d00050e00050e00012c00171e2400560e0001082c00290e000519011d00032d00001d00040e0004082c03580e00031600ff3719014a0e00032f08071d00030e00030cffe00e00022c001f082c00100e0002490e051a0e0004190119024a130005254a14ff9d0e0002330e00012f00000e0203361a000a0e00012f01000e0204112400020f330e00012f02000e02053521000a0e00012f03000e02063521000a0e00012f04000e02073521000a0e00012f05000e02083524000234330f330e0001082c001e0e02020e02020e02011f1902330e0001082c001e0e02020e02011f1901330e00012c00171d00020e00010e00022f0146001d00030e0001082c001e2f000e00020e0003461902330e00012c004b0e00022c004b361a000d0e00012c00170e00022c0017362400020f330e0001082c035c230000a45122021901330e00010e01020e0002003533491d00020e0319180d00053524001d0e03190d035d43011d00030e0003082c035e0e000119011d000214001c0e0001082c035f230000a4a922011901082c00230d002419011d00020e0002330e0407082c00280e00011901330e00002c00172f01312100080e00002f01003c362400090e00002f01001400030d035d1d00020e00020d036238000a0d035d3800134a14001e490e01190e000119011d0003140012490e011a0e000119011d0003140003140000490e01110e000119011d0004490e011519001d0005490e01140e00040e000319021d0003490e011619001d0006490e01180e000619011d00070e00072c01051d00080e00072c00fb1d0009490e011c0e000319011d00030e010f082c00260e000319011d000a490e01132f0019011d000b490e01140e000b0e000519021d000b490e01140e000b0e000619021d000b0e02002c00002c011e082c00e80e000a0e0008060e00094700fb0e02002c00002c00ec2c00f64700ec0e02002c00002c00f72c01184700fa19031d000c490e01140e000b0e010f082c00180e000c2c0102190119021d000b06490e011d0e000b19014703630e000b47036433490e021e0e000119011d00020e00022c00170e02020e02011f152400090e03040d0366430130490e021f0e000219012a2400090e03040d0367430130490e02200e000219011d0003490e02180e000319011d00040e00042c01051d00050e00042c00fb1d0006490e02210e000219011d00070e00072c00170e020c1e2400090e03040d03684301300e03002c00002c011e082c00e9490e021d0e000719010e0005060e00064700fb0e03002c00002c00ec2c00f64700ec0e03002c00002c00f72c01184700fa19031d0008490e02220e020f082c00180e0008190119011d00080e00082c00170e020c1e2400090e03040d03694301300e0008082c001e2f000e020c19021d0009490e02240e0008082c001e0e020c190119011d000a490e02110e000a19011d000b490e02230e00090e000b19022a2400090e03040d036a4301300e000a33230000999822011d001049230000000022020e0100230000000e220019024a2f201d00012f061d00022f741d00032f631d00042f051d00052f101d00062f001d00072f001d00082f401d00092f101d000a0d031d1d000b2f401d000c2f522f092f6a1600d52f302f361600a52f381600bf2f401600a316009e1600811600f31600d71600fb2f7c1600e32f3916008216009b2f2f1600ff1600872f3416008e2f432f441600c41600de1600e91600cb2f542f7b1600942f321600a61600c22f232f3d1600ee2f4c1600952f0b2f421600fa1600c32f4e2f082f2e1600a12f662f281600d92f241600b22f762f5b1600a22f492f6d16008b1600d12f252d00401d000d2f1f1600dd1600a82f331600882f071600c72f311600b12f122f102f592f271600801600ec2f5f2f602f512f7f1600a92f191600b52f4a2f0d2f2d1600e52f7a16009f1600931600c916009c1600ef1600a01600e02f3b2f4d1600ae2f2a1600f51600b01600c81600eb1600bb2f3c1600832f531600992f612f172f2b2f042f7e1600ba2f771600d62f261600e12f692f142f632f552f212f0c2f7d2d00401d000e0623000098cb4501470018230000992b45014700261d000f2300009a5245011d00112300009a6e45021d00122300009afb45001d00132300009b3b45021d00142300009b7745001d00152300009b9e45001d00162300009bea45011d00172300009c4e45011d00182300009cde45011d00192300009e3945011d001a2300009f5845021d001b2300009f7e45011d001c2300009fdb45011d001d230000a1ef45011d001e230000a37c45011d001f230000a3d045011d0020230000a3e445011d0021230000a3f545011d0022230000a41e45021d0023230000a45d45011d00240e0100082c03600d0361230000a4b6220119024a0e0100082c03600d0365230000a60b450119024a3c33036b0856676c65617a5f4609607b7170737c7b70710676676c65617a08786656676c65617a0f72706147747b717a784374796070660873607b76617c7a7b0b67747b717a78576c6170660b677074715c7b6126275950435b74617c63703576676c65617a35787a7160797035767a607971357b7a61357770356066707135617a35727061356670766067703567747b717a78357b60787770673b067667707461700965677a617a616c657003797c7705787c6d5c7b0e7d74665a627b45677a657067616c047c7b7c610631666065706705746565796c06706d61707b7108617a4661677c7b720576797a7b70045774667005627a67716608667c72576c6170660679707b72617d096661677c7b727c736c05767974786506767a7b7674610a21272c212c2322272c200476707c7904767479790566797c7670046560667d0667747b717a7809427a6771546767746c03707b76047f7a7c7b0006666077666167056574676670035d706d0c73677a78567d7467567a71700a767d7467567a71705461065974617c7b2414587479737a6778707135404153382d3571746174044061732d054a717461740b4a7b51746174576c617066056770667061066661677c7b72074a746565707b710977797a767e467c6f700378746d0e4a787c7b576073737067467c6f7003787c7b0f4a717a45677a7670666657797a767e066665797c7670084a65677a7670666616576073737067707157797a767e5479727a677c617d7803767372084a717a4770667061066065717461700b4a717a537c7b74797c6f7008737c7b74797c6f700d4a7667707461705d7079657067045d585456114a7667707461705d7874765d7079657067065d74667d7067047479727a036d2321047d7c727d03797a6204427a677105617a4d2627067760737370670a776c61705a73736670610a776c617059707b72617d074061732423575005406173242307406173242359500a2127222d272020262325044a78746504253b222006767d746754610b4a67706370676670587465077c7b71706d5a7341545756515053525d5c5f5e59585b5a45444746414043424d4c4f747776717073727d7c7f7e79787b7a65646766616063626d6c6f25242726212023222d2c3e3a2806577466702321094a667473704a78746540545756515053525d5c5f5e59585b5a45444746414043424d4c4f747776717073727d7c7f7e79787b7a65646766616063626d6c6f25242726212023222d2c384a095774667023216067790374776603667c7b0a21272c212c2322272c230a212527262726262124220a27202327262d26242527054a7d74667d0573797a7a6703585120075d7874765851200a26272d2026222220272504465d5424085d787476465d5424046664676103657a6206465d542720230a5d787476465d542720230a2627262d2622242526270a212421212c2427232c220a21272c252222202d20220a2627252125222021272d06465d542727210a5d787476465d542727210a2623252c22232221202d0a2625212c2627262122240a262c2321212d21262c2c0a262c272425252c2022260a27242226272c2020212d0a21252d2423272d2122270a262520262d26212723200a2721202623262022212d0a272c262223222420222c0a272d22252223262727240a2623232123252c2023250a26232721262d24252d250a272226212d2d26262c210a26202c252625212c2c210a2125232d242d27262d260a2724232725222d2725230a272324212d2d2d2425260a2627212d272727202d250a2621222c2222212d232d0a262d2620262c252125240a2723232323242621202d0a212527272727212222210a272621242723272222260a2624222027242d2426270a27242c2d2c20252d26220a272020212727252d2d270a262c2c2c22242c26262c0a272d27242d262126212c0a272c20272c2c232d252d0a27202323202c212d222c0a262724252624262322240a262725262626222c20230a262626232022242d2c240a26202d2120272d2224240a272123232c212d2c25240a2622202d262723262d260a272321262d26262d27260a27262126202722262c250a272422222527232620250a272120232c20232526220a27222625212d202c27240a272d27252625272124240a2624202d2120212722260a2627202c2226252d25250a262025202c20272320220a262621202223212222240a262024232523202d24220a2623252325252d2621210a262325252620272d25210a21252c212022242c252c0a262425252d27262220270a26222025232d20202c260a26222d20252025272d250a2626242d2625222127220a262d24272227262125260a262325272526232d2c2c0a272727222226252120270a272224232c25212625230a272623242d20272127210a2721272d2126232122210a27222023222621242d220a2622262624242527212c0a2627252125262421222c0a272c2c2c2620242022260a2626272c262720272c2d0a262d24202c27252127220a26262c2420232c2324210a262c272d262d262c25250a262024202723222722240a262c2125242d222325230a2621202125232c2026210a2124242d2326252722240a2125252527262c2c2c270a272226242520202722250a262725262c2c262525230a2723242d272c222322230a2621252c2d202024202d0a2127262120252c2d23230a21252d2c2726202227250a262421212426212722220a272727222d2226202c200a212722242422202227260a27222226212d252223270a272c24222023202426220a272325252d27272c27210a21272420262d2c20212206465d542024270a5d787476465d542024270a2621242d2522252623200a2721262d20272c2622250a27262c21242d252726240a2623222025252d20272006465d54262d210a5d787476465d54262d210c7a606165606159707b72617d064a666174617004465d5426085d787476465d54260a272125252c202c22252d0a272d21252d20262d262d09475c455058512423250d5d787476475c45505851242325074a7d74667d7067054a7a5e706c054a7c5e706c077e706c467c6f70067d74667d70670a7c61706774617c7a7b6607767a78656061700645575e515327065063655e515306567c657d70670f4a505b564a4d535a47584a585a51500f766770746170507b76676c65617a670f4a5150564a4d535a47584a585a51500f766770746170517076676c65617a670a4a6d737a6778587a7170044a7e706c0765677a76706666067c63467c6f7007707b76676c656107717076676c656105737960667d0c466167707478567c657d706704787a717009507b76676c65617a6709517076676c65617a67074a767c657d7067034a7c630f57797a767e567c657d7067587a71700c707b76676c656157797a767e0a4a6567706357797a767e0c65677a7670666657797a767e0c717076676c656157797a767e035657560365747105607b65747105457e76662207657471717c7b72027c63054a787a7170094a4a76677074617a670b57797a767e567c657d706709737a677874616170670c567c657d706745746774786606737a677874610a767c657d706761706d610466747961075a65707b464659037e706c097479727a677c617d78064a6574676670124670677c74797c6f74777970567c657d7067037e717307706d70766061701345746666627a67715774667071567c657d706703565357084a767a607b617067035641470a5641475279747178747b0a4a7e706c666167707478035a53570350565708547b667c4d2c2726085c667a24252427230a27242122212d2623212d0b4f70677a457471717c7b72085c667a2c222c2224095b7a457471717c7b72084a7b477a607b71660e4a7e706c45677c7a6747706670610c4a7e706c46767d70716079700f4a7c7b635e706c46767d70716079700d4a717a56676c656157797a767e0354504601250927232d212620212023092026232d22252c2427092d252026252326232d0a242522262221242d27210a24262127242222272d250a242324252324272226230a242d222c25212d242c270a272124202c242c2425210a27232d212620212023250a272c2027222c252524230a262727242727202122270a26212d2c2323252c272d0a2622202d252c23262d210a212527232026242d21250924262127242222272d09212527232026242d2109232224252d2d232125092c262c202721252c230a242725222c202c2020270a24212223262c2025252d0a242221212d26252123210a272524262723202c27250a27272d242225242622230a272020252426232d26270a272d242d202227272d2d0a26252d222525222221210a262620202121262725250a262327262d222d2320230a262d2c272624212424270a2124232522212c20232d01240927232d212620212022092026232d22252c2426092d252026252326232c0a242522262221242d27200a24262127242222272d240a242324252324272226220a242d222c25212d242c260a27242122212d2623212c0a272124202c242c2425200a27232d212620212023240a272c2027222c252524220a262727242727202122260a26212d2c2323252c272c0a2622202d252c23262d200a212527232026242d21240924262127242222272c09212527232026242d2009232224252d2d232124092c262c202721252c220a242725222c202c2020260a24212223262c2025252c0a242221212d26252123200a272524262723202c27240a27272d242225242622220a272020252426232d26260a272d242d202227272d2c0a26252d222525222221200a262620202121262725240a262327262d222d2320220a262d2c272624212424260a2124232522212c20232c08242322222227242308262620202121262708202526262423212d08232224252d2d2321082d262d2d23252d2509242525232326272c2309242422212125202427092420252c2c212c21210924232222222724232509242d2120212c26222309272524262723202c270927242d2425262d252d092726212d2d242527210927202423202d272125072d262d2d23252d0827202423202d27210821242c212625212508202d222725272023082220212c22212227082c27272221232d2d0924252c2520242c2521092427202d272c242725092421272325232626230924202c262d262020270924222324232522232d09242c272c26222c2d210927252c22242027252509272723212c272124230927212627232c232627092723252521232d212d09272d20272427232227092625242c2d2c2d2d2d0926242d22232224252109262620202121262725092620272627242026230926232c252c2d22202709262d202d22202c232d0921242c21262521252509212623272522232423092120272c2d212d26270921232c22232725212d09212d2320262c27232109202526262423212d2509202725252c26232c23092722232d272125232109272c26232524272d250926242526222d212c2309262722242020222427092621262c26272c272d0926232522242524212109262222212d2226232509262c2127232120222309212424252124222c27092127222d242c25252d09212121202c23272721092123242622262121250921222d24202523202309212c212c27222d222709202424222520252d2d0920272d212d27262521072425212d2022230727252c22242027072624212022272d0721242c2126252107202721272d2d250723272c242120230722262125252627072c212622242d21082425212d20222325082424202621262623082427202d272c2427082426232624212d2d082421232d2525232108242022272d23212506202721272d2d07242022272d232107272327242121250726232225252423072122242d202c27072022232224232d07232d242022212107222d2321262725072d2c24272d2c23072c2c232421222708242425242525212d08242725202d2327210824262425222725250824212420202222230824202725212620270824232720272c272d0824222d2720222c2708242d2d222126232d08242c2c27272c21210827252c2224202725082727252725252c2308272625232d23222708272124242227212d0827232724212125250827222723272c222308272d26242420202708272c26232524272d08262521252d222521082624212022272d250826272025202d202308242226252420252108242d262025252d2508242c262c2d232023082725212122272627082724212c202d252d082727202121262d21082726202c272c2325082721232124202623082720232c2524242708272322262d232d2d082722222d2227232108272d2d26202d212508272c2d2d212124230826252c26272c2c270826242c2d2420232d0826262526252421210a27242024232d2725212d0a27242122212d222d252d052320202623062426242522270a272420242322222c202706242c2323252d0627232724212106262722232d250a27242122212d2622242706262c262724230621202d22202706202d2c2d2721062320202623250a27242122212d22222121062227252d2c230a2724202423222d25242306222d23212627062d20242c232d062c24222025210a27242024232d27242427062c2d2625212505262722232d052c2d262521062423262d21250627272c26222306272c212c24270626232521212d062127202c2d2106212c242027250620202225202306232727202c2706232d2d24272d06222026232321062d242c272525062d2d21222623062c202527222707242524202d252d0724242421242427072424222c23212d0724272120242d21072426242522272507242622232720230724212124222c27072420252226272d072423262d21252507242225262c2623072422232c21222707242d262025252d07242c252520212107242c2323252d2507272526242324230724252d2426212107242421232d2d25072427242721242307242722222c20270724262126212d2d072421252c25272107242122212023250724202125252c230724232520232627072423222424232d072422262322252107242d252727212507242d232222222307242c262626242707242c2c2d2d212d0727252321262d210421252c23042d242c27052427272d2d052423262d21052725212d2505272120222305272d2322270526232d23210521252c232505212025202305212c24202705202627212d052022262121052324212125042725212d042324212105242527212505242126262305242d21262705272720272d0527232327210526252227250526212d242305262d2c242705212625252d052122242521052024272525052020272c2305202c262c27052326212d2d05232c23262705222622272d0522222d2721052d242c2725052d23252423052c25242427052c2127252d0624252721252506242523212c2306242425202c2706242421232d2d0624242d222d21062427272d2d25062427232c2223052322202d21052224232d2505222022222305222c2d2227052d262c232d052d2d252321052c27242325052c23272023062425252620270624252121212d0624252d2021210624242723212506242423222623062427252d2627062427212c272d0624272c25272103272023032024270322232d04242527210424272d2504242026230424222c270427262521042720232504272d24230426252227042626272d0426202d2104262d21250324272d03262d2103232125032d2c230424242027042421252d042423232104242c2725042724222304272126270427232d2d04272c212104262725250426212023042622242704262c232d0421262027042123252d04212d232104202427250420262223042023262704202d2d2d0423212525042323202304232c2427042224232d04222127210422232d2504222c262304212727210421212d25042122262304212c2c27042027212d0420202521042022232504232524230423272227042320272d0423222d2104222521250422272c23042220202704222d252d042d25232102242302262702212d022321022d25022c230324242703242121032423250324222303242c270327252d0327272103272125012d022721022125022023022227022d2d032425210324272503242623032420270324232d03242d210327252503272423032726270327212d0327222703272d2d032625210326272503262623032620270326232d0321252503212423032126270321212d0321232103212d2503212c230327232103272d2503272c23032624270326272d03262121032623250326222303262c270321252d0321272103212125032120230321222703212d2d03202521012701260121012001230122012c0224250224240224270224260224210224200a27242122212d262320250a27242122212d262320240a27242122212d262320270a27242122212d262320260a27242122212d262320210a27242122212d262320200a27242122212d262320230a27242122212d262320220a27242122212d2623202d0a27242122212d2623202c0a27242122212d262323250a27242122212d262323240a27242122212d262323270a27242122212d2623232602242202242d02242c02272502272402272702272602272002272302272202272d02272c0226250226240a27242122212d262323210a27242122212d262323200a27242122212d262323230a27242122212d262323220a27242122212d2623232d0a27242122212d2623232c0a27242122212d262322250a27242122212d262322240a27242122212d262322270a27242122212d262322260a27242122212d262322210a27242122212d262322200a27242122212d262322230a27242122212d262322220a27242122212d2623222d0a27242122212d2623222c084a6660775e706c660b4a7c7b634660775e706c66074a7957797a767e074a6757797a767e035150464d5c7b6374797c71357e706c3579707b72617d3538352651504635677064607c67706635617d70357e706c3579707b72617d35617a357770352321393524272d3935242c27357a67352b242c273b054a71706624054a71706627054a717066260941677c657970515046024a46024a7f024a7c034756210471677a650747562151677a65024a4d0a21272c212c2524222325024a56024a7706477477777c610a262021202520272622240c477477777c6159707274766c40545756515053525d5c5f5e59585b5a45444746414043424d4c4f747776717073727d7c7f7e79787b7a65646766616063626d6c6f25242726212023222d2c3e3a0a2127222d242c25252d2504737c79790154015701560151015001530152015d015c015f015e01590158015b015a01450144014701460141014001430142014d014c014f0174017701760171017001730172017d017c017f017e01790178017b017a01650164016701660161016001630162016d016c016f013e013a022828012807607b667d7c736107677065797476700c4e4b54384f25382c3e493a4802727c05706370676c05606173382d067170767a7170037874650e6770727c6661417a52797a7774790d746565597a72507b76676c656107717073746079610677746670232106777c7b74676c0d746565597a72517076676c6561167174617435667c6f70357c6635617a7a35667d7a6761127874727c76357b6078777067357067677a6720707b76676c65617071357174617435667c6f70357c6635617a7a35667d7a676120717076676c65617071357174617435667c6f70357c6635617a7a35667d7a67610d767d70767e3566607835706767",
        {
            get 0() {
                return "undefined" != typeof window ? window : void 0;
            },
            get 1() {
                return "undefined" != typeof self ? self : void 0;
            },
            2: globalThis,
            3: Uint32Array,
            4: Error,
            5: Object,
            6: parseInt,
            7: String,
            8: decodeURIComponent,
            get 9() {
                return escape;
            },
            get 10() {
                return unescape;
            },
            11: encodeURIComponent,
            12: Math,
            13: ArrayBuffer,
            14: Uint8Array,
            15: Int8Array,
            16: Uint8ClampedArray,
            17: Int16Array,
            18: Uint16Array,
            19: Int32Array,
            20: Float32Array,
            21: Float64Array,
            22: Array,
            23: Boolean,
            get 24() {
                return "undefined" != typeof atob ? atob : void 0;
            },
            get 25() {
                return "undefined" != typeof TextDecoder ? TextDecoder : void 0;
            },
            get 26() {
                return c;
            },
            27: RegExp,
        },
        void 0,
    ),
        (function (e, f, d) {
            function c(e, f) {
                var d = parseInt(e.slice(f, f + 2), 16);
                return d >>> 7 == 0
                       ? [1, d]
                       : d >>> 6 == 2
                         ? ((d = (63 & d) << 8), [2, (d += parseInt(e.slice(f + 2, f + 4), 16))])
                         : ((d = (63 & d) << 16), [3, (d += parseInt(e.slice(f + 2, f + 6), 16))]);
            }

            var a,
                b = 0,
                r = [],
                t = [];
            for (a = 0; a < 4; ++a) b += (3 & parseInt(e.slice(8 + 2 * a, 10 + 2 * a), 16)) << (2 * a);
            var n = parseInt(e.slice(16, 24), 16),
                o = 2 * parseInt(e.slice(32, 40), 16);
            for (a = 40; a < o + 40; a += 2) r.push(parseInt(e.slice(a, a + 2), 16));
            var s = o + 40,
                i = parseInt(e.slice(s, s + 4), 16);
            for (s += 4, a = 0; a < i; ++a) {
                var u = c(e, s);
                s += 2 * u[0];
                for (var l = "", p = 0; p < u[1]; ++p) {
                    var k = c(e, s);
                    ((l += String.fromCharCode(b ^ k[1])), (s += 2 * k[0]));
                }
                t.push(l);
            }
            ((f.p = null),
                (function e(f, d, c, a, b) {
                    var n,
                        o,
                        s,
                        i,
                        u,
                        l = -1,
                        p = [],
                        k = [0, null],
                        y = null,
                        h = [d];
                    for (o = Math.min(d.length, c), s = 0; s < o; ++s) h.push(d[s]);
                    h.p = a;
                    for (var v = []; ;)
                        try {
                            switch (r[f++]) {
                                case 43:
                                    p[++l] = null;
                                    break;
                                case 71:
                                    ((n = r[f++]), (p[++l] = (n << 24) >> 24));
                                    break;
                                case 62:
                                    ((n = (r[f] << 8) + r[f + 1]), (f += 2), (p[++l] = (n << 16) >> 16));
                                    break;
                                case 65:
                                    ((n = ((n = ((n = r[f++]) << 8) + r[f++]) << 8) + r[f++]), (p[++l] = (n << 8) + r[f++]));
                                    break;
                                case 22:
                                    ((n = (r[f] << 8) + r[f + 1]), (f += 2), (p[++l] = t[n]));
                                    break;
                                case 21:
                                    p[++l] = void 0;
                                    break;
                                case 70:
                                    ((n = (r[f] << 8) + r[f + 1]), (f += 2), (l = l - n + 1), (o = p.slice(
                                        l, l + n)), (p[l] = o));
                                    break;
                                case 73:
                                    p[++l] = {};
                                    break;
                                case 39:
                                    ((n = (r[f] << 8) + r[f + 1]), (f += 2), (o = t[n]), (s = p[l--]), (p[l][o] = s));
                                    break;
                                case 1:
                                    for (o = r[f++], s = r[f++], i = h; o > 0; --o) i = i.p;
                                    p[++l] = i[s];
                                    break;
                                case 36:
                                    ((n = (r[f] << 8) + r[f + 1]), (f += 2), (o = t[n]), (p[l] = p[l][o]));
                                    break;
                                case 53:
                                    ((o = p[l--]), (p[l] = p[l][o]));
                                    break;
                                case 46:
                                    for (o = r[f++], s = r[f++], i = h; o > 0; --o) i = i.p;
                                    i[s] = p[l--];
                                    break;
                                case 75:
                                    ((n = (r[f] << 8) + r[f + 1]), (f += 2), (o = t[n]), (s = p[l--]), (i = p[l--]), (s[o] = i));
                                    break;
                                case 6:
                                    ((o = p[l--]), (s = p[l--]), (i = p[l--]), (s[o] = i));
                                    break;
                                case 19:
                                    for (o = r[f++], s = r[f++], i = h, i = h; o > 0; --o) i = i.p;
                                    ((p[++l] = i), (p[++l] = s));
                                    break;
                                case 31:
                                    ((o = p[l--]), (p[l] += o));
                                    break;
                                case 17:
                                    ((o = p[l--]), (p[l] /= o));
                                    break;
                                case 8:
                                    p[l] = -p[l];
                                    break;
                                case 40:
                                    ((o = p[l--]), (p[l] = p[l] === o));
                                    break;
                                case 10:
                                    ((o = p[l--]), (p[l] = p[l] !== o));
                                    break;
                                case 60:
                                    p[l] = !p[l];
                                    break;
                                case 11:
                                    ((n = ((n = (r[f] << 8) + r[f + 1]) << 16) >> 16), (f += 2), p[l] ? (f += n) : --l);
                                    break;
                                case 32:
                                    ((o = p[l--]), ((s = p[l--])[o] = p[l]));
                                    break;
                                case 48:
                                    p[l] = typeof p[l];
                                    break;
                                case 20:
                                    ((n = r[f++]),
                                        (o = p[l--]),
                                        ((s = function e() {
                                            var f = e._v;
                                            return (0, e._u)(f[0], arguments, f[1], f[2], this);
                                        })._v = [o, n, h]),
                                        (s._u = e),
                                        (p[++l] = s));
                                    break;
                                case 12:
                                    ((n = ((n = (r[f] << 8) + r[f + 1]) << 16) >> 16), (f += 2), ((o = v[v.length - 1])[1] = f + n));
                                    break;
                                case 47:
                                    ((n = ((n = (r[f] << 8) + r[f + 1]) << 16) >> 16),
                                        (f += 2),
                                        (o = v[v.length - 1]) && !o[1] ? ((o[0] = 3), o.push(f)) : v.push([1, 0, f]),
                                        (f += n));
                                    break;
                                case 44:
                                    ((n = ((n = (r[f] << 8) + r[f + 1]) << 16) >> 16), (f += 2), v.push(
                                        [2, 0, f]), (f += n));
                                    break;
                                case 41:
                                    if (((s = (o = v.pop())[0]), (i = k[0]), 1 === s)) f = o[1];
                                    else if (0 === s)
                                        if (0 === i) f = o[1];
                                        else {
                                            if (1 !== i) throw k[1];
                                            if (!y) return k[1];
                                            ((f = y[1]), (b = y[2]), (h = y[3]), (v = y[4]), (p[++l] = k[1]), (k = [0,
                                                                                                                    null]), (y = y[0]));
                                        }
                                    else ((f = o[2]), (o[0] = 0), v.push(o));
                                    break;
                                case 28:
                                    for (o = p[l--], s = null; (i = v.pop());)
                                        if (2 === i[0] || 3 === i[0]) {
                                            s = i;
                                            break;
                                        }
                                    if (s) ((k = [1, o]), (f = s[2]), (s[0] = 0), v.push(s));
                                    else {
                                        if (!y) return o;
                                        ((f = y[1]), (b = y[2]), (h = y[3]), (v = y[4]), (p[++l] = o), (k = [0,
                                                                                                             null]), (y = y[0]));
                                    }
                                    break;
                                case 63:
                                    ((l -= n = r[f++]),
                                        (s = p.slice(l + 1, l + n + 1)),
                                        (o = p[l--]),
                                        (i = p[l--]),
                                        o._u === e
                                        ? ((o = o._v),
                                            (y = [y, f, b, h, v]),
                                            (f = o[0]),
                                        null == i &&
                                        (i = (function () {
                                            return this;
                                        })()),
                                            (b = i),
                                            ((h = [s].concat(s)).length = Math.min(o[1], n) + 1),
                                            (h.p = o[2]),
                                            (v = []))
                                        : ((u = o.apply(i, s)), (p[++l] = u)));
                                    break;
                                case 74:
                                    for (n = r[f++], i = [void 0], u = n; u > 0; --u) i[u] = p[l--];
                                    ((s = p[l--]), (u = new (o = Function.bind.apply(s, i))()), (p[++l] = u));
                                    break;
                                case 38:
                                    f += 2 + (n = ((n = (r[f] << 8) + r[f + 1]) << 16) >> 16);
                                    break;
                                case 27:
                                    ((n = ((n = (r[f] << 8) + r[f + 1]) << 16) >> 16), (f += 2), (o = p[l--]) || (f += n));
                                    break;
                                case 16:
                                    --l;
                                    break;
                                case 52:
                                    ((o = p[l]), (p[++l] = o));
                                    break;
                                default:
                                    throw new Error("ioe");
                            }
                        } catch (e) {
                            for (k = [0, null]; (n = v.pop()) && !n[0];) ;
                            if (!n) {
                                e: for (; y;) {
                                    for (o = y[4]; (n = o.pop());) if (n[0]) break e;
                                    y = y[0];
                                }
                                if (!y) throw e;
                                ((f = y[1]), (b = y[2]), (h = y[3]), (v = y[4]), (y = y[0]));
                            }
                            1 === (o = n[0])
                            ? ((f = n[2]), (n[0] = 0), v.push(n), (p[++l] = e))
                            : 2 === o
                              ? ((f = n[2]), (n[0] = 0), v.push(n), (k = [3, e]))
                              : ((f = n[3]), (n[0] = 2), v.push(n), (p[++l] = e));
                        }
                })(n, [], 0, f, d));
        })(
            "504B0101e8ecf5c2000006bbc2f5eeeb000006e50102010100010102002400022400034a022e00022b01020201020334240004010204342400053f003e03e8113f013f012e0003492e0004010205240006342400071600083f013424000941000002ed14013f011001000224000e3424000f1600103f010b000f01000224000e3424000f1600113f010b000f01000224000e3424000f1600123f010b00060100042400100b00060100042400130b00060100042400140b00060100042400152e00050100053c1b000c49010001270016492700171c492e00064600002e00072b01020901000224000e342400183f003f012e00082c000b010008342400193f0010292f00112e00120100083424001a0100123f0110290c00c40100083424001b3f00100100083424001c3f001300092024001d3c1b00a52b01020a01000924001e47023f022e000a01000a4700352e000b01000a4701352e000c01000b16001f281b00040100011c2b01020601000c3f012e000d01000d01000c0a1b002f01000d01000601000b06010007342400201600213424002201000b16000b3f023424002201000d3f013f011026002c01000c01000601000b06010007342400201600213424002201000b16000b3f023424002201000c3f013f011026ff472901000224000e342400231600103f013c1b001f0100050100064b001001000734240020160024342400220100053f013f011001000224000e342400231600253f013c1b001f0100030100064b002501000734240020160026342400220100033f013f0110010005010003160027010007342400281600293f014600042e000e01020024002a3424002b01000e3424002816002c3f013f013424002d3f002e000f01000f01000616001f060100013424002e16002f3f011b00120100013424000716002f3f014700352600030100012e001001001016002f1f1300102010010207342400300100063f0134240009410000032f14013f012e001149010010010011342400281600293f011f2700164901000527001001000f27001f0100032700312700171c0100013424000a16000b3f012e00020100024701080a1b00270100013424000c01000247011f3f010101040100013424000c47000100023f023424000d3f0006151c1600213424002201000116000b3f0234240022010106010001353f011c0102010100010102002400022400034a022e00042b01020201020334240004010204342400053f003e03e8113f013f012e0005492e0006010205240006342400071600083f0134240009410000065c14013f01100100062400100b00060100062400130b000f01000424000e3424000f1600103f010b00060100062400140b000f01000424000e3424000f1600113f010b00060100062400150b000f01000424000e3424000f1600123f012e00070100073c1b000c49010001270016492700171c492e00084600002e00092b01020901000424000e342400183f003f012e000a2c000b01000a342400193f0010292f00112e001501000a3424001a0100153f0110290c00cc01000a3424001b3f001001000a3424001c3f0013000b2024001d3c1b00ad2b01020a01000b24001e47023f022e000c01000c4700352e000d01000c4701352e000e01000d16001f281b000c49010001270016492700171c2b01020601000e3f012e000f01000f01000e0a1b002f01000f01000801000d06010009342400201600213424002201000d16000b3f023424002201000f3f013f011026002c01000e01000801000d06010009342400201600213424002201000d16000b3f023424002201000e3f013f011026ff3f2901000424000e342400231600103f013c1b00090100070100084b001001000424000e342400231600253f013c1b00090100050100084b00250100013424002e16002f3f011b00120100013424000716002f3f014700352600030100012e001001001016002f1f1300102010010207342400300100083f0134240009410000069e14013f012e00110100023c1b001949010010010011342400281600293f011f270016492700171c01000230160033281b000601000226000c010208342400340100023f012e00120100070100051600270100123424000c47000100033f024600042e001301020024002a3424002b0100133424002816002c3f013f013424002d3f002e001449010010010011342400281600293f011f27001649010007270010160035342400220100033f0127003601001427001f0100052700312700171c0100013424000a16000b3f012e00020100024701080a1b00270100013424000c01000247011f3f010101060100013424000c47000100023f023424000d3f0006151c1600213424002201000116000b3f0234240022010108010001353f011c01010034240000160001410000000014013f021001010034240000160032410000034c14033f0210151c00370e80e280f580f780f980e380e480c480ff80d780fc80ff80f280f180fc0a80e780f580f280c380f980f780fe80c580e280fc0880fc80ff80f380f180e480f980ff80fe0480f880e280f580f60580f680fc80ff80ff80e20380fe80ff80e70680f380ff80ff80fb80f980f50580e380e080fc80f980e40180ab0380fd80f180e00780f980fe80f480f580e880df80f60180ad0580e380fc80f980f380f50480e480e280f980fd0c80e380f580f180e280f380f880c080f180e280f180fd80e30380f780f580e40580e580f980f680f980f40a80e580f980f680f980f480cf80e480f580fd80e00980e580f980f680f980f480e480f580fd80e00580c580d980d680d980d40a80c580d980d680d980d480cf80c480d580dd80c00980c580d980d680d980d480c480d580dd80c00380e580e280fc0780f880f580f180f480f580e280e30780f580fe80e480e280f980f580e30180f60180f50180e30180fe0480f480ff80fe80f50580e680f180fc80e580f51680e880bd80e380f580f380e380f480fb80bd80e780f580f280bd80e380f980f780fe80f180e480e580e280f50480e080e580e380f8000680f380ff80fe80f380f180e40380f880f180e30680e580f980f680f980f480ad0980e480f980fd80f580e380e480f180fd80e00a80e480f980fd80f580e380e480f180fd80e080ad2080d180a980a680d480a880a580a580d180a080a880d380a080d180a980a780a080a780d680a880d280d580d680a080d480a980d180a580a280a780d580a480d50480fa80ff80f980fe0180b60880d380e280e980e080e480ff80da80c30380dd80d480a50180cf0880e480ff80c380e480e280f980fe80f70880f980fe80f380fc80e580f480f580e30180af0480fb80f580e980e31380e880bd80e380f580f380e380f480fb80bd80e780f580f280bd80f580e880e080f980e280f50b80e780f580f280c380f980f780fe80d280ff80f480e90680e380e480e280f980fe80f70980e380e480e280f980fe80f780f980f680e90280a180cf1480e880bd80e380f580f380e380f480fb80bd80e380f980f780fe80bd80f380ff80fe80f680f980f7",
            {
                get 0() {
                    return window;
                },
                get 1() {
                    return URL;
                },
                2: String,
                3: Math,
                4: Date,
                get 5() {
                    return document;
                },
                6: encodeURIComponent,
                7: Object,
                8: JSON,
                get 9() {
                    return f;
                },
                get 10() {
                    return d;
                },
            },
            void 0,
        ),
        window.registToGlobal("executeFetchRequest", function (e, f, d) {
            var c = e.payload,
                a = window.use("ActionType"),
                b = f.type;
            "csrfWebToken" === f.strategyKey &&
            b === a.REWRITE &&
            (new Headers(c.context.headers).has("x-secsdk-csrf-token") || c.addHeader(
                "x-secsdk-csrf-token", "DOWNGRADE"));
            if ("webSign" === f.strategyKey && b === a.REWRITE)
                try {
                    var r,
                        t,
                        n,
                        o,
                        s = window.use("webSignUrl"),
                        i =
                            null === (r = window) ||
                            void 0 === r ||
                            null === (t = r.SSR_RENDER_DATA) ||
                            void 0 === t ||
                            null === (n = t.app) ||
                            void 0 === n ||
                            null === (o = n.odin) ||
                            void 0 === o
                            ? void 0
                            : o.user_id;
                    ((window._secsdk_uifid = i), (c.args[0] = s(c.url).url));
                } catch (e) {}
            if (d) return c.originFn.apply(c.context, c.args);
        }),
        window.registToGlobal("executeXHRRequestSend", function (e, f, d) {
            var c = e.payload,
                a = window.use("ActionType"),
                b = f.type;
            if ("csrfWebToken" === f.strategyKey && b === a.REWRITE) {
                var r = c.context.__secReqHeaders || {};
                r["x-secsdk-csrf-token"] ||
                (c.context.SDKNativeWebApi.XHR_REQUEST_SETQEQUESTHEADER.fn.call(
                    c.context,
                    "x-secsdk-csrf-token",
                    "DOWNGRADE",
                ),
                    (c.context.__secReqHeaders = r),
                    (c.context.__secReqHeaders["x-secsdk-csrf-token"] = "DOWNGRADE"));
            }
            if (d) return c.originFn.apply(c.context, c.args);
        }),
        window.registToGlobal("executeXHRRequestOpen", function (e, f, d) {
            var c = f.payload,
                a = window.use("ActionType"),
                b = f.type;
            if ("diggParams" === f.strategyKey && b === a.REWRITE)
                try {
                    var r = e.payload.args[1],
                        t = c.uid,
                        n = window.CryptoJS.MD5(t).toString();
                    (r.includes("?") ? (r += "&uid=".concat(n)) : (r += "?uid=".concat(n)), (e.payload.args[1] = r));
                } catch (e) {}
            if ("webSign" === f.strategyKey && b === a.REWRITE)
                try {
                    var o,
                        s,
                        i,
                        u,
                        l = window.use("webSignUrl"),
                        p =
                            null === (o = window) ||
                            void 0 === o ||
                            null === (s = o.SSR_RENDER_DATA) ||
                            void 0 === s ||
                            null === (i = s.app) ||
                            void 0 === i ||
                            null === (u = i.odin) ||
                            void 0 === u
                            ? void 0
                            : u.user_id;
                    window._secsdk_uifid = p;
                    var k = e.payload.args[1];
                    e.payload.args[1] = l(k).url;
                } catch (e) {}
            if ("uidRequest" === f.strategyKey && b === a.REWRITE) {
                var y = c.uid;
                if (y) {
                    var h = e.payload.args[1],
                        v = new URL(h);
                    (v.searchParams.append("secsdk_uid", y), (e.payload.args[1] = v.toString()));
                }
            }
            if (d) return e.payload.originFn.apply(e.payload.context, e.payload.args);
        }),
        window.registToGlobal("executeSDKInit", function (e, f, d) {
            var c = f.type;
            if ("envVarDetect" === f.strategyKey)
                if ("BLOCK" !== c) var a;
                else
                    try {
                        var b = document.createElement("div");
                        ((b.id = "__sec_env_block__"),
                            (b.style.cssText =
                                "position:fixed;top:0;left:0;width:100vw;height:100vh;background:#fff;z-index:2147483647;"));
                        ((a = document.body || document.documentElement) &&
                        !document.getElementById("__sec_env_block__") &&
                        a.appendChild(b),
                            document.addEventListener("DOMContentLoaded", function () {
                                ((document.body.innerHTML = ""), document.body.appendChild(b));
                            }));
                    } catch (e) {}
        }));
});
/*!
 * @byted/secsdk-strategy v1.0.40
 * (c) 2026
 */
!(function (e) {
    "function" == typeof define && define.amd ? define(e) : e();
})(function () {
    "use strict";

    function e(e, t) {
        (null == t || t > e.length) && (t = e.length);
        for (var o = 0, a = Array(t); o < t; o++) a[o] = e[o];
        return a;
    }

    function t(e, t) {
        var o = ("undefined" != typeof Symbol && e[Symbol.iterator]) || e["@@iterator"];
        if (!o) {
            if (Array.isArray(e) || (o = r(e)) || (t && e && "number" == typeof e.length)) {
                o && (e = o);
                var a = 0,
                    n = function () {};
                return {
                    s: n,
                    n: function () {
                        return a >= e.length ? {done: !0} : {done: !1, value: e[a++]};
                    },
                    e: function (e) {
                        throw e;
                    },
                    f: n,
                };
            }
            throw new TypeError(
                "Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
            );
        }
        var i,
            w = !0,
            m = !1;
        return {
            s: function () {
                o = o.call(e);
            },
            n: function () {
                var e = o.next();
                return ((w = e.done), e);
            },
            e: function (e) {
                ((m = !0), (i = e));
            },
            f: function () {
                try {
                    w || null == o.return || o.return();
                } finally {
                    if (m) throw i;
                }
            },
        };
    }

    function o(e, t) {
        return (
            (function (e) {
                if (Array.isArray(e)) return e;
            })(e) ||
            (function (e, t) {
                var o = null == e ? null : ("undefined" != typeof Symbol && e[Symbol.iterator]) || e["@@iterator"];
                if (null != o) {
                    var a,
                        r,
                        n,
                        i,
                        w = [],
                        m = !0,
                        c = !1;
                    try {
                        if (((n = (o = o.call(e)).next), 0 === t)) {
                            if (Object(o) !== o) return;
                            m = !1;
                        } else for (; !(m = (a = n.call(o)).done) && (w.push(a.value), w.length !== t); m = !0) ;
                    } catch (e) {
                        ((c = !0), (r = e));
                    } finally {
                        try {
                            if (!m && null != o.return && ((i = o.return()), Object(i) !== i)) return;
                        } finally {
                            if (c) throw r;
                        }
                    }
                    return w;
                }
            })(e, t) ||
            r(e, t) ||
            (function () {
                throw new TypeError(
                    "Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
                );
            })()
        );
    }

    function a(e) {
        return (
            (a =
                "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
                ? function (e) {
                    return typeof e;
                }
                : function (e) {
                    return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype
                           ? "symbol"
                           : typeof e;
                }),
                a(e)
        );
    }

    function r(t, o) {
        if (t) {
            if ("string" == typeof t) return e(t, o);
            var a = {}.toString.call(t).slice(8, -1);
            return (
                "Object" === a && t.constructor && (a = t.constructor.name),
                    "Map" === a || "Set" === a
                    ? Array.from(t)
                    : "Arguments" === a || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(a)
                      ? e(t, o)
                      : void 0
            );
        }
    }

    var n = function (e, t, o, a) {
        o = o.toUpperCase();
        var r = e;
        if (!r[t]) return !1;
        if (!r[t][o]) return !1;
        var n = r[t][o];
        return n instanceof RegExp
               ? n.test(a)
               : Array.isArray(n)
                 ? n.some(function (e) {
                    return e instanceof RegExp ? e.test(a) : e === a;
                })
                 : "*" === n || n === a;
    };
    window.registToModule("strategy", {
        event: {
            SDK_INIT: ["envVarDetect"],
            XHR_REQUEST_OPEN: ["webSign", "diggParams"],
            XHR_REQUEST_SEND: ["csrfWebToken", "cancelDigg", "requestFeatureDetect"],
            FETCH_REQUEST: ["csrfWebToken", "cancelDigg", "diggParams", "webSign"],
        },
        strategy: {
            requestFeatureDetect: {
                body: {
                    singleKey: "requestFeatureDetect",
                    version: "4",
                    createdAt: "2026-05-18T02:57:55.000Z",
                    latest: 0,
                    strategyKey: "requestFeatureDetect",
                    key: "requestFeatureDetect",
                    disabled: !1,
                    condition: "",
                    expression: function (e) {
                        var t,
                            o,
                            r,
                            n,
                            i,
                            w,
                            m,
                            c,
                            l,
                            u,
                            d = window.use("ActionType");

                        function s(e) {
                            return String(e || "").toUpperCase();
                        }

                        function y(e, t) {
                            return !e || "*" === e || String(e) === String(t || "");
                        }

                        function v(e, t) {
                            if (!Array.isArray(e) || 0 === e.length) return !0;
                            if (e.includes("*")) return !0;
                            var o = new Set(
                                (t || []).map(function (e) {
                                    return String(e);
                                }),
                            );
                            return e.every(function (e) {
                                return o.has(String(e));
                            });
                        }

                        var b,
                            p = window.use("strategy").strategy.requestFeatureDetect.config,
                            f = e.payload,
                            h = (function (e) {
                                var t, o, a;
                                return s(
                                    null !== (t = null == e ? void 0 : e.method) && void 0 !== t
                                    ? t
                                    : null == e ||
                                      null === (o = e.context) ||
                                      void 0 === o ||
                                      null === (a = o._xhr_open_args) ||
                                      void 0 === a
                                      ? void 0
                                      : a.method,
                                );
                            })(f),
                            g = (function (e) {
                                var t, o, a, r;
                                return null !==
                                       (t =
                                           null !== (o = null == e ? void 0 : e.url) && void 0 !== o
                                           ? o
                                           : null == e ||
                                             null === (a = e.context) ||
                                             void 0 === a ||
                                             null === (r = a._xhr_open_args) ||
                                             void 0 === r
                                             ? void 0
                                             : r.url) && void 0 !== t
                                       ? t
                                       : "";
                            })(f),
                            _ =
                                null !==
                                (t =
                                    null !== (o = null == f ? void 0 : f.body) && void 0 !== o
                                    ? o
                                    :
                                    null == f || null === (r = f.args) || void 0 === r || null === (n = r[0]) || void 0 === n
                                    ? void 0
                                    : n.body) && void 0 !== t
                                ? t
                                :
                                null == f || null === (i = f.args) || void 0 === i || null === (w = i[1]) || void 0 === w
                                ? void 0
                                : w.body;
                        _ || (_ = null == f || null === (b = f.args) || void 0 === b ? void 0 : b[0]);
                        var S = "";
                        try {
                            S = new URL(g || "", window.location.href).host;
                        } catch (e) {}
                        var T = (function (e) {
                                try {
                                    var t = new URL(e || "", window.location.href);
                                    return Array.from(t.searchParams.keys());
                                } catch (e) {
                                    return [];
                                }
                            })(g),
                            R = (function (e) {
                                if (!e) return [];
                                if ("string" == typeof e) {
                                    try {
                                        var t = JSON.parse(e);
                                        if (t && "object" === a(t) && !Array.isArray(t)) return Object.keys(t);
                                    } catch (e) {}
                                    try {
                                        var o = new URLSearchParams(e),
                                            r = Array.from(o.keys());
                                        if (r.length) return r;
                                    } catch (e) {}
                                    return e
                                        .split(/[&=,{}:\\"\s]+/)
                                        .map(function (e) {
                                            return e.trim();
                                        })
                                        .filter(Boolean);
                                }
                                return "undefined" != typeof FormData && e instanceof FormData
                                       ? Array.from(e.keys())
                                       : "object" !== a(e) || Array.isArray(e)
                                         ? []
                                         : Object.keys(e);
                            })(_),
                            x = (function (e) {
                                try {
                                    return new URL(e || "", window.location.href).pathname;
                                } catch (e) {
                                    return "";
                                }
                            })(g),
                            P = (Array.isArray(null == p ? void 0 : p.rules) ? p.rules : []).find(function (e) {
                                return (
                                    y(null == e ? void 0 : e.host, S) &&
                                    y(null == e ? void 0 : e.path, x) &&
                                    y(s(null == e ? void 0 : e.method), h) &&
                                    v(null == e ? void 0 : e.query, T) &&
                                    v(null == e ? void 0 : e.body, R)
                                );
                            });
                        if (!P) return {type: d.PASS};
                        var E =
                            null === (m = window) ||
                            void 0 === m ||
                            null === (c = m.SSR_RENDER_DATA) ||
                            void 0 === c ||
                            null === (l = c.app) ||
                            void 0 === l ||
                            null === (u = l.odin) ||
                            void 0 === u
                            ? void 0
                            : u.user_id;
                        return {
                            type: d.REPORT_ONLY,
                            key: [S, h, x, (null == P ? void 0 : P.ruleName) || "default"].join("::"),
                            report: !0,
                            bid: "argus_security_custom",
                            payload: {uid: E, host: S, method: h, queryKeys: T, bodyKeys: R, matchedRule: P},
                        };
                    },
                },
                config: {
                    rules: [
                        {
                            ruleName: "用户关注",
                            host: "www.douyin.com",
                            method: "POST",
                            query: ["*"],
                            body: ["*"],
                            path: "/aweme/v1/web/commit/follow/user/",
                        },
                        {
                            ruleName: "用户关注",
                            host: "www-hj.douyin.com",
                            method: "POST",
                            query: ["*"],
                            body: ["*"],
                            path: "/aweme/v1/web/commit/follow/user/",
                        },
                        {
                            ruleName: "评论",
                            host: "www.douyin.com",
                            method: "POST",
                            query: ["*"],
                            body: ["*"],
                            path: "/aweme/v1/web/comment/publish",
                        },
                        {
                            ruleName: "评论",
                            host: "www-hj.douyin.com",
                            method: "POST",
                            query: ["*"],
                            body: ["*"],
                            path: "/aweme/v1/web/comment/publish",
                        },
                        {
                            ruleName: "点赞",
                            host: "www.douyin.com",
                            method: "POST",
                            query: ["*"],
                            body: ["*"],
                            path: "/aweme/v1/web/commit/item/digg/",
                        },
                        {
                            ruleName: "点赞",
                            host: "www-hj.douyin.com",
                            method: "POST",
                            query: ["*"],
                            body: ["*"],
                            path: "/aweme/v1/web/commit/item/digg/",
                        },
                        {
                            ruleName: "收藏",
                            host: "www.douyin.com",
                            method: "POST",
                            query: ["*"],
                            body: ["*"],
                            path: "/aweme/v1/web/aweme/collect/",
                        },
                        {
                            ruleName: "收藏",
                            host: "www-hj.douyin.com",
                            method: "POST",
                            query: ["*"],
                            body: ["*"],
                            path: "/aweme/v1/web/aweme/collect/",
                        },
                        {
                            ruleName: "评论点赞",
                            host: "www.douyin.com",
                            method: "POST",
                            query: ["*"],
                            body: ["*"],
                            path: "/aweme/v1/web/comment/digg",
                        },
                        {
                            ruleName: "评论点赞",
                            host: "www-hj.douyin.com",
                            method: "POST",
                            query: ["*"],
                            body: ["*"],
                            path: "/aweme/v1/web/comment/digg",
                        },
                        {
                            ruleName: "作品推荐",
                            host: "www.douyin.com",
                            method: "POST",
                            query: ["*"],
                            body: ["*"],
                            path: "/aweme/v1/web/familiar/recommend/submit",
                        },
                        {
                            ruleName: "作品推荐",
                            host: "www-hj.douyin.com",
                            method: "POST",
                            query: ["*"],
                            body: ["*"],
                            path: "/aweme/v1/web/familiar/recommend/submit",
                        },
                        {
                            ruleName: "作品举报",
                            host: "www.douyin.com",
                            method: "POST",
                            query: ["*"],
                            body: ["*"],
                            path: "/aweme/v1/report/submit/",
                        },
                        {
                            ruleName: "作品举报",
                            host: "www-hj.douyin.com",
                            method: "POST",
                            query: ["*"],
                            body: ["*"],
                            path: "/aweme/v1/report/submit/",
                        },
                    ],
                },
            },
            monitor: {
                body: {version: "1.0.0", key: "report", name: "上报配置策略"},
                config: {bid: "douyin_web", sampleRatio: 1e4},
            },
            report: {
                body: {version: "1.0.0", key: "report", name: "上报配置策略"},
                config: {bid: "douyin_web", sampleRatio: 1e4},
            },
            envVarDetect: {
                body: {
                    version: "1.0.0",
                    key: "envVarDetect",
                    name: "环境变量检测",
                    condition: "",
                    expression: function (e) {
                        var t = window.use("strategy").strategy.envVarDetect.config,
                            o = t.envVars || [],
                            a = Boolean(t.block),
                            r = o.filter(function (e) {
                                return void 0 !== window[e];
                            });
                        return 0 === r.length
                               ? {type: "PASS"}
                               : {
                                type: a ? "BLOCK" : "REPORT_ONLY",
                                key: r.join(","),
                                once: !0,
                                report: !0,
                                payload: {matched: r}
                            };
                    },
                },
                config: {envVars: ["sxl_info", "sxl_enter", "sxl_fans", "sxl_feed"], block: !1},
            },
            csrfWebToken: {
                body: {
                    version: "1.0.0",
                    key: "csrfWebToken",
                    name: "CSRF前端Token防护",
                    condition: "",
                    expression: function (e) {
                        var t,
                            o = window.use("strategy").strategy.csrfWebToken.config,
                            a = o.protectedHost,
                            r = o.allowedHost,
                            i = SDKRuntime.require("ActionType"),
                            w = e.payload,
                            m = w.context,
                            c = w.method || (null === (t = m._xhr_open_args) || void 0 === t ? void 0 : t.method);
                        if (!c) return {type: i.PASS, payload: {}};
                        var l = (e.payload.context._xhr_open_args || e.payload).url,
                            u = new URL(l, window.location.href),
                            d = "".concat(c, ": ").concat(u.host, "/").concat(u.pathname);
                        return r && n(r, u.host, c, u.pathname)
                               ? {type: i.REPORT_ONLY, key: d, once: !0, payload: {}}
                               :
                            {type: n(a, u.host, c, u.pathname) ? i.REWRITE : i.PASS, key: d, once: !0, payload: {}};
                    },
                },
                config: {
                    protectedHost: {
                        "www.douyin.com": {
                            POST: "*",
                            GET: [
                                "/aweme/v1/web/douyin/select/study/ai_assistant/note/delete",
                                "/web/api/creator/school/collect/",
                                "/aweme/v1/web/recommend/user/dislike/",
                                "/aweme/v1/web/danmaku/get_v2/",
                                "/aweme/v1/web/danmaku/digg/",
                                "/aweme/v1/web/ocpc/write/",
                                "/aweme/v1/web/danmaku/conf/get/",
                                "/web_shorten/",
                                "/aweme/v1/web/address/getlist/",
                                "/aweme/v1/web/ecom/warcraft/api/coupon/couponlist/v2/",
                                "/aweme/v1/web/im/user/active/update/",
                            ],
                        },
                        "so-landing.douyin.com": {
                            POST: ["/douyin/select/v1/ai/history_delete/"],
                            GET: ["/douyin/select/v1/ai/history_delete/"],
                        },
                        "www-hj.douyin.com": {
                            POST: "*",
                            GET: [
                                "/web/api/creator/school/collect/",
                                "/aweme/v1/web/recommend/user/dislike/",
                                "/aweme/v1/web/danmaku/get_v2/",
                                "/aweme/v1/web/danmaku/digg/",
                                "/aweme/v1/web/ocpc/write/",
                                "/aweme/v1/web/danmaku/conf/get/",
                                "/web_shorten/",
                                "/aweme/v1/web/address/getlist/",
                                "/aweme/v1/web/ecom/warcraft/api/coupon/couponlist/v2/",
                                "/aweme/v1/web/im/user/active/update/",
                            ],
                        },
                        "live.douyin.com": {
                            GET: [
                                "/webcast/fansclub/participate/",
                                "/webcast/web/enter/",
                                "/webcast/room/web/enter/",
                                "/webcast/web/home/",
                                "/webcast/web/leave/",
                                "/webcast/room/info_by_scene/",
                                "/webcast/web/partition/detail/header/",
                                "/webcast/user/",
                                "/webcast/user/me/",
                                "/webcast/review/report_user_reason/",
                                "/webcast/room/get_report_chat_reasons/",
                                "/webcast/room/report_chat/",
                                "/webcast/web/more_live/",
                                "/webcast/gift/extra/",
                                "/aweme/v1/web/address/getlist/",
                            ],
                            POST: [
                                "/webcast/lottery/melon/update_user_condition/",
                                "/webcast/room/dislike/",
                                "/webcast/lottery/melon/lottery_info/",
                                "/webcast/props/consume/",
                                "/webcast/room/web/enter/",
                                "/webcast/lottery/melon/update_user_extra_info/",
                                "/webcast/linkmic_audience/invite/",
                                "/webcast/fansclub/participate/",
                                "/webcast/user/relation/update/",
                                "/aweme/v1/web/user/block/",
                                "/aweme/v1/web/notice/del/",
                                "/aweme/v1/fancy/qrcode/info/",
                                "/webcast/user/report/commit/",
                                "/webcast/gift/send/",
                                "/aweme/v1/web/privacy/batch_convert_image",
                                "/aweme/v1/web/privacy/batch_build_image",
                                "/activity/sjb/webcast/",
                                "/aweme/v1/web/address/report/",
                                "/aweme/v1/web/address/save/",
                                "/aweme/v1/web/address/disable/",
                            ],
                        },
                    },
                    allowedHost: {},
                },
            },
            webSign: {
                body: {
                    version: "1.0.0",
                    key: "webSign",
                    name: "接口加签防护",
                    condition: "",
                    expression: function (e) {
                        var t,
                            o = window.use("strategy").strategy.webSign.config,
                            a = o.protectedHost,
                            r = o.allowedHost,
                            i = SDKRuntime.require("ActionType"),
                            w = e.payload,
                            m = w.context,
                            c = w.method || (null === (t = m._xhr_open_args) || void 0 === t ? void 0 : t.method);
                        if (!c) return {type: i.PASS, payload: {}};
                        var l = (e.payload.context._xhr_open_args || e.payload).url,
                            u = new URL(l, window.location.href),
                            d = "".concat(c, ": ").concat(u.host, "/").concat(u.pathname);
                        return r && n(r, u.host, c, u.pathname)
                               ? {type: i.PASS, key: d, once: !0, payload: {}}
                               : {
                                type: n(a, u.host, c, u.pathname) ? i.REWRITE : i.PASS,
                                key: d,
                                once: !0,
                                payload: {url: l}
                            };
                    },
                },
                config: {
                    protectedHost: {
                        "www.douyin.com": {
                            POST: [
                                "/aweme/v1/web/aweme/detail/",
                                "/aweme/v1/web/aweme/post/",
                                "/aweme/v1/web/aweme/favorite/",
                                "/aweme/v1/web/aweme/listcollection/",
                                "/aweme/v1/web/mix/aweme/",
                                "/aweme/v1/web/tab/feed/",
                            ],
                            GET: [
                                "/aweme/v1/web/aweme/detail/",
                                "/aweme/v1/web/aweme/post/",
                                "/aweme/v1/web/aweme/favorite/",
                                "/aweme/v1/web/aweme/listcollection/",
                                "/aweme/v1/web/mix/aweme/",
                                "/aweme/v1/web/tab/feed/",
                                "/aweme/v1/web/mix/list/",
                                "/aweme/v1/web/music/aweme/",
                                "/aweme/v1/web/music/list/",
                                "/aweme/v1/web/mix/detail/",
                                "/aweme/v1/web/mix/listcollection/",
                                "/aweme/v1/web/music/detail/",
                                "/aweme/v1/web/collects/list/",
                                "/aweme/v1/web/collects/video/list/",
                            ],
                        },
                        "www-hj.douyin.com": {
                            POST: [
                                "/aweme/v1/web/aweme/detail/",
                                "/aweme/v1/web/aweme/post/",
                                "/aweme/v1/web/aweme/favorite/",
                                "/aweme/v1/web/aweme/listcollection/",
                                "/aweme/v1/web/mix/aweme/",
                                "/aweme/v1/web/tab/feed/",
                            ],
                            GET: [
                                "/aweme/v1/web/aweme/detail/",
                                "/aweme/v1/web/aweme/post/",
                                "/aweme/v1/web/aweme/favorite/",
                                "/aweme/v1/web/aweme/listcollection/",
                                "/aweme/v1/web/mix/aweme/",
                                "/aweme/v1/web/tab/feed/",
                                "/aweme/v1/web/mix/list/",
                                "/aweme/v1/web/music/aweme/",
                                "/aweme/v1/web/music/list/",
                                "/aweme/v1/web/mix/detail/",
                                "/aweme/v1/web/mix/listcollection/",
                                "/aweme/v1/web/music/detail/",
                                "/aweme/v1/web/collects/list/",
                                "/aweme/v1/web/collects/video/list/",
                            ],
                        },
                    },
                    allowedHost: {},
                },
            },
            cancelDigg: {
                body: {
                    version: "1.0.0",
                    key: "cancelDigg",
                    name: "取消点赞",
                    condition: "",
                    expression: function (e) {
                        var a,
                            r = window.use("strategy").strategy.cancelDigg.config,
                            i = r.protectedHost,
                            w = r.allowedHost,
                            m = SDKRuntime.require("ActionType"),
                            c = e.payload,
                            l = c.context,
                            u = c.method || (null === (a = l._xhr_open_args) || void 0 === a ? void 0 : a.method);
                        if (!u) return {type: m.PASS, payload: {}};
                        var d = (e.payload.context._xhr_open_args || e.payload).url,
                            s = new URL(d, window.location.href),
                            y = "".concat(u, ": ").concat(s.host, "/").concat(s.pathname);
                        if (w && n(w, s.host, u, s.pathname)) return {
                            type: m.REPORT_ONLY,
                            key: y,
                            once: !0,
                            payload: {}
                        };
                        if (n(i, s.host, u, s.pathname)) {
                            var v,
                                b,
                                p,
                                f,
                                h,
                                g =
                                    null === (v = window) ||
                                    void 0 === v ||
                                    null === (b = v.SSR_RENDER_DATA) ||
                                    void 0 === b ||
                                    null === (p = b.app) ||
                                    void 0 === p ||
                                    null === (f = p.odin) ||
                                    void 0 === f
                                    ? void 0
                                    : f.user_id,
                                _ = {},
                                S = t((e.payload.args[0] || "").split("&"));
                            try {
                                for (S.s(); !(h = S.n()).done;) {
                                    var T = o(h.value.split("="), 2),
                                        R = T[0],
                                        x = T[1];
                                    _[R] = x;
                                }
                            } catch (e) {
                                S.e(e);
                            } finally {
                                S.f();
                            }
                            if (0 === Number(_.type))
                                return {
                                    type: m.REPORT_ONLY,
                                    key: y,
                                    bid: "argus_security_custom",
                                    payload: {uid: g, aweme_id: _.aweme_id || ""},
                                };
                        }
                        return {type: m.PASS, payload: {}};
                    },
                },
                config: {
                    protectedHost: {
                        "www.douyin.com": {POST: ["/aweme/v1/web/commit/item/digg/"], GET: []},
                        "www-hj.douyin.com": {POST: ["/aweme/v1/web/commit/item/digg/"], GET: []},
                    },
                    allowedHost: {},
                },
            },
            diggParams: {
                body: {
                    version: "1.0.0",
                    key: "diggParams",
                    name: "点赞参数",
                    condition: "",
                    expression: function (e) {
                        var a,
                            r = window.use("strategy").strategy.diggParams.config,
                            i = r.protectedHost,
                            w = r.allowedHost,
                            m = SDKRuntime.require("ActionType"),
                            c = e.payload,
                            l = c.context,
                            u = c.method || (null === (a = l._xhr_open_args) || void 0 === a ? void 0 : a.method);
                        if (!u) return {type: m.PASS, payload: {}};
                        var d = (e.payload.context._xhr_open_args || e.payload).url,
                            s = new URL(d, window.location.href),
                            y = "".concat(u, ": ").concat(s.host, "/").concat(s.pathname);
                        if (w && n(w, s.host, u, s.pathname)) return {
                            type: m.REPORT_ONLY,
                            key: y,
                            once: !0,
                            payload: {}
                        };
                        if (n(i, s.host, u, s.pathname)) {
                            var v,
                                b,
                                p,
                                f,
                                h,
                                g =
                                    null === (v = window) ||
                                    void 0 === v ||
                                    null === (b = v.SSR_RENDER_DATA) ||
                                    void 0 === b ||
                                    null === (p = b.app) ||
                                    void 0 === p ||
                                    null === (f = p.odin) ||
                                    void 0 === f
                                    ? void 0
                                    : f.user_id,
                                _ = {},
                                S = t((e.payload.args[0] || "").split("&"));
                            try {
                                for (S.s(); !(h = S.n()).done;) {
                                    var T = o(h.value.split("="), 2),
                                        R = T[0],
                                        x = T[1];
                                    _[R] = x;
                                }
                            } catch (e) {
                                S.e(e);
                            } finally {
                                S.f();
                            }
                            return {
                                type: m.REWRITE,
                                key: y,
                                bid: "argus_security_custom",
                                payload: {uid: g, aweme_id: _.aweme_id || _.user_id || _.item_id || ""},
                            };
                        }
                        return {type: m.PASS, payload: {}};
                    },
                },
                config: {
                    protectedHost: {
                        "www.douyin.com": {
                            POST: [
                                "/aweme/v1/web/commit/item/digg/",
                                "/aweme/v1/web/commit/follow/user/",
                                "/aweme/v1/web/comment/publish",
                                "/aweme/v1/web/aweme/collect/",
                                "/aweme/v1/web/comment/digg",
                                "/aweme/v1/web/familiar/recommend/submit",
                                "/aweme/v1/report/submit/",
                            ],
                        },
                        "www-hj.douyin.com": {
                            POST: [
                                "/aweme/v1/web/commit/item/digg/",
                                "/aweme/v1/web/commit/follow/user/",
                                "/aweme/v1/web/comment/publish",
                                "/aweme/v1/web/aweme/collect/",
                                "/aweme/v1/web/comment/digg",
                                "/aweme/v1/web/familiar/recommend/submit",
                                "/aweme/v1/report/submit/",
                            ],
                        },
                    },
                    allowedHost: {},
                },
            },
        },
        execution: {
            SDK_INIT: "executeSDKInit",
            XHR_REQUEST_OPEN: "executeXHRRequestOpen",
            XHR_REQUEST_SEND: "executeXHRRequestSend",
            FETCH_REQUEST: "executeFetchRequest",
        },
    });
});
