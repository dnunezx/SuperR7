-- Copyright (C) 2026 Danny Nunez

local output = script.dir .. "/../artifacts/phase9-boot-logo-hardware/"
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

local shots = {
  [0] = "boot-00",
  [1] = "boot-01",
  [2] = "boot-02",
  [3] = "boot-03",
  [4] = "boot-04",
  [5] = "boot-05",
  [6] = "boot-06",
  [8] = "boot-08",
  [10] = "boot-10",
  [12] = "boot-12",
  [15] = "boot-15",
  [20] = "boot-20",
}

callbacks:add("frame", function()
  if not start_frame then start_frame = emu:currentFrame() end
  local frame = emu:currentFrame() - start_frame

  if shots[frame] then shot(shots[frame]) end
  if frame == 24 then
    local marker = assert(io.open(output .. "complete.txt", "w"))
    marker:write("mGBA SuperR7 boot-logo capture completed\n")
    marker:close()
  end
end)
