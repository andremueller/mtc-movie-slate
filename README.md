MMC Format

F0 7F <Device-ID> <Sub-ID#1> [<Sub-ID#2> [<parameters>]] F7

Record

F07F7F06440601203B380000F7
F0 7F 7F 06 44 06 01 20 3B 38 00 00 F7
deviceID = 7F (all devices, channel)
subId1 = 06 (MMC Machine Control Command)
subId2 = command

Start
F0 7F 7F 06 44 06 01 21 00 1B 16 00 F7
F0 7F 7F 06 44 06 01 21 00 08 0B 00 F7
F0 7F 7F 06 44 06 01 21 00 02 09 00 F7

Stop
F0 7F 7F 06 44 06 01 21 00 04 15 00 F7
F0 7F 7F 06 44 06 01 21 00 09 15 00 F7

Record
F0 7F 7F 06 44 06 01 20 3B 3A 00 00 F7
F0 7F 7F 06 44 06 01 21 00 06 00 00 F7

RECEIVE    | ENDPOINT(TouchOSC) TYPE(NOTE_ON) CHANNEL(2) DATA1(24) DATA2(0)
RECEIVE    | ENDPOINT(TouchOSC) TYPE(NOTE_ON) CHANNEL(2) DATA1(25) DATA2(127)
RECEIVE    | ENDPOINT(TouchOSC) TYPE(NOTE_ON) CHANNEL(2) DATA1(25) DATA2(0)


## Detect Bonjour Services

``````bash
dns-sd -B _osc._udp
```

In a second step you can find out more information on the given instance using

```bash
dns-sd -L "My-iPhone" _osc._tcp local
```
