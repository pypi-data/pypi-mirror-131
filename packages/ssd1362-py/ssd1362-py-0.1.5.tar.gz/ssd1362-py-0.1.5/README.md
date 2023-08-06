# ssd1362

- oled(ssd1363) controller (tested with jetson nano)
- This module use linux's spidev, g4l(gpio), numpy
- link : (https://gitlab.com/telelian/peripheral-library/ssd1362.git)

## Usage

### class

- Ssd1362(spibus, spidev, io_dc)

  - parameters

    - spibus, spidev
      - spi device info
      - looks like /dev/spidev{spibus}.{device}

    - io_dc
      - data/command select pin number for ssd1362
      - check your schematics

### methods

- Ssd1362.loadframe(buf)

  - parameters

    - buf
      - load buffer for oled's pixel
      - width : 256, height : 64
      - list[height][width]
      - pixel's gray level : 0 ~ 255 (convert to 16 level in show)

- Ssd1362.show(gray_level)

  - parameters

    - gray_level
      - ssd1362's pixel gray scale
      - min:0 ~ max:15
