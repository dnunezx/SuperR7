local output = script.dir .. "/../artifacts/cover-demo/"
local start_frame = nil

local function shot(name)
  emu:screenshot(output .. name .. ".png")
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

  if frame == 60 then
    shot("browse-aurora-ready")
  elseif frame == 65 then
    press(C.GBA_KEY.DOWN)
  elseif frame == 66 then
    release(C.GBA_KEY.DOWN)
  elseif frame == 68 then
    shot("browse-checker-pending")
  elseif frame == 90 then
    shot("browse-checker-ready")
  elseif frame == 95 then
    shot("browse-checker-stable")
  elseif frame == 100 then
    press(C.GBA_KEY.DOWN)
  elseif frame == 101 then
    release(C.GBA_KEY.DOWN)
  elseif frame == 125 then
    shot("browse-missing")
  elseif frame == 130 then
    press(C.GBA_KEY.DOWN)
  elseif frame == 131 then
    release(C.GBA_KEY.DOWN)
  elseif frame == 155 then
    shot("browse-invalid")
  elseif frame == 160 then
    press(C.GBA_KEY.L)
  elseif frame == 161 then
    release(C.GBA_KEY.L)
  elseif frame == 185 then
    shot("recent-aurora-ready")
  elseif frame == 190 then
    local marker = io.open(output .. "complete.txt", "w")
    marker:write("mGBA cover demo completed\n")
    marker:close()
  end
end)
