-- Copyright (C) 2026 Danny Nunez

local output = script.dir .. "/../artifacts/cover-demo-v3/"
local start_frame = nil

local function shot(name)
  local display_control = emu:read16(0x04000000)
  local page = 0x06000000
  if math.floor(display_control / 0x10) % 2 == 1 then
    page = page + 0xA000
  end

  local frame = assert(io.open(output .. name .. ".frame", "wb"))
  frame:write(emu:readRange(0x05000000, 512))
  frame:write(emu:readRange(page, 240 * 160))
  frame:close()
end

local function press(key)
  emu:addKey(key)
end

local function release(key)
  emu:clearKey(key)
end

callbacks:add("frame", function()
  if not start_frame then
    start_frame = emu:currentFrame()
  end
  local frame = emu:currentFrame() - start_frame

  if frame == 100 then
    shot("glow-red")
  elseif frame == 101 then
    press(C.GBA_KEY.SELECT)
  elseif frame == 103 then
    release(C.GBA_KEY.SELECT)
  elseif frame == 108 then
    shot("glow-cyan")
  elseif frame == 109 then
    press(C.GBA_KEY.SELECT)
  elseif frame == 111 then
    release(C.GBA_KEY.SELECT)
  elseif frame == 120 then
    shot("browse-aurora-ready")
  elseif frame == 130 then
    press(C.GBA_KEY.DOWN)
  elseif frame == 135 then
    release(C.GBA_KEY.DOWN)
  elseif frame == 145 then
    shot("browse-checker-pending")
  elseif frame == 200 then
    shot("browse-checker-ready")
  elseif frame == 210 then
    shot("browse-checker-stable")
  elseif frame == 215 then
    press(C.GBA_KEY.DOWN)
  elseif frame == 220 then
    release(C.GBA_KEY.DOWN)
  elseif frame == 310 then
    shot("browse-missing")
  elseif frame == 315 then
    press(C.GBA_KEY.DOWN)
  elseif frame == 320 then
    release(C.GBA_KEY.DOWN)
  elseif frame == 410 then
    shot("browse-invalid")
  elseif frame == 415 then
    press(C.GBA_KEY.DOWN)
  elseif frame == 420 then
    release(C.GBA_KEY.DOWN)
  elseif frame == 510 then
    shot("browse-folder")
  elseif frame == 515 then
    press(C.GBA_KEY.DOWN)
  elseif frame == 520 then
    release(C.GBA_KEY.DOWN)
  elseif frame == 530 then
    shot("browse-long-name-start")
  elseif frame == 610 then
    shot("browse-long-name-scrolled")
  elseif frame == 615 then
    press(C.GBA_KEY.DOWN)
  elseif frame == 620 then
    release(C.GBA_KEY.DOWN)
  elseif frame == 630 then
    shot("browse-last-row")
  elseif frame == 635 then
    press(C.GBA_KEY.DOWN)
  elseif frame == 640 then
    release(C.GBA_KEY.DOWN)
  elseif frame == 650 then
    shot("browse-window-shift")
  elseif frame == 655 then
    press(C.GBA_KEY.L)
  elseif frame == 660 then
    release(C.GBA_KEY.L)
  elseif frame == 720 then
    shot("recent-aurora-ready")
  elseif frame == 725 then
    press(C.GBA_KEY.R)
  elseif frame == 730 then
    release(C.GBA_KEY.R)
  elseif frame == 735 then
    press(C.GBA_KEY.R)
  elseif frame == 740 then
    release(C.GBA_KEY.R)
  elseif frame == 820 then
    shot("dock-settings")
  elseif frame == 825 then
    press(C.GBA_KEY.R)
  elseif frame == 830 then
    release(C.GBA_KEY.R)
  elseif frame == 835 then
    press(C.GBA_KEY.R)
  elseif frame == 840 then
    release(C.GBA_KEY.R)
  elseif frame == 920 then
    shot("dock-tools")
  elseif frame == 930 then
    local marker = io.open(output .. "complete.txt", "w")
    marker:write("mGBA 76x76 cover demo completed\n")
    marker:close()
  end
end)
