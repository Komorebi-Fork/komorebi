{
  lib,
  stdenv,
  fetchFromGitHub,
  meson,
  vala,
  pkg-config,
  glib,
  gtk3,
  libgee,
  webkitgtk_4_1,
  clutter-gtk,
  clutter-gst,
  ninja,
  wrapGAppsHook3,
  testers,
  pkgs,
}:

stdenv.mkDerivation (finalAttrs: {
  pname = "komorebi";
  version = "3.0.0";

  src = lib.fileset.toSource {
    root = ./.;
    fileset = lib.fileset.unions [
      ./data
      ./komorebi
      ./screenshots
      ./komorebi.py
      ./komorebi-wallpaper-creator.py
      ./komorebi.spec
      ./meson.build
    ];
  };

  nativeBuildInputs = [
    meson
    vala
    pkg-config
    ninja
    wrapGAppsHook3
  ];

  buildInputs = [
    glib
    gtk3
    libgee
    webkitgtk_4_1
    clutter-gtk
    clutter-gst
    (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
       pygobject3  
    ]))
  ];

  postFixup = ''
    wrapProgram $out/bin/komorebi \
      --prefix PYTHONPATH : $out/lib/python3.13/site-packages
    wrapProgram $out/bin/komorebi-wallpaper-creator \
      --prefix PYTHONPATH : $out/lib/python3.13/site-packages
  '';

  passthru.tests.version = testers.testVersion { package = finalAttrs.finalPackage; };

  meta = {
    description = "Beautiful and customizable wallpaper manager for Linux";
    homepage = "https://github.com/Komorebi-Fork/komorebi";
    license = lib.licenses.gpl3Only;
    maintainers = [ ];
    platforms = lib.platforms.linux;
  };
})
