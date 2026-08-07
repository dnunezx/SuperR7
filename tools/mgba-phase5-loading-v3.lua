-- Copyright (C) 2026 Danny Nunez

local output = script.dir .. "/../artifacts/phase5-loading-v3/"
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
  {170, C.GBA_KEY.A},
  {240, C.GBA_KEY.SELECT},
  {280, C.GBA_KEY.SELECT},
  {300, C.GBA_KEY.SELECT},
  {350, C.GBA_KEY.B},
}

local shots = {
  [225] = "loading-electric-blue",
  [265] = "loading-mutant-green",
  [325] = "loading-chrome-silver",
  [385] = "loading-returned-to-launch",
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
  if frame == 400 then
    local marker = assert(io.open(output .. "complete.txt", "w"))
    marker:write("mGBA Phase 5 themed loading demo completed\n")
    marker:close()
  end
end)
