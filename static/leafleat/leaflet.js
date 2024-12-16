/*!
 * Leaflet 1.7.1, https://leafletjs.com
 * (c) 2010-2020 Vladimir Agafonkin, (c) 2010-2011 CloudMade
 */

(function (global, factory) {
  typeof exports === "object" && typeof module !== "undefined"
    ? factory(exports)
    : typeof define === "function" && define.amd
    ? define(["exports"], factory)
    : ((global = typeof globalThis !== "undefined" ? globalThis : global || self), factory((global.L = {})));
})(this, function (exports) {
  "use strict";

  // Leaflet code goes here.
  // For simplicity, this example uses a placeholder.
  // Visit https://leafletjs.com/download.html for the full source.

  // Add initialization and utility code for creating Leaflet maps.
  exports.map = function (id, options) {
    return new Map(id, options);
  };

  exports.tileLayer = function (url, options) {
    return new TileLayer(url, options);
  };

  exports.geoJSON = function (geojson, options) {
    return new GeoJSON(geojson, options);
  };

  // Other Leaflet functionality...
});
