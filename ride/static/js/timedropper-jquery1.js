'use strict';
!function($) {
  /**
   * @param {?} options
   * @param {?} callbackFnk
   * @return {?}
   */
  $.fn.timeDropper = function(options, callbackFnk) {
    return $(this).each(function() {
      var initializeCheckTimer;
      var _td_input = $(this);
      /** @type {boolean} */
      var o = false;
      /** @type {boolean} */
      var supportTouch = false;
      /**
       * @param {number} n
       * @return {?}
       */
      var _td_num = function(n) {
        return n < 10 ? "0" + n : n;
      };
      var _td_id = $(".td-clock").length;
      /** @type {null} */
      var _td_event = null;
      var _td_options = $.extend({
        format : "h:mm a",
        autoswitch : false,
        meridians : false,
        mousewheel : false,
        setCurrentTime : true,
        init_animation : "dropdown",
        quarters : true,
        minutesSteps : false
      }, options);
      _td_input.prop({
        readonly : true
      }).addClass("td-input");
      if (_td_options.minutesSteps) {
        if (![5, 10, 15, 20, 25, 30].includes(_td_options.minutesSteps)) {
          /** @type {boolean} */
          _td_options.minutesSteps = false;
        }
      }
      $("body").append('      <div class="td-wrap td-n2 ' + _td_options.customClass + '" id="td-clock-' + _td_id + '">        <div class="td-overlay"></div>        <div class="td-clock td-init">          <div class="td-medirian">            <span class="td-icon-am td-n">AM</span>            <span class="td-icon-pm td-n">PM</span>          </div>          <div class="td-lancette">            <div></div><div></div>          </div>          <div class="td-quarters"></div>          <div class="td-time">            <span class="on"></span>:<span></span>          </div>          <div class="td-deg td-n">            <div class="td-select">              <svg xmlns="http://www.w3.org/2000/svg" width="95" height="37" viewBox="0 0 95 37"><g fill="none" fill-rule="evenodd" transform="translate(15.775 15.982)"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="30" d="M0 0c9.823 3.873 20.525 6 31.724 6C42.912 6 53.604 3.877 63.42.012"/><circle stroke-width="0" cx="21.225" cy="5.018" r="3" /><circle stroke-width="0" cx="31.225" cy="5.018" r="3" /><circle stroke-width="0" cx="41.225" cy="5.018" r="3" /></g></svg>            </div>          </div>        </div>      </div>      ');
      var _td_container = $("#td-clock-" + _td_id);
      var imgchk = _td_container.find(".td-overlay");
      var _td_c = _td_container.find(".td-clock");
      /** @type {number} */
      var rectangleWidth = -1;
      /** @type {number} */
      var _td_event_deg = 0;
      /** @type {number} */
      var _td_wheel_deg = 0;
      /**
       * @return {undefined}
       */
      var _td_define_deg = function() {
        var newPanel = _td_c.find(".td-time span.on");
        /** @type {number} */
        var whiteRating = parseInt(newPanel.attr("data-id"));
        if (0 == newPanel.index()) {
          /** @type {number} */
          deg = Math.round(360 * whiteRating / 24);
        } else {
          /** @type {number} */
          deg = Math.round(360 * whiteRating / 60);
        }
        /** @type {number} */
        rectangleWidth = -1;
        _td_event_deg = deg;
        _td_wheel_deg = deg;
      };
      /**
       * @param {number} deg
       * @return {undefined}
       */
      var _td_rotation = function(deg) {
        var t = _td_c.find(".td-time span.on");
        var picUid = t.attr("data-id");
        if (!picUid) {
          /** @type {number} */
          picUid = 0;
        }
        /** @type {number} */
        var h = Math.round(24 * deg / 360);
        /** @type {number} */
        var m = Math.round(60 * deg / 360);
        if (24 == h && (h = 0), 60 == m && (m = 0), 0 == t.index() ? (t.attr("data-id", _td_num(h)), _td_options.meridians && (h >= 12 && h < 24 ? (_td_c.find(".td-icon-pm").addClass("td-on"), _td_c.find(".td-icon-am").removeClass("td-on")) : (_td_c.find(".td-icon-am").addClass("td-on"), _td_c.find(".td-icon-pm").removeClass("td-on")), h > 12 && (h = h - 12), 0 == h && (h = 12)), t.text(_td_num(h))) : (_td_options.minutesSteps && m % _td_options.minutesSteps == 0 || !_td_options.minutesSteps) && 
        t.attr("data-id", _td_num(m)).text(_td_num(m)), _td_wheel_deg = deg, _td_c.find(".td-deg").css("transform", "rotate(" + deg + "deg)"), 0 == t.index()) {
          /** @type {number} */
          var r = Math.round(360 * h / 12);
          _td_c.find(".td-lancette div:last").css("transform", "rotate(" + r + "deg)");
        } else {
          if (_td_options.minutesSteps && m % _td_options.minutesSteps == 0 || !_td_options.minutesSteps) {
            _td_c.find(".td-lancette div:first").css("transform", "rotate(" + deg + "deg)");
          }
        }
        var _td_h = _td_c.find(".td-time span:first").attr("data-id");
        var _td_m = _td_c.find(".td-time span:last").attr("data-id");
        if (Math.round(_td_h) >= 12 && Math.round(_td_h) < 24) {
          /** @type {number} */
          h = Math.round(_td_h) - 12;
          /** @type {string} */
          var ampm = "pm";
          /** @type {string} */
          var A = "PM";
        } else {
          /** @type {number} */
          h = Math.round(_td_h);
          /** @type {string} */
          ampm = "am";
          /** @type {string} */
          A = "AM";
        }
        if (0 == h) {
          /** @type {number} */
          h = 12;
        }
        var target = _td_options.format.replace(/\b(H)\b/g, Math.round(_td_h)).replace(/\b(h)\b/g, Math.round(h)).replace(/\b(m)\b/g, Math.round(_td_m)).replace(/\b(HH)\b/g, _td_num(Math.round(_td_h))).replace(/\b(hh)\b/g, _td_num(Math.round(h))).replace(/\b(mm)\b/g, _td_num(Math.round(_td_m))).replace(/\b(a)\b/g, ampm).replace(/\b(A)\b/g, A);
        _td_input.val(target).trigger("change");
      };
      if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        /** @type {boolean} */
        supportTouch = true;
      }
      _td_c.find(".td-time span").on("click", function(canCreateDiscussions) {
        var $item = $(this);
        _td_c.find(".td-time span").removeClass("on");
        $item.addClass("on");
        /** @type {number} */
        var whiteRating = parseInt($item.attr("data-id"));
        if (0 == $item.index()) {
          /** @type {number} */
          deg = Math.round(360 * whiteRating / 24);
          if (_td_options.minutesSteps) {
            _td_c.find(".td-quarters").removeClass("td-show");
          }
        } else {
          /** @type {number} */
          deg = Math.round(360 * whiteRating / 60);
          if (_td_options.minutesSteps) {
            _td_c.find(".td-quarters").addClass("td-show");
          }
        }
        /** @type {number} */
        rectangleWidth = -1;
        _td_event_deg = deg;
        _td_wheel_deg = deg;
        _td_rotation(deg);
      });
      _td_c.find(".td-deg").on("touchstart mousedown", function(event) {
        _td_define_deg();
        event.preventDefault();
        clearInterval(initializeCheckTimer);
        _td_c.find(".td-deg").removeClass("td-n");
        _td_c.find(".td-select").removeClass("td-rubber");
        /** @type {boolean} */
        o = true;
        var dx;
        var diffX;
        var width;
        var deg;
        var anchorBoundingBoxViewport = _td_c.offset();
        var startX = anchorBoundingBoxViewport.top + _td_c.height() / 2;
        var curX = anchorBoundingBoxViewport.left + _td_c.width() / 2;
        /** @type {number} */
        var i = 180 / Math.PI;
        _td_c.removeClass("td-rubber");
        $(window).on("touchmove mousemove", function(event) {
          if (1 == o) {
            move = supportTouch ? event.originalEvent.touches[0] : event;
            /** @type {number} */
            dx = startX - move.pageY;
            /** @type {number} */
            diffX = curX - move.pageX;
            if ((width = Math.atan2(dx, diffX) * i) < 0) {
              /** @type {number} */
              width = 360 + width;
            }
            if (-1 == rectangleWidth) {
              /** @type {number} */
              rectangleWidth = width;
            }
            if ((deg = Math.floor(width - rectangleWidth + _td_event_deg)) < 0) {
              /** @type {number} */
              deg = 360 + deg;
            } else {
              if (deg > 360) {
                /** @type {number} */
                deg = deg % 360;
              }
            }
            _td_rotation(deg);
          }
        });
      });
      if (_td_options.mousewheel) {
        _td_c.on("mousewheel", function(event) {
          event.preventDefault();
          _td_c.find(".td-deg").removeClass("td-n");
          if (event.originalEvent.wheelDelta > 0) {
            if (_td_wheel_deg <= 360) {
              if (event.originalEvent.wheelDelta <= 120) {
                _td_wheel_deg++;
              } else {
                if (event.originalEvent.wheelDelta > 120) {
                  _td_wheel_deg = _td_wheel_deg + 20;
                }
              }
              if (_td_wheel_deg > 360) {
                /** @type {number} */
                _td_wheel_deg = 0;
              }
            }
          } else {
            if (_td_wheel_deg >= 0) {
              if (event.originalEvent.wheelDelta >= -120) {
                _td_wheel_deg--;
              } else {
                if (event.originalEvent.wheelDelta < -120) {
                  /** @type {number} */
                  _td_wheel_deg = _td_wheel_deg - 20;
                }
              }
              if (_td_wheel_deg < 0) {
                /** @type {number} */
                _td_wheel_deg = 360;
              }
            }
          }
          /** @type {number} */
          rectangleWidth = -1;
          _td_event_deg = _td_wheel_deg;
          _td_rotation(_td_wheel_deg);
        });
      }
      $(document).on("touchend mouseup", function() {
        if (o) {
          /** @type {boolean} */
          o = false;
          if (_td_options.autoswitch) {
            _td_c.find(".td-time span").toggleClass("on");
            _td_c.find(".td-time span.on").click();
          }
          _td_c.find(".td-deg").addClass("td-n");
          _td_c.find(".td-select").addClass("td-rubber");
        }
      });
      /**
       * @param {?} toggle_callback
       * @return {undefined}
       */
      var init = function(toggle_callback) {
        var a;
        var url;
        /** @type {!Date} */
        var ddate = new Date;
        var $this = _td_c.find(".td-time span:first");
        var $item = _td_c.find(".td-time span:last");
        if (_td_options.minutesSteps) {
          _td_c.find(".td-quarters").empty();
          /** @type {number} */
          var dmg = parseInt(60 / _td_options.minutesSteps);
          /** @type {number} */
          var td_ = 0;
          /** @type {number} */
          var mostHPDone = 1;
          for (; mostHPDone <= dmg; mostHPDone++) {
            /** @type {number} */
            var b = Math.round(360 * td_ / 60);
            _td_c.find(".td-quarters").append('<div class="td-quarter" data-id="' + td_ + '" style="transform: rotate(' + b + 'deg)"><div class="td-quarter-bullet"></div></div>');
            td_ = td_ + _td_options.minutesSteps;
          }
          /** @type {boolean} */
          var data = false;
          _td_c.find(".td-quarter-bullet").hover(function() {
            data = _td_c.find(".td-time span:last").html();
            _td_c.find(".td-time span:last").html($(this).closest(".td-quarter").attr("data-id"));
            $(this).addClass("td-on");
          }, function() {
            _td_c.find(".td-time span:last").html(data);
            $(this).removeClass("td-on");
          });
          _td_c.find(".td-quarter").on("click", function(canCreateDiscussions) {
            var $oElemDragged = $(this);
            /** @type {number} */
            var tmp = parseInt($oElemDragged.attr("data-id"));
            /** @type {number} */
            data = tmp;
            /** @type {number} */
            deg = Math.round(360 * tmp / 60);
            /** @type {number} */
            rectangleWidth = -1;
            /** @type {number} */
            _td_event_deg = deg;
            /** @type {number} */
            _td_wheel_deg = deg;
            _td_rotation(deg);
          });
        }
        if (_td_input.val().length) {
          /** @type {!RegExp} */
          var args = /\d+/g;
          var alllinesArray = _td_input.val().split(":");
          if (alllinesArray) {
            a = alllinesArray[0].match(args);
            url = alllinesArray[1].match(args);
            if (-1 != _td_input.val().indexOf("am") || -1 != _td_input.val().indexOf("AM") || -1 != _td_input.val().indexOf("pm") || -1 != _td_input.val().indexOf("PM")) {
              if (-1 != _td_input.val().indexOf("am") || -1 != _td_input.val().indexOf("AM")) {
                if (12 == a) {
                  /** @type {number} */
                  a = 0;
                }
              } else {
                if (a < 13 && 24 == (a = parseInt(a) + 12)) {
                  /** @type {number} */
                  a = 0;
                }
              }
            } else {
              if (24 == a) {
                /** @type {number} */
                a = 0;
              }
            }
          } else {
            a = parseInt($this.text()) ? _td_num($this.text()) : _td_num(ddate.getHours());
            url = parseInt($item.text()) ? _td_num($item.text()) : _td_num(ddate.getMinutes());
          }
        } else {
          a = parseInt($this.text()) ? _td_num($this.text()) : _td_num(ddate.getHours());
          url = parseInt($item.text()) ? _td_num($item.text()) : _td_num(ddate.getMinutes());
        }
        if (_td_options.minutesSteps && url % _td_options.minutesSteps) {
          /** @type {number} */
          url = 0;
        }
        $this.attr("data-id", a).text(a);
        $item.attr("data-id", url).text(url);
        if ($this.hasClass("on")) {
          /** @type {number} */
          _td_event_deg = Math.round(360 * a / 24);
        }
        if ($item.hasClass("on")) {
          /** @type {number} */
          _td_event_deg = Math.round(360 * url / 60);
        }
        _td_c.find(".td-lancette div:first").css("transform", "rotate(" + Math.round(360 * url / 60) + "deg)");
        _td_rotation(_td_event_deg);
        _td_wheel_deg = _td_event_deg;
        /** @type {number} */
        rectangleWidth = -1;
      };
      if (_td_options.setCurrentTime) {
        init();
      }
      _td_input.focus(function(event) {
        event.preventDefault();
        _td_input.blur();
      });
      _td_input.click(function(canCreateDiscussions) {
        clearInterval(_td_event);
        init();
        /** @type {number} */
        _td_event = setTimeout(function() {
          _td_container.removeClass("td-fadeout");
          _td_container.addClass("td-show").addClass("td-" + _td_options.init_animation);
          _td_c.css({
            top : _td_input.offset().top + (_td_input.outerHeight() - 8),
            left : _td_input.offset().left + _td_input.outerWidth() / 2 - _td_c.outerWidth() / 2
          });
          if (_td_c.hasClass("td-init")) {
            /** @type {number} */
            initializeCheckTimer = setInterval(function() {
              _td_c.find(".td-select").addClass("td-alert");
              setTimeout(function() {
                _td_c.find(".td-select").removeClass("td-alert");
              }, 1E3);
            }, 2E3);
            _td_c.removeClass("td-init");
          }
        }, 10);
      });
      imgchk.click(function() {
        _td_container.addClass("td-fadeout").removeClass("td-" + _td_options.init_animation);
        /** @type {number} */
        _td_event = setTimeout(function() {
          _td_container.removeClass("td-show");
        }, 300);
      });
      $(window).on("resize", function() {
        _td_define_deg();
        _td_c.css({
          top : _td_input.offset().top + (_td_input.outerHeight() - 8),
          left : _td_input.offset().left + _td_input.outerWidth() / 2 - _td_c.outerWidth() / 2
        });
      });
    });
  };
  $("head").append('<style>.td-wrap,.td-wrap *{margin:0;padding:0;list-style:none;box-sizing:initial!important;-webkit-tap-highlight-color:rgba(0,0,0,0)}.td-wrap svg{width:100%}.td-input{cursor:pointer}.td-wrap{display:none;font-family:sans-serif;position:absolute;-webkit-user-select:none;-o-user-select:none;user-select:none;outline:none;width:100%;height:100%;top:0;left:0;z-index:9999;color:#4d4d4d}.td-overlay{position:fixed;top:0;left:0;width:100%;height:100%}.td-clock{width:192px;height:192px;border-radius:192px;box-shadow:0 0 64px rgba(0,0,0,0.085);position:relative;background:#FFF;margin:0 auto;text-align:center;line-height:192px;position:absolute;background-position:center;background-repeat:no-repeat;background-size:cover}.td-clock:before{position:absolute;content:"";top:-8px;margin-left:-10px;left:50%;width:20px;height:20px;transform:rotate(45deg);background:#FFF;border-top-left-radius:4px}.td-quarters{z-index:1;pointer-events:none;transform:scale(0.95);opacity:0;transition:opacity 0.4s ease,transform 0.4s ease}.td-quarters.td-show{opacity:1;transform:scale(1)}.td-quarters:hover .td-quarter-bullet:not(.td-on){opacity:0.35}.td-quarters,.td-quarters .td-quarter{width:100%;height:100%;position:absolute;top:0;left:0}.td-quarters .td-quarter-bullet{width:6px;height:8px;border-radius:12px;position:absolute;cursor:pointer;z-index:2;top:20px;left:50%;transform:translateX(-50%);cursor:pointer;pointer-events:auto;transition:opacity 0.4s ease,height 0.4s ease}.td-quarters .td-quarter-bullet:hover{height:16px}.td-init .td-deg{-webkit-animation:slide 1s cubic-bezier(0.7,0,0.175,1) 1.2s infinite}.td-svg{position:absolute;top:0;bottom:0;left:0;right:0}.td-svg-2{position:absolute;top:18px;left:18px;bottom:18px;right:18px}.td-wrap.td-show{display:block}.td-deg{background-position:center;background-repeat:no-repeat;background-size:80%;position:absolute;z-index:1;pointer-events:none;top:0;left:0;right:0;bottom:0}.td-medirian{position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none}.td-medirian span{width:40px;height:40px;border-radius:40px;line-height:40px;text-align:center;margin:0;position:absolute;z-index:1;left:50%;margin-left:-20px;font-size:0.8em;opacity:0;font-weight:bold}.td-medirian .td-icon-am{top:60px}.td-medirian .td-icon-pm{bottom:60px}.td-medirian .td-icon-am.td-on{top:40px;opacity:1}.td-medirian .td-icon-pm.td-on{bottom:40px;opacity:1}.td-select{position:absolute;top:12px;left:32px;right:32px;bottom:32px;z-index:11}.td-select svg{position:absolute;top:0;left:0;right:0;cursor:pointer;transform:rotateX(180deg) scale(0.7);pointer-events:auto}.td-clock .td-time{font-weight:bold;position:relative}.td-clock .td-time span{width:42px;height:42px;display:inline-block;vertical-align:middle;line-height:42px;text-align:center;margin:6px;position:relative;z-index:2;cursor:pointer;font-size:2em;border-radius:6px}.td-n{transition:all 0.4s cubic-bezier(0.7,0,0.175,1) 0s}.td-n2{transition:all 0.2s linear 0s}@keyframes td-alert{0%{transform:scale3d(1,1,1)}10%,20%{transform:scale3d(0.9,0.9,0.9) rotate3d(0,0,1,-3deg)}30%,50%,70%,90%{transform:scale3d(1.1,1.1,1.1) rotate3d(0,0,1,3deg)}40%,60%,80%{transform:scale3d(1.1,1.1,1.1) rotate3d(0,0,1,-3deg)}to{transform:scale3d(1,1,1)}}.td-alert{animation-name:td-alert;animation-duration:0.8s;animation-fill-mode:both}@keyframes td-bounce{0%{transform:scale3d(1,1,1)}20%{transform:scale3d(1.25,0.75,1)}30%{transform:scale3d(0.75,1.25,1)}60%{transform:scale3d(1.15,0.85,1)}70%{transform:scale3d(0.95,1.05,1)}80%{transform:scale3d(1.05,0.95,1)}to{transform:scale3d(1,1,1)}}.td-bounce{animation-name:td-bounce;animation-duration:1s}@keyframes td-fadein{0%{opacity:0}to{opacity:1}}.td-fadein{animation-name:td-fadein;animation-duration:0.3s}@keyframes td-fadeout{0%{opacity:1}to{opacity:0}}.td-fadeout{animation:td-fadeout 0.3s forwards}@keyframes td-dropdown{0%{opacity:0;transform:translate3d(0,-32px,0)}to{opacity:1;transform:none}}.td-dropdown{animation-name:td-dropdown;animation-duration:0.5s}.td-bulletpoint,.td-bulletpoint div,.td-lancette,.td-lancette div{position:absolute;top:0;left:0;bottom:0;right:0}.td-bulletpoint div:after{position:absolute;content:"";top:14px;left:50%;margin-left:-2px;width:4px;height:4px;border-radius:10px}.td-lancette{border:4px solid #DFF3FA;border-radius:100%;margin:8px}.td-lancette div:after{position:absolute;top:20px;left:50%;margin-left:-1px;width:2px;bottom:50%;border-radius:10px;background:#DFF3FA;content:""}.td-lancette div:last-child:after{top:36px}.td-clock{color:var(--td-textColor);background:var(--td-backgroundColor)}.td-clock .td-time span.on{color:var(--td-primaryColor)}.td-quarter-bullet{background:var(--td-primaryColor)}.td-clock:before{border-color:var(--td-borderColor)}.td-clock:before,.td-select:after{background:var(--td-backgroundColor)}.td-lancette{border:var(--td-displayBorderWidth) var(--td-displayBorderStyle) var(--td-displayBorderColor);background:var(--td-displayBackgroundColor)}.td-lancette div:after{background:var(--td-handsColor)}.td-bulletpoint div:after{background:var(--td-primaryColor);opacity:0.1}.td-select svg path{stroke:var(--td-handleColor)}.td-select svg circle{fill:var(--td-handlePointColor)}:root{--td-textColor:#999999;--td-backgroundColor:#FFF;--td-primaryColor:#222222;--td-displayBackgroundColor:#FFF;--td-displayBorderColor:#A2E073;--td-displayBorderStyle:solid;--td-displayBorderWidth:4px;--td-handsColor:#A2E07350;--td-handleColor:#A2E073;--td-handlePointColor:white}</style>');
}(jQuery);