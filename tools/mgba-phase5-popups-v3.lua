-- Copyright (C) 2026 Danny Nunez

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
  {120, C.GBA_KEY.A},
  {190, C.GBA_KEY.R},
  {260, C.GBA_KEY.R},
  {330, C.GBA_KEY.B},
  {340, C.GBA_KEY.B},
  {350, C.GBA_KEY.DOWN}, {365, C.GBA_KEY.DOWN},
  {380, C.GBA_KEY.DOWN}, {395, C.GBA_KEY.DOWN},
  {410, C.GBA_KEY.DOWN}, {425, C.GBA_KEY.DOWN},
  {445, C.GBA_KEY.A},
  {520, C.GBA_KEY.B},
  {540, C.GBA_KEY.SELECT},
  {610, C.GBA_KEY.B},
  {630, C.GBA_KEY.DOWN},
  {645, C.GBA_KEY.A},
  {720, C.GBA_KEY.B},
  {740, C.GBA_KEY.R},
  {760, C.GBA_KEY.DOWN}, {775, C.GBA_KEY.DOWN},
  {790, C.GBA_KEY.DOWN}, {805, C.GBA_KEY.DOWN},
  {820, C.GBA_KEY.DOWN}, {835, C.GBA_KEY.DOWN},
  {855, C.GBA_KEY.A},
  {930, C.GBA_KEY.DOWN},
  {990, C.GBA_KEY.B},
  {1010, C.GBA_KEY.UP}, {1025, C.GBA_KEY.UP},
  {1040, C.GBA_KEY.UP}, {1055, C.GBA_KEY.UP},
  {1075, C.GBA_KEY.A},
  {1095, C.GBA_KEY.DOWN}, {1110, C.GBA_KEY.DOWN},
  {1125, C.GBA_KEY.DOWN}, {1140, C.GBA_KEY.DOWN},
  {1155, C.GBA_KEY.DOWN}, {1170, C.GBA_KEY.DOWN},
  {1185, C.GBA_KEY.DOWN}, {1200, C.GBA_KEY.DOWN},
  {1215, C.GBA_KEY.DOWN}, {1230, C.GBA_KEY.DOWN},
  {1245, C.GBA_KEY.DOWN},
  {1265, C.GBA_KEY.A},
  {1340, C.GBA_KEY.RIGHT},
  {1400, C.GBA_KEY.B},
  {1420, C.GBA_KEY.DOWN}, {1435, C.GBA_KEY.DOWN},
  {1450, C.GBA_KEY.DOWN}, {1465, C.GBA_KEY.DOWN},
  {1480, C.GBA_KEY.DOWN},
  {1500, C.GBA_KEY.A},
  {1580, C.GBA_KEY.B},
}

local shots = {
  [170] = "launch-quick",
  [240] = "launch-options",
  [310] = "launch-advanced",
  [500] = "save-actions",
  [590] = "file-actions",
  [700] = "firmware-update",
  [910] = "confirm-no",
  [970] = "confirm-yes",
  [1320] = "rtc-year",
  [1380] = "rtc-month",
  [1560] = "settings-alert",
}

callbacks:add("frame", function()
  if not start_frame then start_frame = emu:currentFrame() end
  local frame = emu:currentFrame() - start_frame

  for _, tap in ipairs(taps) do
    if frame == tap[1] then emu:addKey(tap[2])
    elseif frame == tap[1] + 5 then emu:clearKey(tap[2])
    end
  end

  if shots[frame] then shot(shots[frame]) end
  if frame == 1600 then
    local marker = assert(io.open(output .. "complete.txt", "w"))
    marker:write("mGBA Phase 5 popup demo completed\n")
    marker:close()
  end
end)
