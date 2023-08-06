
(ns ^:figwheel-hooks colorpicker.core
  (:require [cljs.core.async :refer [<!]]
            [cljs-http.client :as http]
            [reagent.core :as r]
            [reagent.dom :as rdom]
            [goog.dom :as gdom]
            [clojure.browser.dom :as dom]
            [my]
            )
  (:require-macros [cljs.core.async.macros :refer [go]])

            )

(enable-console-print!)
(defonce global-state (r/atom {:selectedtext "No selected text"
                               :translatedselection "No selected text"
                               :menuopened false
                               :mouseX 0
                               :mouseY 0}))

(def translated-background-color "#e4fde1")


(defn get-all-paragraphs []
  (array-seq (js/document.getElementsByTagName "p"))
)

(defn translate-paragraph [paragraph]
(go ( let [response (<! (http/get (str "http://localhost:5007/translate?q=" (.-innerText paragraph)) {:with-credentials? false}))]
      ; (println (str "Response: "(:body response)))
      (set! (.-innerText paragraph) (:body response))
      ;(set! (.-style paragraph) (str "background-color:" translated-background-color))
      paragraph
      ))
)

(defn translate-back [sentence]
  (let [ s @global-state ]
    (if (> (count sentence) 3) [(go ( let [response (<! (http/get (str "http://localhost:5007/translate_back?q=" sentence) {:with-credentials? false}))]
        (println (str "Response: "(:body response)))
        (swap! global-state assoc :translatedselection (:body response))
        (swap! global-state update :menuopened not)
        ))] [

       (swap! global-state assoc :translatedselection "No selection")
       (swap! global-state assoc :menuopened false)
                                             ])
  )
)
(defn translate-visible []
  (let [visible-paragraphs (filter my/isElementVisible not-translated-paragraphs)]
  (doall (map translate-paragraph visible-paragraphs))
  (set! not-translated-paragraphs (remove (set visible-paragraphs) not-translated-paragraphs))
  ))


(defn start-immersion []
  ;initialize stuff
  (def my-container (gdom/createElement "div"))
  (gdom/append (get-body) my-container)
  (rdom/render [my-react-container] my-container)


  ;start immersion
  (def ^:dynamic not-translated-paragraphs (get-all-paragraphs))
  (set! (.-onscroll js/window) translate-visible)
 )


(defn get-body[]
  (first (js/document.getElementsByTagName "body"))
  )


(defn menu-entry[text]
  [:li {:class 'menu-option'  :style {
                                      :font-weight "500"
                                      :font-size "14px"
                                      :padding "10px 40px 10px 20px"
                                      :cursor "pointer"
                                      }} text]
  )

(defn render-menu[]
  (let [ s @global-state ]
    (if (:menuopened s) [:div {
                                :style {
                                         :width 240
                                         :z-index 1000
                                         :position "absolute"
                                         :border "1px solid blue"
                                         :backgroundColor "white"
                                         :box-shadow "0 4px 5px 3px rgba(0, 0, 0, 0.2)"
                                         :left (str (:mouseX s) "px")
                                         :top (str (:mouseY s) "px")
                                         :display "block"
                                         }
                                }
                          [:ul {:class 'menu-options' :style {
                                                               :padding "0 0"
                                                               :list-style "none"

                                                               }}
                           (menu-entry (:translatedselection s))
                         ]
                         ] [:div
                               ])

    ))

(defn my-react-container []
  (let [s @global-state]
  [:div
   (render-menu)
  ])
)

(defn handle-menu-toggle[e]
  (.preventDefault e)
  (print "Menu toggle" (:menuopened @global-state))
  (print (str "Selected text" (js/window.getSelection)))
  (print (str "Mouse position: X " (.-pageX e) " Y " (.-pageY e)))
  (swap! global-state assoc :selectedtext (str (js/window.getSelection)))
  (swap! global-state assoc :mouseX (.-pageX e))
  (swap! global-state assoc :mouseY (.-pageY e))
  (translate-back (:selectedtext @global-state))
)

(defn on-load-handler []
  (println "On load detected on clojure")

  (set! (.-oncontextmenu js/document) handle-menu-toggle)
  (my/immersionEnabled start-immersion)
)

(set! (.-onload js/window) on-load-handler)
