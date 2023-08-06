
let enableCheck = document.getElementById('changeState');


chrome.storage.sync.get('immersion_enabled', function(data) {
  is_enabled = data['immersion_enabled'] || false
  enableCheck.checked = is_enabled
});
console.log("Test root")

enableCheck.onchange = function(element) {
  console.log("Test checked")
  chrome.storage.sync.get('immersion_enabled', function(data) {
    is_enabled = data['immersion_enabled'] || false
    chrome.storage.sync.set({"immersion_enabled": !is_enabled}, function() {
      console.log('immersion state changed');
    });
    //reload page
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.update(tabs[0].id, {url: tabs[0].url});
    });
  });
};
