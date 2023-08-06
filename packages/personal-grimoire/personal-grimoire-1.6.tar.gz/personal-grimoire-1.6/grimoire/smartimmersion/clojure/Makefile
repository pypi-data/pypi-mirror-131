develop:
	clojure -A:fig:build
.PHONY: develop

release:
	clojure -m cljs.main -co build.edn --optimizations advanced  -c colorpicker.core
	cp -rf out/main.js ../chrome-extension/run.js

.PHONY: release
