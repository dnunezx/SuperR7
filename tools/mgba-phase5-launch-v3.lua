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
  {120, C.GBA_KEY.A},
  {190, C.GBA_KEY.DOWN},
  {250, C.GBA_KEY.DOWN},
  {310, C.GBA_KEY.DOWN},
  {370, C.GBA_KEY.A},
  {440, C.GBA_KEY.B},
  {500, C.GBA_KEY.R},
  {570, C.GBA_KEY.R},
  {640, C.GBA_KEY.B},
}

local shots = {
  [170] = "launch-quick",
  [230] = "launch-quick-favorite",
  [290] = "launch-quick-options",
  [350] = "launch-quick-details",
  [420] = "launch-details",
  [550] = "launch-options",
  [620] = "launch-advanced",
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
  if frame == 680 then
    local marker = assert(io.open(output .. "launch-complete.txt", "w"))
    marker:write("mGBA Phase 5 launch refinement completed\n")
    marker:close()
  end
end)
