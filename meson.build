project(
    'komorebi',
    version: '3.0.0',
    meson_version: '>=0.64',
)

fs = import('fs')

# Internationalisation / Localisation. This is currently only used to configure the .desktop files;
i18n = import('i18n')
po_dir = meson.project_source_root() / 'po'
gettext_package = meson.project_name()
add_project_arguments('-DGETTEXT_PACKAGE=' + gettext_package, language: 'c')
i18n.gettext(
    meson.project_name(),
    args: '--directory=' + meson.project_source_root(),
)

py_mod = import('python')
py = py_mod.find_installation('python3')

# Set some variables
prefix = get_option('prefix')
bindir = get_option('bindir')
datadir = get_option('datadir')
pkgdatadir = join_paths(prefix, datadir, meson.project_name())
py_dir = join_paths(prefix, py.get_install_dir())

# Compile resources (images, etc,) so that they're built into the app.
# TODO: Generate separate resource bundles for Komorebi & Wallpaper Creator;
# There's enough overlap that I'm not going to do it right now, but it'd be more elegant.
gnome = import('gnome')
komorebiresources = gnome.compile_resources(
    'komorebi',
    'data/resources/komorebi.gresource.xml',
    source_dir: 'data/resources',
    gresource_bundle: true,
    install: true,
    install_dir: pkgdatadir,
)

dependencies = [
    dependency('glib-2.0', version: '>=2.38'),
    dependency('gobject-2.0'),
    dependency('gtk+-3.0', version: '>=3.14'),
    dependency('gee-0.8'),
    dependency('clutter-gtk-1.0'),
    dependency('clutter-1.0'),
    dependency('clutter-gst-3.0'),
]

webkit_dep = dependency('webkitgtk-4.1', required: false)
if not webkit_dep.found()
    webkit_dep = dependency('webkitgtk-4.0')
endif

install_data(
    ['komorebi.py', 'komorebi-wallpaper-creator.py'],
    rename: ['komorebi', 'komorebi-wallpaper-creator'],
    install_dir: bindir,
)

subdir('data')
subdir('komorebi')
