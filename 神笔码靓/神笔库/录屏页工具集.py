# -*- coding: utf-8 -*-
"""录屏页工具集（框架级）

只做两件与「作品装进画框」有关的事，**不碰任何时钟元素、不参与走时**：

1. 开场缩放脚本 —— 放大到指定倍数、停留、再缓动缩回 100% 并居中；
   缩放与位移都交给 CSS 关键帧（合成器线程），主线程忙也不会抖。
2. 录屏页 —— 把 SVG 包进 16:9 画框，加上下装饰、可选字体、浏览器内置录制。

走时与元素操作不在这里：请用 时间管家.注册时间事件() 在回调里自己驱动元素。
"""

import base64
import json
import os
import re

缓动别名 = {
    "线性": "linear", "匀速": "linear",
    "缓出": "easeOutCubic",
    "缓入缓出": "easeInOutCubic", "平滑": "easeInOutCubic",
}

默认开场设置 = {
    "启用": True,
    "倍数": 8,
    "停留毫秒": 3000,
    "时长毫秒": 20000,
    "缓动": "easeInOutCubic",
    "锚点": None,                    # [x, y]：放大时对准画面中心的 SVG 坐标
    "居中": True,
    "推拉": True,
    "自动循环": False,
    "循环间隔毫秒": 2000,
    "点击重播": False,
    "键盘重播": True,
}

默认页面设置 = {
    "标题": "",
    "副标题": "",
    "标题字体": None,
    "标题字体名": "标题字体",
    "副标题字体": None,
    "副标题字体名": "副标题字体",
    "标题字号": None,
    "副标题字号": None,
    "标题位置": "7.5%",
    "副标题位置": "12%",
    "内嵌字体": False,
    "装饰": True,
    "画框宽": 1920,
    "画框高": 1080,
    "背景": None,
    "录制": {
        "启用": True,
        "帧率": 60,
        "比特率": 12000000,
        "播完自动停止": True,
    },
}


def 合并设置(*层):
    """深合并配置（后面的覆盖前面的），None 与空字符串也会覆盖。"""
    结果 = {}
    for 层_ in 层:
        if not 层_:
            continue
        for k, v in 层_.items():
            if isinstance(v, dict) and isinstance(结果.get(k), dict):
                结果[k] = 合并设置(结果[k], v)
            else:
                结果[k] = v
    return 结果


def _缓动名(名):
    return 缓动别名.get(名, 名 or "easeInOutCubic")


def _转义JSON(数据):
    文本 = json.dumps(数据, ensure_ascii=False, separators=(",", ":"))
    return 文本.replace("</", "<\\/")


# ============================================================
# 开场缩放脚本（独立脚本，录屏页会整段替换掉）
# ============================================================

# ============================================================
# 开场缩放脚本（独立脚本，录屏页会整段替换掉）
# ============================================================

开场JS = r"""
/* ===== 开场缩放（独立脚本，可整段删除，不影响走时）=====
   放大到「倍数」停留一会儿，再缓动缩回 100% 并居中。
   地址栏可临时覆盖：?zoomoff=1 关闭；?zoom=8&ms=6000 改倍数/时长 */
(function () {
  var 配置 = __CAMERA__;
  var 根 = document.documentElement;
  var 参 = null;
  try { 参 = new URLSearchParams(location.search || ""); } catch (e) { }
  if (参 && 参.has("zoomoff")) 配置.启用 = false;
  if (参 && 参.has("zoom")) 配置.倍数 = parseFloat(参.get("zoom")) || 配置.倍数;
  if (参 && 参.has("ms")) 配置.时长毫秒 = parseFloat(参.get("ms")) || 配置.时长毫秒;
  if (!配置.启用) return;

  var 起始 = Math.max(1, 配置.倍数 || 1), 时长 = Math.max(1, 配置.时长毫秒 || 1);
  var 停留 = Math.max(0, 配置.停留毫秒 || 0);
  var 图宽 = 配置.图宽, 图高 = 配置.图高;
  var 原点X = 配置.锚点 ? 配置.锚点[0] : 图宽 / 2;
  var 原点Y = 配置.锚点 ? 配置.锚点[1] : 图高 / 2;
  var 居中 = 配置.居中 !== false, 推拉 = 配置.推拉 !== false;
  if (起始 === 1) return;

  var 曲线 = { linear: "linear", easeOutCubic: "cubic-bezier(.33,1,.68,1)",
              easeInOutCubic: "cubic-bezier(.65,0,.35,1)" }[配置.缓动] || "cubic-bezier(.65,0,.35,1)";

  // 缩放与位移都是进度的线性函数 → 整段写成 CSS 关键帧，由合成器线程播放，
  // 主线程忙着重绘指针也不会掉帧。
  var dx = (居中 && 推拉) ? 原点X - 图宽 / 2 : 0;
  var dy = (居中 && 推拉) ? 原点Y - 图高 / 2 : 0;
  var 基X = 居中 ? (window.innerWidth - 图宽) / 2 : 0;
  var 基Y = 居中 ? (window.innerHeight - 图高) / 2 : 0;

  var 样式 = document.createElement("style");
  样式.textContent = "@keyframes 开场推拉{"
    + "from{transform:translate(" + (基X - dx * 起始) + "px," + (基Y - dy * 起始) + "px) scale(" + 起始 + ")}"
    + "to{transform:translate(" + 基X + "px," + 基Y + "px) scale(1)}}";
  根.appendChild(样式);

  var 原溢出 = 根.style.overflow;
  根.style.transformOrigin = (居中 && 推拉) ? (图宽 / 2) + "px " + (图高 / 2) + "px"
                                            : 原点X + "px " + 原点Y + "px";
  根.style.overflow = "hidden";
  根.style.animation = "开场推拉 " + 时长 + "ms " + 曲线 + " " + 停留 + "ms both";

  根.addEventListener("animationend", function (e) {
    if (e.animationName === "开场推拉") 根.style.overflow = 原溢出;
  });
})();
"""


