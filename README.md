<p align="center"><img src="https://raw.githubusercontent.com/Komorebi-Fork/komorebi/master/screenshots/komorebi-icon.png" width="130"></p>
<h2 align="center">Komorebi - Animated Wallpapers for Linux</h2>
<p align="center">(n) sunlight filtering through trees.</p>

<p align="center">
	<a href="http://www.kernel.org"><img alt="Platform (GNU/Linux)" src="https://img.shields.io/badge/platform-GNU/Linux-blue.svg"></a>
	<a href="https://travis-ci.org/Komorebi-Fork/komorebi"><img alt="Build Status" src="https://travis-ci.org/Komorebi-Fork/komorebi.svg?branch=master"></a>
</p>

<p align="center">
<a href="http://www.youtube.com/watch?feature=player_embedded&v=NvfRy5qMsos
" target="_blank"><img src="http://img.youtube.com/vi/NvfRy5qMsos/0.jpg"
alt="Komorebi Demo" width="240" height="180" border="10" /><br>Watch demo</a>
</p>

## What is Komorebi?

Komorebi is an animated wallpaper manager for all Linux platforms.
It provides you with fully customisable image, video, and web page wallpapers that you can tweak at any time!

This project is a Python rewrite and continuation of the original [Komorebi](https://github.com/cheesecakeufo/komorebi) by [@cheesecakeufo](https://github.com/cheesecakeufo).

![s1](https://raw.githubusercontent.com/Komorebi-Fork/komorebi/master/screenshots/collage.jpg)

## Installing

Komorebi has been tested on:

- **Gentoo**

Please test on your own distro and submit a pull request with your distro's instructions!

### Debian and derivatives (Ubuntu, Deepin, Elementary OS, Pop! OS, etc...)

> [!TIP]
> Users interested in packaging Komorebi for Debian-based distros are encouraged to do so - Please reach out for access to our legacy (vala) packaging repo!

If you'd like to compile Komorebi from source instead, you'll need to install the following dependencies:

> [!Note]
> If ``libwebkit2gtk-4.1-dev`` is unavailable, try installing ``libwebkit2gtk-4.0-dev`` instead
```bash
sudo apt install meson valac libgtk-3-dev libgee-0.8-dev libclutter-gtk-1.0-dev libclutter-1.0-dev libwebkit2gtk-4.1-dev libclutter-gst-3.0-dev
```

and jump to the [compiling section](#compiling).

### Fedora / OpenSUSE

Grab the appropriate rpm from [here](https://build.opensuse.org/package/show/home%3ANNowakowski/Komorebi-Fork), and install it.

```bash
sudo rpm -ivh komorebi-2.2.0-9.1.x86_64.rpm
```

If you'd like to compile Komorebi from source instead, you'll need to install the following dependencies:

```bash
sudo dnf install meson vala gcc-c++ gtk3-devel clutter-devel clutter-gtk-devel clutter-gst3-devel webkit2gtk3-devel libgee-devel gstreamer1-libav
```

and jump to the [compiling section](#compiling).

### Arch Linux and derivatives (Manjaro, etc...)

Install from the [AUR](https://aur.archlinux.org/packages/komorebi/):

```bash
yay -S komorebi
```

or grab the required dependencies:

```bash
sudo pacman -S meson vala gtk3 clutter clutter-gtk clutter-gst libgee
```

and jump to the [compiling section](#compiling).

### Gentoo

There is an ebuild available in Kangie's overlay. You can add the overlay and install Komorebi with the following commands:

```bash
eselect repository add kangie git https://github.com/Kangie/kangie-tools.git
emerge --sync
emerge -av x11-misc/komorebi
```

## Compiling

Run the following:

```bash
git clone https://github.com/Komorebi-Fork/komorebi.git
cd komorebi
meson setup builddir --python.bytecompile=2
cd builddir && meson compile
```

To install the compiled package:

```bash
meson install
```

> [!NOTE]
> The default installation prefix is `/usr/local`. If you want to install it in a different location, you can specify it with `meson setup builddir --prefix=/your/prefix`.
>
> This is important, as /usr/local/bin is not in the default PATH for non-root users on most distros and, in particular, the `PYTHONPATH` may not include `/usr/local/lib/python3.x/site-packages`.

Users are encouraged to install Komorebi from their distro's package manager if available (or request it to be packaged!)

## Using Komorebi

Simply run `komorebi`, or open your application launcher and look for **Komorebi**.

Komorebi displays behind all other windows, so you may not notice anything if you have a fullscreen application running.

Optional arguments:

- `--single-screen`: forces Komorebi to run on the main screen only
- `version` or `--version`: prints current version

### Change wallpaper & desktop preferences

Komorebi's preferences (including the wallpaper selector) can be accessed from the bubble menu, available by right-clicking on the desktop.

![s1](https://raw.githubusercontent.com/Komorebi-Fork/komorebi/master/screenshots/preferences.jpg)

### Create custom wallpapers

Komorebi provides a simple tool to create your own wallpapers! Simply run `komorebi-wallpaper-creator` or open your application launcher and search for **Wallpaper Creator**.

![s1](https://raw.githubusercontent.com/Komorebi-Fork/komorebi/master/screenshots/wallpaper_creator.jpg)

You can use either an image, a video, or a web page as a wallpaper and you have many different options to customize your very own wallpaper!

## Uninstalling

If you manually installed Komorebi, run the following on the cloned repository folder:

```bash
cd builddir
sudo ninja uninstall
```

If you didn't compile Komorebi from source, you can uninstall it through your package manager in the same way you would uninstall any other package.

# Contributing

We welcome contributions from everyone! Please submit a pull request or raise an issue if you'd like to help out.

## Reporting bugs

Please report bugs on the [issue tracker](https://github.com/Komorebi-Fork/komorebi/issues). Remember to seach for existing issues before creating a new one!

## Translating

We would love to have Komorebi translated into as many languages as possible! If you'd like to help, please raise an issue for guidance.

# Questions? Issues?

### Komorebi is slow. What can I do about it?

Komorebi includes support for video wallpapers that might slow your computer down. We've put together a few tips that you can use to increase performance on the [wiki](https://github.com/Komorebi-Fork/komorebi/wiki/Improve-video-wallpapers-performance).

You can also disable support for video wallpapers altogether in 'Desktop Preferences' → uncheck 'Enable Video Wallpapers'.

_note: you need to quit and re-open Komorebi after changing this option_

### Thanks To:

Pete Lewis ([@PJayB](https://github.com/PJayB)) for adding multi-monitor support.
