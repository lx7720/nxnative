# Xenoblade Chronicles 2 3.0.0 (JP) at 2560x1440 instead of 1280x720: the rewriter's cuts for a second set of modules (patched_v983040_1440), applied with DM_PATCH_EXTRA=<this file>.
# - the 1280x720 RGBA8 texture main+0x700640 builds (the engine sizes its render targets from it: G-buffer 2560x1440);
# - the screen size getters (main+0x6e3fc8 / +0x6e3fd0) and the other places that hold 1280 / 720 (effects, post-processing: without them post effects drew 720p boxes in the frame);
# - the memory the engine budgets for it at start: the graphics heap (config +0x30, main+0x6421c4, 512 MB -> 2 GB; the root heap the render-target pool is cut from) and the
#   render-target pool (main+0x6f4f74, 362 MB -> 1.5 GB). Without them the pool allocation failed (svcBreak at main+0x6e9420). Needs a larger memory partition than game.tsv sets (mem_reserve 0x200000000, app_pool 0x1CD500000)
CUTS = {'feee7afa8a1541bd67aed1a0061fbb57': [
    (0x700640, '15a08052', '15408152', 'tw'),
    (0x700644, '165a8052', '16b48052', 'th'),
    (0x6e3fc8, '00a08052', '00408152', 'w'),
    (0x6e3fd0, '005a8052', '00b48052', 'h'),
    (0x6f4f74, '09d4e2d2', '0900ecd2', 'render target pool 362 MB -> 1.5 GB'),
    (0x6421c4, 'e8030332', '0800b0d2', 'graphics heap 512 MB -> 2 GB (mov x8: the config field is 64 bits)'),
    (0x6f4f90, 'e80b0a32', '0800a152', 'GLIBUNI heap 28 MB -> 128 MB (1440p stopped after the language prompt without it, 2026-10-25)'),
    (0x6f4f80, '0950a052', '09a4a052', 'GLIBVTX heap 42 MB -> 84 MB (w9 + 2 MB)'),
    (0xfa3ec, '02a08052', '02408152', 'w2, #0x500'),
    (0xfa3f0, '035a8052', '03b48052', 'w3, #0x2d0'),
    (0xfa860, '02a08052', '02408152', 'w2, #0x500'),
    (0xfa864, '035a8052', '03b48052', 'w3, #0x2d0'),
    (0x14da34, '01a08052', '01408152', 'w1, #0x500'),
    (0x14da38, '025a8052', '02b48052', 'w2, #0x2d0'),
    (0x4a461c, '00a08052', '00408152', 'w0, #0x500'),
    (0x4a4620, '015a8052', '01b48052', 'w1, #0x2d0'),
    (0x6809e4, '175a8052', '17b48052', 'w23, #0x2d0'),
    (0x6809e8, '14a08052', '14408152', 'w20, #0x500'),
    (0x680ab4, '14a08052', '14408152', 'w20, #0x500'),
    (0x680ab8, '175a8052', '17b48052', 'w23, #0x2d0'),
    # screen-space particles (main+0x861438 writes their projection diag(2/W, 2/H) from the render-context size +0x558/+0x55c): their sizes are authored in 720p pixels
    # (a cutscene fog quad is 1280 x 723.2), so at a larger render target they covered only the centre; keep the projection at the 1280x720 virtual screen
    (0x862ac0, 'a05a45bd', 'a024000f', 'screen-space particle width: movi v0.2s, #1280 (was ldr s0, [x21, #0x558])'),
    (0x862ad8, 'a25e45bd', '085a8052', 'screen-space particle height: movz w8, #720 (was ldr s2, [x21, #0x55c])'),
    (0x862ae0, '42d8217e', '0201231e', 'ucvtf s2, w8'),
]}
