# Maintaining this fork

This repo tracks `owendswang/ps5-webkit-autoloader-esp32` and adds the
0.96" LCD display support on top of it (SSID shown as "PS5 Master Key",
plus IP/WiFi/password on screen).

## Syncing upstream changes

```sh
git fetch upstream
git merge upstream/main
```

If upstream touched a file we've customized (currently: `esp32-arduino.ino`,
`Makefile`, `install-deps.sh`, `.gitignore`), git will flag a conflict.
Resolve it by keeping both sides' changes — never just take one side
wholesale, since upstream fixes and our LCD code both need to survive.

Once resolved:

```sh
git add <resolved files>
git commit -m "Merge upstream <version>, keep LCD display"
make s3-lcd   # confirm the existing display build still works
make s3-tdongle
make s3
git push
```

(First-time setup, if `upstream` isn't added yet:)
```sh
git remote add upstream https://github.com/owendswang/ps5-webkit-autoloader-esp32.git
```

## Tagging a release

Match upstream's version tag and append `_display`, e.g. if upstream
released `v0.6.1-0`, tag this repo as:

```sh
git tag v0.6.1-0_display
git push origin v0.6.1-0_display
```

Pushing a `v*` tag triggers `.github/workflows/build-lcd.yml`, which
checks the display build selection, builds both display variants and plain S3,
and attaches these two display images to an auto-created GitHub Release:

- `esp32-arduino.s3.merged-lcd-<tag>.bin` — Pocket-Dongle-S3 (existing filename)
- `esp32-arduino.tdongle-s3.merged-<tag>.bin` — LILYGO T-Dongle-S3

## Local build (WSL/Ubuntu)

```sh
sed -i 's/\r$//' *.sh Makefile
chmod +x *.sh prepare-data.sh
git submodule update --init --recursive
./install-deps.sh
make s3-lcd
make s3-tdongle
```

Output: `build/lcd/s3/esp32-arduino.s3.merged.bin`

T-Dongle-S3 output: `build/tdongle-s3/s3/esp32-arduino.tdongle-s3.merged.bin`

Run `python3 -m unittest discover -s tests -v` to check that both display
targets select distinct build directories and the correct board variant.
The initial T-Dongle-S3 build was flashed and visually checked on hardware.
Repeat the screen check when changing display initialization or layout.
