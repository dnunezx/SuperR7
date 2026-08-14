-- Copyright (C) 2026 Danny Nunez (dnunezx)

local output = script.dir .. "/../artifacts/phase5-popups-v3/"
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

local taps = {
  {120, C.GBA_KEY.DOWN}, {180, C.GBA_KEY.DOWN},
  {240, C.GBA_KEY.DOWN}, {300, C.GBA_KEY.DOWN},
  {360, C.GBA_KEY.DOWN}, {420, C.GBA_KEY.DOWN},
  {500, C.GBA_KEY.A},
  {580, C.GBA_KEY.B},
  {640, C.GBA_KEY.DOWN},
  {700, C.GBA_KEY.A},
  {780, C.GBA_KEY.B},
}

callbacks:add("frame", function()
  if not start_frame then start_frame = emu:currentFrame() end
  local frame = emu:currentFrame() - start_frame

  for _, tap in ipairs(taps) do
    if frame == tap[1] then emu:addKey(tap[2])
    elseif frame == tap[1] + 5 then emu:clearKey(tap[2])
    end
  end

  if frame == 560 then shot("save-actions") end
  if frame == 760 then shot("firmware-update") end
  if frame == 800 then
    local marker = assert(io.open(output .. "files-complete.txt", "w"))
    marker:write("mGBA Phase 5 file popup demo completed\n")
    marker:close()
  end
end)
