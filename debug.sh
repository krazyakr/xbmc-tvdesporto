# ~/.bashrc

mkdir tmp
mkdir tmp/plugin.video.tvdesporto
cp -r * tmp/plugin.video.tvdesporto/
rm -r tmp/plugin.video.tvdesporto/build
rm tmp/plugin.video.tvdesporto/*.sh
rm tmp/plugin.video.tvdesporto/*~
rm -r tmp/plugin.video.tvdesporto/tmp
cd tmp
cp -r plugin.video.tvdesporto ~/.xbmc/addons/
cd ..
rm -r tmp


