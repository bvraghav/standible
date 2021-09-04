(use-modules (ice-9 ftw))
(use-modules (srfi srfi-1))

;; Randomize
(set! *random-state* (random-state-from-platform))

(define SEP #\+)

(define (random-keys n prefix)
  (let* ((!dot-file? (lambda (key)
                       (not (string-prefix? "." key))))
         (keys (scandir prefix !dot-file?))
         (*keys (lambda (i)
                  (list-ref keys i)))
         ;; (random-indices
         ;;  (when (< n (length keys))
         ;;    (list-tabulate
         ;;     n
         ;;     (lambda _ (random (length keys))))))
	 (random-indices
	  (list-tabulate
	   n
	   (lambda _ (random (length keys))))))
    ;; (if (pair? random-indices)
    ;;     (map *keys random-indices)
    ;;     keys)
    (map *keys random-indices)))

;; (random-keys 8 "/nfs/151/gpu/raghav/data/shadegan/data-single/renders")


(define (random-frame prefix render-key style)
  (let* ((render-folder (format #f "~a/~a/r_~a"
                                prefix
                                render-key
                                style))
         (!dot-file? (lambda (name)
                       (not (string-prefix? "." name))))
         (frames (scandir render-folder !dot-file?))
         (random-index (random (length frames))))
    (list-ref frames random-index)))

;; (random-frame "/nfs/151/gpu/raghav/data/shadegan/data-single/renders" "fc1a2579" "contour")

(define (random-key-frame-pairs n prefix . rest)
  (let* ((style (if (pair? rest) (car rest) "contour"))
         (keys (random-keys n prefix))
         (frame< (lambda (key)
                   (random-frame prefix key style)))
         (key-frame-pair (lambda (key frame)
                           (format #f "~a~c~a"
                                   key SEP frame))))
    (map key-frame-pair
         keys
         (map frame< keys))))

(define (all-images prefix k+f-pair style+)
  (let* ((key (car (string-split k+f-pair SEP)))
         (frame (cadr (string-split k+f-pair SEP)))
         (styles (filter (lambda (x) (not (string-null? x)))
                         (string-split style+ #\space))))
    (map (lambda (style)
           (format #f "~a/~a/r_~a/~a"
                   prefix key style frame))
         styles)))
