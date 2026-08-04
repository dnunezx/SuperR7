local output = script.dir .. "/../artifacts/cover-demo/"
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
    shot("browse-aurora-ready")
  elseif frame == 105 then
    press(C.GBA_KEY.DOWN)
  elseif frame == 110 then
    release(C.GBA_KEY.DOWN)
  elseif frame == 120 then
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
    press(C.GBA_KEY.L)
  elseif frame == 420 then
    release(C.GBA_KEY.L)
  elseif frame == 520 then
    shot("recent-aurora-ready")
  elseif frame == 530 then
    local marker = io.open(output .. "complete.txt", "w")
    marker:write("mGBA cover demo completed\n")
    marker:close()
  end
end)
