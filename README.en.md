# BoziDockCat

[中文](README.md) | English

BoziDockCat is a customized macOS desktop companion cat based on [Auwuua/DockCat](https://github.com/Auwuua/DockCat). The star is **Bozi** (波子), our Ragdoll cat.

Bozi rests, stretches, and walks along the Dock, and gently reminds you to drink water and take breaks. A Bozi asset pack is bundled by default.

## About Bozi

Bozi is a fluffy white Ragdoll with seal-point ears and face mask, bright blue eyes, and a bushy tail. Reference photos live in [`bozi/references/`](bozi/references/).

## Quick Start

Download `BoziDockCat.zip` from [Releases](https://github.com/genzuuuu/BoziDockCat/releases), unzip, and move `DockCat.app` to Applications.

### Build from Source

```bash
git clone https://github.com/genzuuuu/BoziDockCat.git
cd BoziDockCat
xcodebuild -project DockCatApp/DockCat.xcodeproj -scheme DockCat -configuration Debug -derivedDataPath DockCatApp/DerivedDataDebug build
open DockCatApp/DerivedDataDebug/Build/Products/Debug/DockCat.app
```

## Customize Bozi's Look

See [`CustomizationGuide/波子图片生成提示词.md`](CustomizationGuide/波子图片生成提示词.md) for Bozi-specific AI prompts, then run:

```bash
python3 scripts/process_bozi_assets.py
```

## Credits & License

Based on [DockCat](https://github.com/Auwuua/DockCat) under the PolyForm Noncommercial License. See [LICENSE.txt](LICENSE.txt).