def 生成开场脚本(设置=None):
    设置 = 合并设置(默认开场设置, 设置 or {})
    设置["缓动"] = _缓动名(设置.get("缓动"))
    return 开场JS.replace("__CAMERA__", _转义JSON(设置))


# ============================================================
# 录屏页
# ============================================================

页面HTML = r"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>__PAGE_TITLE__</title>
<style>
  __FONT_FACE__
  html, body { height: 100%; margin: 0; overflow: hidden; background: #14141a; }
  body { display: grid; place-items: center; }

  /* 固定比例画框：无论窗口什么比例，录出来的画面都是横向的 */
  #画框 {
    position: relative;
    width: min(100vw, calc(100vh * __FW__ / __FH__));
    aspect-ratio: __FW__ / __FH__;
    max-height: 100vh;
    display: flex; align-items: center; justify-content: center;
    overflow: hidden;
    background: __BG__;
  }

  /* 上下装饰：在时钟之外，不随缩放变化；z-index 低于舞台，放大时被钟面盖住 */
  .装饰 { position: absolute; left: 0; right: 0; z-index: 0; text-align: center; color: #8d8a82; pointer-events: none; }
  #装饰上 { top: __TITLE_POS__; font-family: __TITLE_FAMILY__; font-size: __TITLE_SIZE__; letter-spacing: .42em; }
  #装饰下 { bottom: __SUB_POS__; font-family: __SUB_FAMILY__; font-size: __SUB_SIZE__; letter-spacing: .62em; }
  #装饰上::after, #装饰下::before {
    content: ""; display: block; width: 7%; height: 1px; margin: 1.5em auto;
    background: linear-gradient(90deg, rgba(0,0,0,0), rgba(0,0,0,.18), rgba(0,0,0,0));
  }
  #装饰下::before { margin: 0 auto 1.5em; }
  /* 负右边距抵消末字符后的字距 → 墨迹真正居中 */
  #装饰上 span, #装饰下 span { display: inline-block; }
  #装饰上 span { margin-right: -.42em; }
  #装饰下 span { margin-right: -.62em; }

  #舞台 { z-index: 1; will-change: transform; backface-visibility: hidden; }
  #舞台 svg { display: block; }

  /* 内置录制条：录制开始后淡出，不会出现在视频里 */
  #录屏条 {
    position: fixed; left: 50%; bottom: 14px; transform: translateX(-50%);
    z-index: 99; display: flex; align-items: center; gap: 10px;
    padding: 7px 16px; border-radius: 999px;
    background: rgba(18,18,24,.78); color: #e9e6df;
    font: 13px/1.4 "Microsoft YaHei", system-ui, sans-serif;
    box-shadow: 0 6px 20px rgba(0,0,0,.28);
    opacity: .35; transition: opacity .25s ease, transform .25s ease;
    backdrop-filter: blur(6px);
  }
  #录屏条:hover { opacity: 1; }
  #录屏条.录制中 { opacity: 0; pointer-events: none; transform: translate(-50%, 12px); }
  #录屏按钮 { all: unset; cursor: pointer; padding: 3px 10px; border-radius: 999px;
              background: #c0392b; color: #fff; font-weight: 600; letter-spacing: .04em; }
  #录屏按钮:hover { background: #d54535; }
  #录屏状态 { opacity: .8; white-space: nowrap; }
  @media (max-width: 700px) { #录屏状态 { display: none; } }
</style>
</head>
<body>
<div id="画框">__DECO__<div id="舞台">__SVG__</div></div>
__RECBAR__
<script>
(function () {
  var 舞台 = document.getElementById("舞台");
  var 起始 = __SCALE__, 停留 = __HOLD__, 时长 = __DURATION__;
  var 图宽 = __W__, 图高 = __H__, 原点X = __OX__, 原点Y = __OY__, 推拉 = __PUSH__;
  var 循环 = __LOOP__, 间隔 = __GAP__, 点击 = __CLICK__;
  var 曲线 = __BEZIER__;
  var 循环定时 = 0;

  // 缩放 s 与位移 t 都是进度的线性函数 → 整段写成 CSS 关键帧，交给合成器线程
  var dx = 推拉 ? 原点X - 图宽 / 2 : 0;
  var dy = 推拉 ? 原点Y - 图高 / 2 : 0;

  var 样式 = document.createElement("style");
  样式.textContent = "@keyframes 开场推拉{"
    + "from{transform:translate(" + (-dx * 起始) + "px," + (-dy * 起始) + "px) scale(" + 起始 + ")}"
    + "to{transform:translate(0px,0px) scale(1)}}";
  document.head.appendChild(样式);

  舞台.style.transformOrigin = 推拉 ? (图宽 / 2) + "px " + (图高 / 2) + "px"
                                  : 原点X + "px " + 原点Y + "px";
  var 动画 = "开场推拉 " + 时长 + "ms " + 曲线 + " " + 停留 + "ms both";

  function 播放() {
    clearTimeout(循环定时);
    舞台.style.animation = "none";
    void 舞台.offsetWidth;
    舞台.style.animation = 动画;
  }

  舞台.addEventListener("animationend", function (e) {
    if (e.animationName !== "开场推拉") return;
    if (循环) 循环定时 = setTimeout(播放, 间隔);
  });

  播放();
  window.重播 = 播放;
  window.回到开场 = 播放;

  // 离线渲染接口：加 ?render=1 时跳过 CSS 动画，由渲染器逐帧给进度
  window.设缩放 = function (s) {
    s = Math.min(起始, Math.max(1, s));
    var f = 起始 > 1 ? Math.min(1, Math.max(0, (起始 - s) / (起始 - 1))) : 1;
    var tx = 推拉 ? dx * (f - s) : 0;
    var ty = 推拉 ? dy * (f - s) : 0;
    舞台.style.animation = "none";
    舞台.style.transform = "translate(" + tx + "px," + ty + "px) scale(" + s + ")";
  };
  window.设进度 = function (p) {
    p = Math.min(1, Math.max(0, p));
    var e = p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
    设缩放(起始 + (1 - 起始) * e);
  };
  if (location.search.indexOf("render=1") >= 0) {
    舞台.style.animation = "none";
    var 条 = document.getElementById("录屏条");
    if (条) 条.remove();
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "F12") return;
    e.preventDefault(); 播放();
  });
  if (点击) document.addEventListener("pointerdown", function () { 播放(); });
})();

