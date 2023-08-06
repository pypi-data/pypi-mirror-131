"use strict";
(self["webpackChunkserialhub"] = self["webpackChunkserialhub"] || []).push([["lib_plugin_js"],{

/***/ "./lib/plugin.js":
/*!***********************!*\
  !*** ./lib/plugin.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./version */ "./lib/version.js");
// Copyright (c) cdr4eelz
// Distributed under the terms of the Modified BSD License.



const EXTENSION_ID = 'serialhub_plugin';
/*
namespace CommandIDs {
  export const connect = 'serialhub:connect'
  export const disconnect = 'serialhub:disconnect'
  export const test = 'serialhub:test'
}
*/
/**
 * The SerialHub plugin.
 */
const serialhubPlugin = {
    id: EXTENSION_ID,
    requires: [_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.IJupyterWidgetRegistry],
    activate: activateWidgetExtension,
    autoStart: true
}; // as unknown as IPlugin<Application<Widget>, void>;
// the "as unknown as ..." typecast above is solely to support JupyterLab 1
// and 2 in the same codebase and should be removed when we migrate to Lumino.
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (serialhubPlugin);
/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app, registry) {
    registry.registerWidget({
        name: _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_NAME,
        version: _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_VERSION,
        exports: _widget__WEBPACK_IMPORTED_MODULE_2__,
    });
}


/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MODULE_VERSION": () => (/* binding */ MODULE_VERSION),
/* harmony export */   "MODULE_NAME": () => (/* binding */ MODULE_NAME)
/* harmony export */ });
// Copyright (c) cdr4eelz
// Distributed under the terms of the Modified BSD License.
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
const MODULE_VERSION = data.version;
/*
 * The current package name.
 */
const MODULE_NAME = data.name;


/***/ }),

/***/ "./lib/webseriallink.js":
/*!******************************!*\
  !*** ./lib/webseriallink.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SerialHubPort": () => (/* binding */ SerialHubPort)
/* harmony export */ });
// Copyright (c) cdr4eelz
// Distributed under the terms of the Modified BSD License.
class SerialHubPort {
    constructor(oldSP) {
        if (oldSP)
            oldSP.disconnect(); //Dispose of prior "port" if passed to us
        this.port = null;
        this.outputStream = null;
        this.outputDone = null;
        //this.inputStream = null;
        //this.inputDone = null;
        this.reader = null;
    }
    async connect(f) {
        let NAV = window.navigator;
        if (!NAV || !NAV.serial)
            return;
        if (this.port) {
            await this.disconnect();
        }
        const filter = { usbVendorId: 0x2047 }; // TI proper ; unused 0x0451 for "TUSB2046 Hub"
        let rawPort = await NAV.serial.requestPort({ filters: [filter] });
        if (!rawPort)
            return;
        this.port = rawPort;
        await this.port.open({ baudRate: 115200 });
        const encoder = new TextEncoderStream();
        this.outputDone = encoder.readable.pipeTo(this.port.writable);
        this.outputStream = encoder.writable;
        //    let decoder = new TextDecoderStream();
        //    this.inputDone = this.port.readable.pipeTo(decoder.writable);
        //    this.inputStream = decoder.readable;
        //    this.reader = this.inputStream.getReader();
        this.reader = this.port.readable.getReader();
        console.log("CONNECT: ", this);
        this.readLoop(f);
    }
    async disconnect() {
        console.log("CLOSE: ", this);
        if (this.reader) {
            await this.reader.cancel();
            this.reader = null;
            //if (this.inputDone) await this.inputDone.catch(() => {});
            //this.inputDone = null;
        }
        if (this.outputStream) {
            await this.outputStream.getWriter().close();
            await this.outputDone;
            this.outputStream = null;
            this.outputDone = null;
        }
        if (this.port) {
            await this.port.close();
            this.port = null;
        }
    }
    writeToStream(...lines) {
        if (!this.outputStream)
            return;
        const writer = this.outputStream.getWriter();
        lines.forEach(line => {
            console.log("[SEND]", line);
            writer.write(line + "\n");
        });
        writer.releaseLock();
    }
    async readLoop(f) {
        while (true) {
            if (!this.reader)
                break;
            const { value, done } = await this.reader.read();
            if (value) {
                console.log("[readLoop] VALUE", value);
                f(value);
            }
            if (done) {
                console.log("[readLoop] DONE", done);
                this.reader.releaseLock();
                break;
            }
        }
    }
    static isSupported() {
        let NAV = window.navigator;
        if (NAV === undefined || NAV === null)
            return false;
        let SER = NAV.serial;
        if (SER === undefined || SER === null)
            return false;
        return true;
    }
    static test(f) {
        let W = window;
        let SER = new SerialHubPort(W.serPort);
        W.serPort = SER;
        SER.connect(f).then(() => {
            console.log(SER);
            SER.writeToStream("1");
        });
        return SER;
    }
}


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SerialHubModel": () => (/* binding */ SerialHubModel),
/* harmony export */   "SerialHubView": () => (/* binding */ SerialHubView)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./version */ "./lib/version.js");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _webseriallink__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./webseriallink */ "./lib/webseriallink.js");
// Copyright (c) cdr4eelz
// Distributed under the terms of the Modified BSD License.


// Import the CSS




class SerialHubModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: SerialHubModel.model_name, _model_module: SerialHubModel.model_module, _model_module_version: SerialHubModel.model_module_version, _view_name: SerialHubModel.view_name, _view_module: SerialHubModel.view_module, _view_module_version: SerialHubModel.view_module_version, isSupported: false, status: 'Initializing...', value: 'Loading...' });
    }
    static get mytempid() {
        return SerialHubModel._mytempid;
    }
}
SerialHubModel._mytempid = _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.uuid();
SerialHubModel.serializers = Object.assign({}, _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetModel.serializers);
SerialHubModel.model_name = 'SerialHubModel';
SerialHubModel.model_module = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_NAME;
SerialHubModel.model_module_version = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_VERSION;
SerialHubModel.view_name = 'SerialHubView'; // Set to null if no view
SerialHubModel.view_module = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_NAME; // Set to null if no view
SerialHubModel.view_module_version = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_VERSION;
class SerialHubView extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetView {
    constructor() {
        super(...arguments);
        this._el_status = null;
        this._el_value = null;
    }
    render() {
        this.el.id = this.id || _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.UUID.uuid4();
        this.el.classList.add('xx-serialhub-widget');
        /* Create a couple sub-Elements for our custom widget */
        this._el_status = window.document.createElement("div");
        this._el_status.classList.add('xx-serialhub-status');
        this._el_value = window.document.createElement("pre");
        this._el_value.classList.add('xx-serialhub-value');
        /* Click events wrapped to capture "this" object */
        this._el_status.onclick = (ev) => this.click_status(ev);
        this._el_value.onclick = (ev) => this.click_value(ev);
        /* Maybe is more appropriate append() function availablie? */
        this.$el.append(this._el_status, this._el_value);
        this.changed_status();
        this.changed_value();
        this.model.on('change:status', this.changed_status, this);
        this.model.on('change:value', this.changed_value, this);
        this.model.on('msg:custom', this.msg_custom, this);
        this.model.set('isSupported', _webseriallink__WEBPACK_IMPORTED_MODULE_3__.SerialHubPort.isSupported());
        this.model.set('status', (_webseriallink__WEBPACK_IMPORTED_MODULE_3__.SerialHubPort.isSupported()) ? 'Supported' : 'Unsupported');
        this.touch();
        return this;
    }
    changed_status() {
        if (!this._el_status)
            return;
        this._el_status.textContent = this.model.get('status');
    }
    changed_value() {
        if (!this._el_value)
            return;
        this._el_value.textContent = this.model.get('value');
    }
    click_status(ev) {
        //console.log(this, arguments, this.model);
        let SHP = _webseriallink__WEBPACK_IMPORTED_MODULE_3__.SerialHubPort.test((value) => {
            console.log(value);
            this.model.send({ 'type': "binary" }, {}, [value]);
        });
        console.log("DONE", SHP);
    }
    click_value(ev) {
        if (!this || !this.model)
            return;
        this.model.send({ 'type': "text", 'text': "DATA\n" }, {}, []);
        window.serPort.writeToStream("6");
    }
    msg_custom(mData, mBuffs) {
        console.log(this, mData, mBuffs);
        let msgType = mData['type'];
        if (msgType == 'text') {
            window.serPort.writeToStream(mData['text']);
        }
    }
}


/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

module.exports = JSON.parse('{"name":"serialhub","version":"0.0.16","description":"WebSerial widget for Jupyter Hub/Lab","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"homepage":"https://github.com/cdr4eelz/serialhub","bugs":{"url":"https://github.com/cdr4eelz/serialhub/issues"},"license":"BSD-3-Clause","author":{"name":"cdr4eelz","email":"1408777+cdr4eelz@users.noreply.github.com"},"files":["lib/**/*.{d.ts,eot,gif,html,jpg,js,js.map,json,png,svg,woff2,ttf}","style/**/*.{css,js,eot,gif,html,jpg,json,png,svg,woff2,ttf}","schema/*.json"],"main":"lib/index.js","types":"lib/index.d.ts","style":"style/index.css","repository":{"type":"git","url":"https://github.com/cdr4eelz/serialhub.git"},"scripts":{"build":"jlpm run build:lib && jlpm run build:labextension:dev","build:prod":"jlpm run clean && jlpm run build:lib && jlpm run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","clean":"jlpm run clean:lib","clean:lib":"rimraf lib tsconfig.tsbuildinfo","clean:labextension":"rimraf serialhub/labextension","clean:all":"jlpm run clean:lib && jlpm run clean:labextension","eslint":"eslint . --ext .ts,.tsx --fix","eslint:check":"eslint . --ext .ts,.tsx","install:extension":"jlpm run build","watch":"run-p watch:src watch:labextension","watch:src":"tsc -w","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^2 || ^3 || ^4","@lumino/coreutils":"^1.11.1","@lumino/widgets":"^1.30.1","@jupyterlab/application":"^3.1.0","@jupyterlab/coreutils":"^5.1.0","@jupyterlab/services":"^6.1.0","@jupyterlab/settingregistry":"^3.1.0"},"devDependencies":{"@jupyterlab/builder":"^3.1.0","@typescript-eslint/eslint-plugin":"^4.8.1","@typescript-eslint/parser":"^4.8.1","eslint":"^7.14.0","eslint-config-prettier":"^6.15.0","eslint-plugin-prettier":"^3.1.4","mkdirp":"^1.0.3","npm-run-all":"^4.1.5","prettier":"^2.1.1","rimraf":"^3.0.2","typescript":"~4.1.3"},"sideEffects":["style/*.css","style/index.js"],"styleModule":"style/index.js","publishConfig":{"access":"public"},"jupyterlab":{"sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}},"discovery":{"server":{"managers":["pip"],"base":{"name":"serialhub"}}},"extension":"lib/plugin","outputDir":"serialhub/labextension"},"jupyter-releaser":{"hooks":{"before-build-npm":["python -m pip install jupyterlab~=3.1","jlpm"]}}}');

/***/ })

}]);
//# sourceMappingURL=lib_plugin_js.83e522c618a7893f0492.js.map