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
    rev = "dbbc704ea6ca75d2cd05407652ce051bd2e47818";
    hash = "sha256-qiVfieW9j8uDe9ExKCcOAf7IZUufCl0NcZ1mB+iCXbo=";
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
