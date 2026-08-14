-- Copyright (C) 2026 Danny Nunez (dnunezx)

local output = script.dir .. "/../artifacts/phase5-v3/"
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

  if frame == 120 then press(C.GBA_KEY.R)
  elseif frame == 125 then release(C.GBA_KEY.R)
  elseif frame == 180 then shot("tools")

  elseif frame == 185 then press(C.GBA_KEY.DOWN)
  elseif frame == 190 then release(C.GBA_KEY.DOWN)
  elseif frame == 205 then press(C.GBA_KEY.A)
  elseif frame == 210 then release(C.GBA_KEY.A)
  elseif frame == 260 then shot("interface")
  elseif frame == 280 then press(C.GBA_KEY.B)
  elseif frame == 285 then release(C.GBA_KEY.B)

  elseif frame == 305 then press(C.GBA_KEY.DOWN)
  elseif frame == 310 then release(C.GBA_KEY.DOWN)
  elseif frame == 325 then press(C.GBA_KEY.A)
  elseif frame == 330 then release(C.GBA_KEY.A)
  elseif frame == 380 then shot("settings-start")

  elseif frame >= 400 and frame < 580 then
    local phase = (frame - 400) % 10
    if phase == 0 then press(C.GBA_KEY.DOWN)
    elseif phase == 4 then release(C.GBA_KEY.DOWN)
    end
  elseif frame == 590 then press(C.GBA_KEY.DOWN)
  elseif frame == 595 then release(C.GBA_KEY.DOWN)
  elseif frame == 610 then shot("settings-save")
  elseif frame == 630 then press(C.GBA_KEY.B)
  elseif frame == 635 then release(C.GBA_KEY.B)

  elseif frame == 655 then press(C.GBA_KEY.DOWN)
  elseif frame == 660 then release(C.GBA_KEY.DOWN)
  elseif frame == 675 then press(C.GBA_KEY.A)
  elseif frame == 680 then release(C.GBA_KEY.A)
  elseif frame == 730 then shot("info-superr7")
  elseif frame == 750 then press(C.GBA_KEY.A)
  elseif frame == 755 then release(C.GBA_KEY.A)
  elseif frame == 790 then shot("info-flash")
  elseif frame == 810 then press(C.GBA_KEY.A)
  elseif frame == 815 then release(C.GBA_KEY.A)
  elseif frame == 850 then shot("info-patch-db")
  elseif frame == 870 then press(C.GBA_KEY.A)
  elseif frame == 875 then release(C.GBA_KEY.A)
  elseif frame == 910 then shot("info-sd-card")
  elseif frame == 930 then
    local marker = io.open(output .. "complete.txt", "w")
    marker:write("mGBA Phase 5 v3 demo completed\n")
    marker:close()
  end
end)
