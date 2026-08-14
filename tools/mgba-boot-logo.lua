-- Copyright (C) 2026 Danny Nunez (dnunezx)

local output = script.dir .. "/../artifacts/boot-logo/"
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
  [0] = "boot-v2-00",
  [1] = "boot-v2-01",
  [2] = "boot-v2-02",
  [3] = "boot-v2-03",
  [4] = "boot-v2-04",
  [5] = "boot-v2-05",
  [6] = "boot-v2-06",
  [8] = "boot-v2-08",
  [10] = "boot-v2-10",
  [12] = "boot-v2-12",
  [15] = "boot-v2-15",
  [20] = "boot-v2-20",
}

callbacks:add("frame", function()
  if not start_frame then start_frame = emu:currentFrame() end
  local frame = emu:currentFrame() - start_frame

  if shots[frame] then shot(shots[frame]) end
  if frame == 24 then
    local marker = assert(io.open(output .. "complete-v2.txt", "w"))
    marker:write("mGBA SuperR7 boot-logo v2 capture completed\n")
    marker:close()
  end
end)
