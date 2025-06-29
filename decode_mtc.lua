-- Script to receive and display MIDI Timecode in a TouchOSC Label

-- Initialize variables to store timecode components
local hours = 0
local minutes = 0
local seconds = 0
local frames = 0
local frame_rate = 30 -- Set your project's frame rate here (24, 25, 29.97, or 30)

-- A table to hold the 8 pieces of the MTC quarter-frame message
local mtc_pieces = {}

-- This function is called whenever a MIDI message is received
function onReceiveMIDI(message, connection)
  -- Check if the message is a MIDI Timecode Quarter Frame (Status 0xF1)
  if message[1] == 0xF1 then
    local piece_index = bit32.band(bit32.rshift(message[2], 4), 0x07)
    local piece_value = bit32.band(message[2], 0x0F)

    mtc_pieces[piece_index] = piece_value

    -- Once we have all 8 pieces, we can assemble the timecode
    if piece_index == 7 then
      -- Frames
      local frames_lsb = mtc_pieces[0]
      local frames_msb = mtc_pieces[1]
      frames = frames_lsb + (frames_msb * 16)

      -- Seconds
      local seconds_lsb = mtc_pieces[2]
      local seconds_msb = mtc_pieces[3]
      seconds = seconds_lsb + (seconds_msb * 16)

      -- Minutes
      local minutes_lsb = mtc_pieces[4]
      local minutes_msb = mtc_pieces[5]
      minutes = minutes_lsb + (minutes_msb * 16)

      -- Hours and Frame Rate
      local hours_lsb = mtc_pieces[6]
      local hours_msb_and_rate = mtc_pieces[7]
      local hours_msb = bit32.band(hours_msb_and_rate, 0x01)
      hours = hours_lsb + (hours_msb * 16)
      
      -- You can uncomment the following lines to attempt to read the frame rate from the MTC message
      -- local rate_bits = (hours_msb_and_rate >> 1) & 0x03
      -- if rate_bits == 0 then frame_rate = 24 end
      -- if rate_bits == 1 then frame_rate = 25 end
      -- if rate_bits == 2 then frame_rate = 29.97 end
      -- if rate_bits == 3 then frame_rate = 30 end

      -- Format the timecode string with leading zeros
      local timecode_string = string.format("%02d:%02d:%02d:%02d", hours, minutes, seconds, frames)

      -- Update the text of this label
      self.values.text = timecode_string
    end
  end

  -- Handle Full Frame messages (System Exclusive)
  if message[1] == 0xF0 and message[2] == 0x7F and message[4] == 0x01 and message[5] == 0x01 then
    hours = bit32.band(message[6], 0x1F)
    minutes = message[7]
    seconds = message[8]
    frames = message[9]

    local timecode_string = string.format("%02d:%02d:%02d:%02d", hours, minutes, seconds, frames)
    self.values.text = timecode_string
  end
end