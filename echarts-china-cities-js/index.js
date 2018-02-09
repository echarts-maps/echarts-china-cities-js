define(["require", "exports"], function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    var version = '0.1.0';
    function load_ipython_extension() {
        console.log("echarts-china-cities-js " + version + " has been loaded");
    }
    exports.load_ipython_extension = load_ipython_extension;
});
