<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# makepkg -si

==> Making package: webots-bin 2025a-1 (Wed 06 May 2026 07:46:13 PM CEST)
==> Checking runtime dependencies...
==> Installing missing dependencies...
[sudo] password for roel:
error: target not found: freeimage>=3.15.4
==> ERROR: 'pacman' failed to install missing dependencies.
==> Missing dependencies:
-> freeimage>=3.15.4
-> zziplib>=0.13.62
==> ERROR: Could not resolve all dependencies.
❯

    ~/CTAI/IRP/webots-bin    master ?1 

`makepkg` is failing because `webots-bin` depends on packages that are not available in your enabled Arch repos, and at least `freeimage` was removed from Arch/extra and is now only available through AUR or a replacement AUR package. `zziplib` is still in `extra`, so the dependency problem is most likely repo sync/order plus the missing `freeimage` provider.[^1_1][^1_2][^1_3]

## What to do

1. Refresh your package databases first:
```bash
sudo pacman -Syu
```

2. Check whether your mirrorlists are current, then install the repo package that still exists:
```bash
sudo pacman -S zziplib
```

`zziplib` is available in Arch `extra` as version 0.13.80-1.[^1_2]

3. For `freeimage`, install an AUR provider instead of the old repo package. The AUR page notes that the original `freeimage` package was dropped and points to a maintained fork; another Arch thread notes `freeimage-vpinball-git` is being used as a provider.[^1_4][^1_1]
4. After the dependency is installed, rerun:
```bash
makepkg -si
```


## Likely fix

The fastest path is usually:

```bash
sudo pacman -Syu zziplib
# then install an AUR provider for freeimage, such as freeimage-vpinball-git
makepkg -si
```

`webots-bin` explicitly lists `freeimage` as an AUR dependency, so `makepkg` cannot solve it from official repos alone.[^1_3]

## Why this happens

Your error means pacman could not find a package named `freeimage>=3.15.4` in the repositories it knows about. That happens when a package has been removed from Arch repos or when your package databases are out of date relative to the PKGBUILD’s dependency names.[^1_5][^1_1]

Would you like me to help you patch the PKGBUILD so it depends on the currently available `freeimage` provider?
<span style="display:none">[^1_10][^1_11][^1_12][^1_13][^1_14][^1_15][^1_16][^1_17][^1_18][^1_6][^1_7][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://aur.archlinux.org/packages/freeimage

[^1_2]: https://archlinux.org/packages/extra/x86_64/zziplib/

[^1_3]: https://aur.archlinux.org/packages/webots-bin

[^1_4]: https://bbs.archlinux.org/viewtopic.php?id=307499

[^1_5]: https://bbs.archlinux.org/viewtopic.php?id=206594

[^1_6]: https://security.archlinux.org/package/zziplib

[^1_7]: https://aur.archlinux.org/packages/lib32-freeimage

[^1_8]: https://forum.pine64.org/showthread.php?tid=15636\&pid=104411

[^1_9]: https://bbs.archlinux.org/viewtopic.php?id=23456

[^1_10]: https://sourceforge.net/projects/zziplib/files/zziplib13/0.13.62/zziplib-0.13.62.tar.bz2/download

[^1_11]: https://wiki.archlinux.org/title/Makepkg

[^1_12]: https://packages.msys2.org/packages/mingw-w64-x86_64-freeimage

[^1_13]: https://aur.archlinux.org/packages/lib32-freeimage?O=10

[^1_14]: https://aur.archlinux.org/packages/webots-nightly

[^1_15]: https://linux-packages.com/arch-linux/package/freeimage

[^1_16]: https://www.reddit.com/r/archlinux/comments/tm79jf/what_very_basic_packages_arent_included_in_arch/

[^1_17]: https://cyberbotics.com/doc/guide/samples-community-projects?version=R2023a

[^1_18]: https://www.youtube.com/watch?v=kGubIjUVM-E

