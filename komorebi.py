#!/usr/bin/env python3

import argparse
import os
import gi
import signal
import sys
import logging

gi.require_versions({
    'Gtk': '3.0',
    'GObject': '2.0',
    'GtkClutter': '1.0',
    'Clutter': '1.0',
    'ClutterGst': '3.0',
    'Gdk': '3.0',
    'GdkPixbuf': '2.0',
    'Gst': '1.0',
})

try:
    gi.require_version('WebKit2', '4.0')
except ValueError:
    # If 4.0 is not available, try 4.1
    try:
        gi.require_version('WebKit2', '4.1')
    except ValueError:
        print("Neither WebKit2 version 4.0 nor 4.1 is available.")
        sys.exit(1)

from komorebi.screen import Screen
import komorebi.utilities
from komorebi.settings import ConfigKeys, Settings
from komorebi.preferences_window import PreferencesWindow
from gi.repository import Gio, GLib, Gtk, GtkClutter, Gdk, Gst, Clutter


def check_desktop_wayland():
    return not (os.environ.get('XDG_SESSION_TYPE') == 'wayland' or os.environ.get('WAYLAND_DISPLAY'))


def main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version',
                        action='version',
                        help='show current version',
                        version=f'Version: {komorebi.__version__}\nMaintained by: Komorebi Team')
    parser.add_argument('-ss', '--single-screen',
                        action='store_true',
                        help='force komorebi to run only on the main screen')
    parser.add_argument('-l', '--log',
                        type=str,
                        choices=['NORMAL', 'INFO', 'DEBUG'],
                        default='NORMAL',
                        help="set logging level for komorebi")
    return parser


def _on_destroy(*args):
    logging.info("Quitting...")
    Clutter.main_quit()


def main():
    print(f'Welcome to {komorebi.__package_name__}')

    # Handle Ctrl-C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Parse the arguments
    parser = main_parser()
    args = parser.parse_args()

    # Setup logger
    log_level = logging.WARNING
    log_format = '[%(levelname)s]: %(message)s'

    if args.log:
        if args.log == 'INFO':
            log_level = logging.INFO
        elif args.log == 'DEBUG':
            log_level = logging.DEBUG
            log_format = '[%(levelname)s] (%(asctime)s): %(message)s'

    logging.basicConfig(format=log_format, level=log_level, datefmt='%H:%M:%S')

    # Ensure we are not on Wayland
    if not check_desktop_wayland():
        logging.info('Wayland detected. Wayland support is Experimental!')
        logging.info('Contribute to Komorebi and add the support! <3')

    # Work around Clutter bugs with more than one screen (one stage per monitor) on Mesa.
    # Must be set before Clutter is initialized.
    # - disable-clipped-redraws: clipped redraws make Cogl query GLX drawable attributes,
    #   which fails for our stage windows -> GLXBadDrawable crash (issues #18, #105).
    # - disable-culling: paint culling intermittently skips overlay actors (e.g. the desktop
    #   icons), making them flicker.
    if not args.single_screen:
        paint_flags = [f for f in os.environ.get('CLUTTER_PAINT', '').split(',') if f]
        for flag in ('disable-clipped-redraws', 'disable-culling'):
            if flag not in paint_flags:
                paint_flags.append(flag)
        os.environ['CLUTTER_PAINT'] = ','.join(paint_flags)

    # Initialize backends
    GtkClutter.init(sys.argv)
    logging.debug("GtkClutter initialized")

    Settings.load_settings()
    logging.debug("Configuration file read")

    logging.info('loading Gst')
    Gst.init(sys.argv)
    logging.debug('Gst initialized')

    # Load resources
    resource_path = os.path.join(komorebi.__package_datadir__, 'komorebi.gresource')
    resource = Gio.Resource.load(resource_path)
    Gio.resources_register(resource)

    display = Gdk.Display.get_default()

    def _get_monitor_count():
        return 1 if args.single_screen else display.get_n_monitors()

    logging.info(f"Monitor Count - {_get_monitor_count()}")

    komorebi.utilities.init_clipboard(display)

    # One Screen (window) per monitor; kept in sync with the monitor layout below
    screen_list = []

    # Setup some GTK properties
    main_settings = Gtk.Settings.get_default()
    main_settings.props.gtk_application_prefer_dark_theme = True
    main_settings.props.gtk_xft_antialias = 1
    main_settings.props.gtk_xft_rgba = "none"
    main_settings.props.gtk_xft_hintstyle = "slight"

    # Setup preferences window
    def _on_settings_changed(_, setting_key):
        logging.debug("Setting " + str(setting_key) + " changed!")
        if setting_key == ConfigKeys.WALLPAPER_NAME:
            for screen in screen_list:
                screen.load_wallpaper(Settings.wallpaper_name)
        elif setting_key == ConfigKeys.AUTOSTART:
            komorebi.utilities.toggle_autostart()
        else:
            for screen in screen_list:
                screen.on_settings_changed(setting_key)
        return True

    prefs_window = PreferencesWindow()
    prefs_window.connect('settings-changed', _on_settings_changed)

    # Setup screens
    def _on_settings_request_event(_, wallpaper_tab):
        prefs_window.show(wallpaper_tab)
        return True

    def _add_screen(monitor_index):
        screen = Screen(monitor_index)
        # Closing a screen window quits komorebi; keep the handler id so screens
        # removed because their monitor went away can be destroyed without quitting.
        screen.quit_handler = screen.connect("destroy", _on_destroy)
        screen.load_wallpaper(Settings.wallpaper_name)
        screen.fade_in()
        screen.connect('settings_requested', _on_settings_request_event)
        screen_list.append(screen)

    def _remove_screen(screen):
        screen.disconnect(screen.quit_handler)
        screen.unload()
        screen.destroy()
        screen_list.remove(screen)

    for i in range(_get_monitor_count()):
        _add_screen(i)

    # Follow monitor changes (plugging/unplugging, closing the laptop lid, rearranging).
    # A single change usually emits several signals, so wait for things to settle first.
    resync_source = None

    def _sync_screens():
        nonlocal resync_source
        resync_source = None

        monitor_count = _get_monitor_count()
        geometries = [display.get_monitor(i).get_geometry() for i in range(monitor_count)]
        if monitor_count == 0 or any(g.width == 0 or g.height == 0 for g in geometries):
            logging.info("Monitor layout not ready yet, retrying...")
            resync_source = GLib.timeout_add(1000, _sync_screens)
            return False

        logging.info(f"Monitor layout changed - {monitor_count} monitor(s), rebuilding screens")

        # Remove screens first: unloading a video wallpaper stops the shared player,
        # and reloading the remaining screens below starts it again.
        for screen in screen_list[monitor_count:]:
            _remove_screen(screen)

        for i, screen in enumerate(screen_list):
            screen.set_monitor(i)
            screen.load_wallpaper(Settings.wallpaper_name)

        for i in range(len(screen_list), monitor_count):
            _add_screen(i)

        return False

    def _on_monitors_changed(*_):
        nonlocal resync_source
        if resync_source is not None:
            GLib.source_remove(resync_source)
        resync_source = GLib.timeout_add(1000, _sync_screens)

    gdk_screen = display.get_default_screen()
    gdk_screen.connect('monitors-changed', _on_monitors_changed)
    gdk_screen.connect('size-changed', _on_monitors_changed)

    # Start Clutter backend
    logging.debug("Starting Clutter backend...")
    Clutter.main()


if __name__ == '__main__':
    main()