/* 内置录制：浏览器原生 getDisplayMedia + MediaRecorder（不需要 OBS / Win+G） */
(function () {
  if (!__RECUI__) return;
  var 舞台 = document.getElementById("舞台");
  var 条 = document.getElementById("录屏条");
  var 按钮 = document.getElementById("录屏按钮");
  var 状态 = document.getElementById("录屏状态");
  var 帧率 = __FPS__, 码率 = __BITRATE__, 自动停 = __AUTOSTOP__;
  var 录制器 = null, 数据 = null, 流 = null;

  function 时间戳() {
    var d = new Date(), p = function (n) { return (n < 10 ? "0" : "") + n; };
    return d.getFullYear() + p(d.getMonth() + 1) + p(d.getDate()) + "_"
         + p(d.getHours()) + p(d.getMinutes()) + p(d.getSeconds());
  }
  function 下载(blob) {
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "__FILEBASE___" + 时间戳() + ".webm";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 5000);
  }
  function 停止() { if (录制器 && 录制器.state !== "inactive") 录制器.stop(); }
  function 开始() {
    if (录制器) { 停止(); return; }
    if (!navigator.mediaDevices || !navigator.mediaDevices.getDisplayMedia) {
      状态.textContent = "此浏览器不支持录制，请用 Edge/Chrome"; return;
    }
    navigator.mediaDevices.getDisplayMedia({
      video: { frameRate: 帧率, width: { ideal: __FW__ }, height: { ideal: __FH__ } },
      audio: false, preferCurrentTab: true, selfBrowserSurface: "include", surfaceSwitching: "exclude"
    }).then(function (s) {
      流 = s;
      try {
        var 轨 = s.getVideoTracks()[0];
        if (轨 && "contentHint" in 轨) 轨.contentHint = "motion";
      } catch (e) { }
      var 类型 = ["video/webm;codecs=vp9", "video/webm;codecs=vp8", "video/webm"]
        .filter(function (t) { return window.MediaRecorder && MediaRecorder.isTypeSupported(t); })[0];
      数据 = [];
      录制器 = new MediaRecorder(流, { mimeType: 类型, videoBitsPerSecond: 码率 });
      录制器.ondataavailable = function (e) { if (e.data && e.data.size) 数据.push(e.data); };
      录制器.onstop = function () {
        try { 流.getTracks().forEach(function (t) { t.stop(); }); } catch (e) { }
        var b = new Blob(数据, { type: 类型 || "video/webm" });
        录制器 = null;
        条.classList.remove("录制中");
        按钮.textContent = "● 录制";
        状态.textContent = "已保存 " + (b.size / 1048576).toFixed(1)
          + " MB · 播放器只显示 1 秒属容器问题，用 修复录制文件.py 转一下就正常了";
        下载(b);
      };
      录制器.start(1000);
      条.classList.add("录制中");
      按钮.textContent = "■ 停止";
      状态.textContent = "录制中…（再按 V 结束）";
      if (window.重播) window.重播();
    }).catch(function (e) {
      状态.textContent = (e && e.name === "NotAllowedError") ? "已取消 / 未授权" : ("失败：" + e);
    });
  }

  舞台.addEventListener("animationend", function (e) {
    if (e.animationName === "开场推拉" && 自动停) setTimeout(停止, 400);
  });
  按钮.addEventListener("click", 开始);
  document.addEventListener("keydown", function (e) {
    if (e.key === "v" || e.key === "V") { e.preventDefault(); 开始(); }
  });
  window.录制 = 开始;
  window.停止录制 = 停止;
})();
</script>
</body>
</html>
"""


def _内嵌字体(路径, 族名, 目录, 脚本目录, 内嵌=False, 引用表=None):
    回退 = f'"{族名}", "Helvetica Neue", Helvetica, Arial, "Microsoft YaHei", sans-serif'
    if not 路径:
        return "", 回退
    p = 路径 if os.path.isabs(路径) else os.path.join(脚本目录, 路径)
    if not os.path.exists(p):
        print(f"⚠ 字体文件不存在，改用系统字体：{p}")
        return "", 回退
    if 内嵌:
        with open(p, "rb") as f:
            数据 = base64.b64encode(f.read()).decode("ascii")
        css = ('@font-face { font-family: "%s"; src: url("data:font/ttf;base64,%s") '
               'format("truetype"); font-display: block; }' % (族名, 数据))
    else:
        try:
            相对 = os.path.relpath(p, 目录).replace("\\", "/")
        except ValueError:
            相对 = "file:///" + p.replace("\\", "/")
        if 引用表 is not None:
            引用表.append(相对)
        css = ('@font-face { font-family: "%s"; src: url("%s") '
               'format("truetype"); font-display: swap; }' % (族名, 相对))
    return css, 回退


def 生成录屏页(设置):
    """把 SVG 文本包装成 16:9 录屏页（含装饰、开场动画、内置录制）。"""
    设置 = 合并设置(默认页面设置, 设置 or {})
    开场 = 合并设置(默认开场设置, 设置.get("开场") or {})
    录制 = 合并设置(默认页面设置["录制"], 设置.get("录制") or {})

    画框宽 = int(设置.get("画框宽", 1920))
    画框高 = int(设置.get("画框高", 1080))
    输出目录 = 设置.get("输出目录") or os.getcwd()
    脚本目录 = 设置.get("脚本目录") or os.getcwd()

    引用表 = []
    标题CSS, 标题族 = _内嵌字体(设置.get("标题字体"), 设置.get("标题字体名") or "标题字体",
                            输出目录, 脚本目录, 设置.get("内嵌字体", False), 引用表)
    副CSS, 副族 = "", 标题族
    if 设置.get("副标题字体"):
        副CSS, 副族 = _内嵌字体(设置["副标题字体"], 设置.get("副标题字体名") or "副标题字体",
                               输出目录, 脚本目录, 设置.get("内嵌字体", False), 引用表)

    def 字号(值, 缺省):
        if 值 is None:
            return 缺省
        return f"{值}px" if isinstance(值, (int, float)) else str(值)

    装饰HTML = ""
    if 设置.get("装饰", True):
        if 设置.get("标题"):
            装饰HTML += f'<div class="装饰" id="装饰上"><span>{设置["标题"]}</span></div>'
        if 设置.get("副标题"):
            装饰HTML += f'<div class="装饰" id="装饰下"><span>{设置["副标题"]}</span></div>'

    录制HTML = ('<div id="录屏条"><button id="录屏按钮" type="button">● 录制</button>'
                '<span id="录屏状态">或按 V；选「当前标签页」</span></div>') if 录制.get("启用", True) else ""

    锚点 = 开场.get("锚点") or [设置.get("图宽", 0) / 2, 设置.get("图高", 0) / 2]
    背景 = 设置.get("背景") or "radial-gradient(120% 120% at 50% 42%, #fcfbf8 0%, #efede7 55%, #dedcd5 100%)"
    曲线 = {"linear": "linear", "easeOutCubic": "cubic-bezier(.33,1,.68,1)",
            "easeInOutCubic": "cubic-bezier(.65,0,.35,1)"}.get(
                开场.get("缓动"), "cubic-bezier(.65,0,.35,1)")

    return (页面HTML
            .replace("__PAGE_TITLE__", 设置.get("页面标题") or "ClockClock 24 · 录屏")
            .replace("__FONT_FACE__", 标题CSS + ("\n  " + 副CSS if 副CSS else ""))
            .replace("__TITLE_FAMILY__", 标题族).replace("__SUB_FAMILY__", 副族)
            .replace("__TITLE_SIZE__", 字号(设置.get("标题字号"), "clamp(10px, 1.55vh, 19px)"))
            .replace("__SUB_SIZE__", 字号(设置.get("副标题字号"), "clamp(9px, 1.3vh, 16px)"))
            .replace("__TITLE_POS__", str(设置.get("标题位置", "7.5%")))
            .replace("__SUB_POS__", str(设置.get("副标题位置", "12%")))
            .replace("__DECO__", 装饰HTML)
            .replace("__SVG__", 设置.get("SVG", ""))
            .replace("__RECBAR__", 录制HTML)
            .replace("__RECUI__", "true" if 录制.get("启用", True) else "false")
            .replace("__FPS__", str(int(录制.get("帧率", 60))))
            .replace("__BITRATE__", str(int(录制.get("比特率", 12000000))))
            .replace("__AUTOSTOP__", "true" if 录制.get("播完自动停止", True) else "false")
            .replace("__FILEBASE__", 设置.get("文件前缀") or "Clock")
            .replace("__SCALE__", str(开场.get("倍数", 8)))
            .replace("__HOLD__", str(开场.get("停留毫秒", 3000)))
            .replace("__DURATION__", str(开场.get("时长毫秒", 20000)))
            .replace("__PUSH__", "true" if 开场.get("推拉", True) else "false")
            .replace("__LOOP__", "true" if 开场.get("自动循环", False) else "false")
            .replace("__GAP__", str(开场.get("循环间隔毫秒", 2000)))
            .replace("__CLICK__", "true" if 开场.get("点击重播", False) else "false")
            .replace("__BEZIER__", json.dumps(曲线))
            .replace("__OX__", f"{锚点[0]:.2f}").replace("__OY__", f"{锚点[1]:.2f}")
            .replace("__W__", f"{设置.get('图宽', 0):g}").replace("__H__", f"{设置.get('图高', 0):g}")
            .replace("__FW__", str(画框宽)).replace("__FH__", str(画框高))
            .replace("__BG__", 背景)), 引用表


def 提取SVG(路径):
    """读取绘图板产出的 SVG，剥掉 XML 头、DOCTYPE 和开场缩放脚本（页面里另有一套）。"""
    with open(路径, "r", encoding="utf-8") as f:
        文本 = f.read()
    文本 = re.sub(r"<\?xml[^>]*\?>\s*", "", 文本)
    文本 = re.sub(r"<!DOCTYPE[^>]*>\s*", "", 文本, flags=re.S)
    段 = re.split(r"(<script\b[^>]*>.*?</script>)", 文本, flags=re.S)
    return "".join(块 for 块 in 段 if "开场缩放" not in 块)
