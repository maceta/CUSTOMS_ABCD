odoo.define('st_ecommerce_theme.systray.install', function (require) {
"use strict";
console.log("Service Worker called");
if ('serviceWorker' in navigator) {
    console.log("serviceWorker in navigator found");
    navigator.serviceWorker.register('/portal-service-worker.js')
        .catch(function (reg) {
          console.log('Service worker registered.', reg);
        });
}
else{
    console.log("No serviceWorker in navigator");
}

});
