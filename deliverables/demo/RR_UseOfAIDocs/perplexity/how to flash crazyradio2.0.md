<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# how to flash crazyradio2.0

To flash a **Crazyradio 2.0**, put it in bootloader mode by holding its button while plugging it into USB, then drag and drop the `.UF2` firmware file onto the `Crazyradio2` drive that appears. The radio will reboot after the copy finishes, and the drive will disappear.[^1_2][^1_3]

## Steps

1. Unplug the Crazyradio 2.0.
2. Hold the button on the dongle.
3. Plug it into USB while still holding the button.
4. Wait for the LED to turn red and pulse slowly; the device should appear as a USB drive named `Crazyradio2`.[^1_2]
5. Copy the firmware `.UF2` file to that drive.
6. Wait for the radio to restart; the LED should stop being red and the drive should vanish.[^1_3][^1_2]

## Useful notes

- The current firmware backup can be copied from `CURRENT.UF2` before flashing.[^1_2]
- If you prefer command line flashing during development, Bitcraze also documents a serial DFU method using `adafruit-nrfutil`.[^1_2]
- The older Crazyradio PA flashing instructions are different and do **not** apply to Crazyradio 2.0.[^1_4]


## If it fails

If the drive does not appear, replug the device and try bootloader mode again. If the radio boots but behaves oddly after flashing, Bitcraze notes that reflashing the latest firmware can fix known bad releases.[^1_7][^1_3]

Would you like the exact commands for building a custom firmware `.UF2` too?
<span style="display:none">[^1_1][^1_10][^1_5][^1_6][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://www.youtube.com/watch?v=LGqCM9dPIPo

[^1_2]: https://www.bitcraze.io/documentation/repository/crazyradio2-firmware/main/building-and-flashing/flash/

[^1_3]: https://www.bitcraze.io/documentation/tutorials/getting-started-with-crazyradio-2-0/

[^1_4]: https://www.bitcraze.io/documentation/repository/crazyradio-firmware/master/building/building_flashing/

[^1_5]: https://github.com/bitcraze/crazyradio2-bootloader

[^1_6]: https://www.bitcraze.io/documentation/repository/crazyradio-firmware/master/building/programming/

[^1_7]: https://github.com/orgs/bitcraze/discussions/1688

[^1_8]: https://www.youtube.com/watch?v=M_m4vA9gRVs

[^1_9]: https://github.com/bitcraze/crazyradio2-firmware

[^1_10]: https://www.reddit.com/r/sdr/comments/1kmovn9/custom_firmware_for_a_crazyradio_20/

