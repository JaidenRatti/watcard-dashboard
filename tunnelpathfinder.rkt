;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-reader.ss" "lang")((modname |graph testing|) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #t)))
(require graph)
(require racket/gui/base)

(define g (unweighted-graph/undirected
           '((EV2 PAS)
             (EV2 EV3)
             (EV2 EV1)
             (EV1 HH)
             (EV1 AL)
             (AL ML)
             (AL TC)
             (TC SCH)
             (NH STC)
             (DP ())
             (GH ())
             (OPT ())
             (CIF ())
             (STC B2)
             (STC B1)
             (B2 B1)
             (B2 QNC)
             (B1 ESC)
             (QNC MC)
             (ESC C2)
             (ESC EIT)
             (MC C2)
             (MC DC)
             (MC M3)
             (MC SLC)
             (DC EIT)
             (SLC PAC)
             (EXP LHI)
             (LHI BMH)
             (BMH EXP)
             (EIT E3)
             (E3 E5)
             (E5 E7)
             (E7 E6)
             (E3 E2)
             (EIT PHYS)
             (PHYS E2)
             (E2 CPH)
             (CPH DWE)
             (DWE RCH)
             (DWE E2)
             (E2 RCH)
             )))

(cc g)
;; returns connected components of graph
(dijkstra g 'SCH)
;; returns number of edges between building and all others
;; pretty much bfs since no weights*
;;
;; * distances between connected buildings are insignificant => no weights
(fewest-vertices-path g 'QNC 'E3)
;; uses bfs to return the shortest path in order
;; sample output: (list 'QNC 'MC 'DC 'EIT)

;; will manually recreate fewest-vertices-path

