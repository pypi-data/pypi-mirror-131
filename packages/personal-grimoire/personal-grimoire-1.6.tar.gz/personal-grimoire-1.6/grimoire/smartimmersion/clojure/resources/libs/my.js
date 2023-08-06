

var my = {
    isElementVisible: function (el) {
        var rect     = el.getBoundingClientRect(),
            vWidth   = window.innerWidth || document.documentElement.clientWidth,
            vHeight  = window.innerHeight || document.documentElement.clientHeight,
            efp      = function (x, y) { return document.elementFromPoint(x, y) };

        // Return false if it's not in the viewport
        if (rect.right < 0 || rect.bottom < 0
                || rect.left > vWidth || rect.top > vHeight)
            return false;

        // Return true if any of its four corners are visible
        return (
              el.contains(efp(rect.left,  rect.top))
          ||  el.contains(efp(rect.right, rect.top))
          ||  el.contains(efp(rect.right, rect.bottom))
          ||  el.contains(efp(rect.left,  rect.bottom))
        );
    },
    immersionEnabled: function(callback) {
        if (!chrome.storage) {
            console.log("Chrome storage not available, starting immersion nevertheless")
            callback()
            return
        }

         chrome.storage.sync.get('immersion_enabled', function(data) {
             console.log("Immersion storage: ", data)
             if (!data['immersion_enabled']) {
                 console.log("Immersion is not enabled")
                 return
             } else {
                 console.log("Immersion is enabled")
                 callback()
             }
         })
    }
};


module.exports = my;
