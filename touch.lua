local delay = 200 -- the maximum elapsed time between taps
local last = 0

function onValueChanged(field)
  local tapped=false
  if(not self.values.touch) then
    local now = getMillis()
    if(now - last < delay) then
      print('double tap!')
      last = 0
    else
      last = now
      tapped = true
    end
  end
  if tapped then
    -- MMC Play command (System Exclusive)
    local mmcStop = {0xF0, 0x7F, 0x7F, 0x06, 0x01, 0xF7} -- Example MMC Stop command
       sendMIDI(mmcStop) -- Sending the message
        print("Sending MMC Stop")
  end
end