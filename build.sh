# ~/.bashrc

rm build/*
mkdir tmp
mkdir tmp/plugin.video.tvdesporto
cp -r source/* tmp/plugin.video.tvdesporto/
#rm -r tmp/plugin.video.tvdesporto/build
#rm tmp/plugin.video.tvdesporto/*.sh
rm tmp/plugin.video.tvdesporto/*~
#rm -r tmp/plugin.video.tvdesporto/tmp
cd tmp
zip -r ../build/plugin.video.tvdesporto.zip plugin.video.tvdesporto
cd ..
rm -r tmp


