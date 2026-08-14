-- Copyright (C) 2026 Danny Nunez (dnunezx)

local output = script.dir .. "/../artifacts/favorites-v3/"
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
  {180, C.GBA_KEY.DOWN},
  {250, C.GBA_KEY.A},
  {330, C.GBA_KEY.B},
  {360, C.GBA_KEY.L},
  {390, C.GBA_KEY.L},
  {480, C.GBA_KEY.SELECT},
  {560, C.GBA_KEY.DOWN},
  {580, C.GBA_KEY.A},
}

local shots = {
  [230] = "launch-add",
  [310] = "launch-remove",
  [450] = "favorites-added",
  [540] = "favorites-remove-confirm",
  [650] = "favorites-empty",
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
    local marker = assert(io.open(output .. "complete.txt", "w"))
    marker:write("mGBA Favorites flow completed\n")
    marker:close()
  end
end)
