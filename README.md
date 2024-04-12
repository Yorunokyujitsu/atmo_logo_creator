# Atmosphère splash & fatal logo Creator
* boot splash and fatal screen custom logo creation tool.
* Used with [switch-logo-patcher](https://github.com/friedkeenan/switch-logo-patcher) you can change all logos.

## ⬦ Image source
* **JPEG, JPG, PNG, BMP files** with name **splash** or **fatal** 
* splash image : Max size = 1280x720
* fatal image : 160x160 / **background color is `#393B4B (0x39C9)`**

## ⬦ How to use
1. Place png files named `splash` and `fatal` in the `\resources` folder.
2. run python scritps.
  - `output/stratosphere/boot/source/`**`boot_splash_screen_notext.inc`**
  - `output/stratosphere/fatal/source/`**`fatal_ams_logo.inc`**
3. **`startosphere`** folder copy > Atmosphère path paste.
4. build Atmosphère.
5. check boot screen logo & fatal error screen.

## ⬦ Restore images
1. Place `boot_splash_screen_notext.inc` or `fatal_ams_logo.inc` files in the `\restore` folder.
2. run python scripts.
  - `output` > **`splash.png`** or **`fatal.png`**

## ⬦ Install python library
```
pip install numpy pillow
```

## ⬦ Create include files

`boot_splash_screen_notext.inc`, `fatal_ams_logo.inc`
```
python .\scripts\create_logos.py
```

## ⬦ Restore include files to image

`splash.png`, `fatal.png`
```
python .\scripts\image_restore.py
```