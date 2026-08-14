-- Copyright (C) 2026 Danny Nunez (dnunezx)

local output = script.dir .. "/../artifacts/ingame-menu/"
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

local function press(key) emu:addKey(key) end
local function release(key) emu:clearKey(key) end

callbacks:add("frame", function()
  if not start_frame then start_frame = emu:currentFrame() end
  local frame = emu:currentFrame() - start_frame

  if frame == 120 then shot("main")
  elseif frame == 140 then press(C.GBA_KEY.DOWN)
  elseif frame == 160 then release(C.GBA_KEY.DOWN)
  elseif frame == 180 then press(C.GBA_KEY.A)
  elseif frame == 200 then release(C.GBA_KEY.A)
  elseif frame == 260 then shot("reset")
  elseif frame == 280 then press(C.GBA_KEY.B)
  elseif frame == 300 then release(C.GBA_KEY.B)

  elseif frame == 340 then press(C.GBA_KEY.DOWN)
  elseif frame == 360 then release(C.GBA_KEY.DOWN)
  elseif frame == 390 then press(C.GBA_KEY.DOWN)
  elseif frame == 410 then release(C.GBA_KEY.DOWN)
  elseif frame == 440 then press(C.GBA_KEY.A)
  elseif frame == 460 then release(C.GBA_KEY.A)
  elseif frame == 540 then shot("save")
  elseif frame == 560 then press(C.GBA_KEY.B)
  elseif frame == 580 then release(C.GBA_KEY.B)

  elseif frame >= 620 and frame < 820 then
    local phase = (frame - 620) % 50
    if phase == 0 then press(C.GBA_KEY.DOWN)
    elseif phase == 20 then release(C.GBA_KEY.DOWN)
    end
  elseif frame == 840 then press(C.GBA_KEY.A)
  elseif frame == 860 then release(C.GBA_KEY.A)
  elseif frame == 940 then shot("rtc")

  elseif frame >= 980 and frame < 1280 then
    local phase = (frame - 980) % 50
    if phase == 0 then press(C.GBA_KEY.RIGHT)
    elseif phase == 20 then release(C.GBA_KEY.RIGHT)
    end
  elseif frame == 1320 then shot("rtc-update-selected")
  elseif frame == 1350 then press(C.GBA_KEY.A)
  elseif frame == 1370 then release(C.GBA_KEY.A)
  elseif frame == 1450 then shot("rtc-updated-popup")
  elseif frame == 1490 then press(C.GBA_KEY.B)
  elseif frame == 1510 then release(C.GBA_KEY.B)

  elseif frame >= 1540 and frame < 1690 then
    local phase = (frame - 1540) % 50
    if phase == 0 then press(C.GBA_KEY.DOWN)
    elseif phase == 20 then release(C.GBA_KEY.DOWN)
    end
  elseif frame == 1710 then press(C.GBA_KEY.A)
  elseif frame == 1730 then release(C.GBA_KEY.A)
  elseif frame == 1810 then shot("savestates")
  elseif frame == 1830 then press(C.GBA_KEY.B)
  elseif frame == 1850 then release(C.GBA_KEY.B)

  elseif frame >= 1890 and frame < 2140 then
    local phase = (frame - 1890) % 50
    if phase == 0 then press(C.GBA_KEY.DOWN)
    elseif phase == 20 then release(C.GBA_KEY.DOWN)
    end
  elseif frame == 2160 then press(C.GBA_KEY.A)
  elseif frame == 2180 then release(C.GBA_KEY.A)
  elseif frame == 2260 then shot("cheats")
  elseif frame == 2280 then
    local marker = assert(io.open(output .. "complete.txt", "w"))
    marker:write("SuperR7 in-game menu demo completed\n")
    marker:close()
  end
end)
