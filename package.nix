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

  src = fetchFromGitHub {
    owner = "luozenan";
    repo = "nixos-komorebi";
    rev = "dc00496da23503eaff11087f5fc93de9af93923f";
    hash = "sha256-vLC6biUEidB5beKATMoPjPoPgFg1e5IHpku67JBbaHU=";
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

  passthru.tests.version = testers.testVersion { package = finalAttrs.finalPackage; };

  meta = {
    # webkitgtk_4_0 was removed
    broken = true;
    description = "Beautiful and customizable wallpaper manager for Linux";
    homepage = "https://github.com/Komorebi-Fork/komorebi";
    license = lib.licenses.gpl3Only;
    maintainers = [ ];
    platforms = lib.platforms.linux;
  };
})
