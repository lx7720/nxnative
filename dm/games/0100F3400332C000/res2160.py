# Xenoblade Chronicles 2 3.0.0 (JP) at 3840x2160 instead of 1280x720: the rewriter's cuts for a second set of modules (patched_v983040_2160), applied with DM_PATCH_EXTRA=<this file>.
# - the 1280x720 RGBA8 texture main+0x700640 builds (the engine sizes its render targets from it: G-buffer 3840x2160);
# - the screen size getters (main+0x6e3fc8 / +0x6e3fd0) and the other places that hold 1280 / 720 (effects, post-processing: without them post effects drew 720p boxes in the frame);
# - the memory the engine budgets for it at start: the graphics heap (config +0x30, main+0x6421c4, 512 MB -> 4 GB; the root heap the render-target pool is cut from) and the
#   render-target pool (main+0x6f4f74, 362 MB -> 3 GB). Without them the pool allocation failed (svcBreak at main+0x6e9420). Needs a larger memory partition than game.tsv sets (mem_reserve 0x200000000, app_pool 0x1CD500000)
# - 2026-10-25: the GLIBUNI heap (main+0x6f4f90, 28 MB; GLIB heaps are cut at main+0x705c20) holds screen-sized buffers (main+0x834510, w*h*3 each): at 1440p they did not fit and
#   the game stopped (svcBreak at main+0x6e9420, from main+0x7064d0) right after the language prompt. 128 MB; GLIBVTX doubled too. Checked headless (2160p): boots, opening, first battle screen; GPU allocated ~6.3 GB.
# - 2026-10-29, on a host with upstream's queue raster origin fix (9b2f085), M4 Pro: cutscenes 30 fps (GPU 29-31 ms), first battle ~38-40 fps, menus 60.
CUTS = {'feee7afa8a1541bd67aed1a0061fbb57': [
    (0x700640, '15a08052', '15e08152', 'tw'),
    (0x700644, '165a8052', '160e8152', 'th'),
    (0x6e3fc8, '00a08052', '00e08152', 'w'),
    (0x6e3fd0, '005a8052', '000e8152', 'h'),
    (0x6f4f74, '09d4e2d2', '0900f8d2', 'render target pool 362 MB -> 3 GB'),
    (0x6421c4, 'e8030332', '2800c0d2', 'graphics heap 512 MB -> 4 GB (mov x8: the config field is 64 bits)'),
    (0xfa3ec, '02a08052', '02e08152', 'w2, #0x500'),
    (0xfa3f0, '035a8052', '030e8152', 'w3, #0x2d0'),
    (0xfa860, '02a08052', '02e08152', 'w2, #0x500'),
    (0xfa864, '035a8052', '030e8152', 'w3, #0x2d0'),
    (0x14da34, '01a08052', '01e08152', 'w1, #0x500'),
    (0x14da38, '025a8052', '020e8152', 'w2, #0x2d0'),
    (0x4a461c, '00a08052', '00e08152', 'w0, #0x500'),
    (0x4a4620, '015a8052', '010e8152', 'w1, #0x2d0'),
    (0x6809e4, '175a8052', '170e8152', 'w23, #0x2d0'),
    (0x6809e8, '14a08052', '14e08152', 'w20, #0x500'),
    (0x680ab4, '14a08052', '14e08152', 'w20, #0x500'),
    (0x680ab8, '175a8052', '170e8152', 'w23, #0x2d0'),
    (0x6f4f90, 'e80b0a32', '0800a152', 'GLIBUNI heap 28 MB -> 128 MB'),
    (0x6f4f80, '0950a052', '09a4a052', 'GLIBVTX heap 42 MB -> 84 MB (w9 + 2 MB)'),
    # screen-space particles: keep their projection at the 1280x720 virtual screen (same three rows as res1440.py)
    (0x862ac0, 'a05a45bd', 'a024000f', 'screen-space particle width: movi v0.2s, #1280 (was ldr s0, [x21, #0x558])'),
    (0x862ad8, 'a25e45bd', '085a8052', 'screen-space particle height: movz w8, #720 (was ldr s2, [x21, #0x55c])'),
    (0x862ae0, '42d8217e', '0201231e', 'ucvtf s2, w8'),
]}
