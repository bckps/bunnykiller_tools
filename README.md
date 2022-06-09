# create_lookat_lookup.py
 BlenderのLocation(位置)とRotation(回転)からbunnykillerで必要なカメラのパラメータを計算する。

  
# dae_parser.py
Blenderでkeyframeを打ち込み、作成したdaeファイルを読み込む。
  
  
# dae_simu.py
このスクリプトで「.obj」,「.dae」,「filename」を入力して実行すれば,  
bunnykillerを実行するファイルを作成し読み込んだkeyframeの数だけシミュレーションを開始する。
dae_simu.pyからもシミュレーションの変数を変更できる。
```
実行例
obj_file = '/home/blenderfileBox/5by5-front-plane.obj'
    blenderから三角化済みのobjファイルを指定する。

dae_file = '/home/blenderfileBox/5by5-front-plane.dae'
    blenderでカメラの位置、向きを設定しキーフレームを登録、daeファイルにExport。
    Exportする際の設定は次のように行う。
    1. Main→Selection Only(check)
    2. Geom,Anim→Transform(Decomposed)
    3. Anim→Sampling Rate→All Keyed Curves(check)

simu_name = '5by5-front-plane'
    一連のキーフレームで行うシミュレーションに名前をつける。


ディレクトリ構成

~/bunnykiller_tools/
　├ dae_simu.py
　│
　├ model/
　│　└ livingroom.obj
　├ daes/
　│　└ livingroom-train1.dae
　│
　├ scene-results/
　│　└ livingroom-train1/
　│　　　├ 00000/
　│　　　│　└ hdr/
　│　　　│ 　 　└ livingroom-train1.hdr
　│　　　│ 　   └ ...
　│　　　└ 00001/
　│　　　└ ...
　└ etc

livingroom-train1はシミュレーションの名前で実行時にscene-results下に作成される。
livingroom-train1/00000では0番目に設定したカメラの位置でシミュレーションを行う。
```

## camera_sppなどのシミュレーションの変数を変更する

```
dae_simu.py
    simucmd.camera_samples = 4
    一連のシミュレーションはcamera_spp=4で行われる。

```

# simucmd.py
bunnykillerに必要なパラメータを管理する。
```
self.camera_samples=8
camera-spp: カメラの画素ごとにspp*spp本光線をサンプルする。

self.bdpt_samples=512
bidirectional-path-tracing: 光線ごとに"bidirectional-path-tracing"だけ
                            反射等が起こった際に新たな光線を生成する。

self.bounce_streak=4
光線が反射した回数に応じて異なるファイルに保存される。

self.max_bounces=8
反射する回数の上限をきめる。simucmd.pyではコメントアウトされており指定していない。

self.height=257
self.width=257
# 256×256のシミュレーションデータが欲しい場合
# 257×257でシミュレーションのサイズを指定する。(要検討)

self.time_res=2220
時間分解を行う長さ。tのサイズは2220で出力される

self.toffset=0
j時間のオフセット

self.exp=0.008993773740
exposureだが単位は[m]で, 30psずつ時間を分解したい場合
self.exp = c(光速)×30psを入力する。

self.camera_pos='0 1 3'
カメラの位置

self.camera_at='0 1 2'
カメラの見ている先の位置

self.camera_lookup='0 2 3'
カメラの上ベクトル

self.camera_fov=40
カメラのFoV

self.point_light = self.camera_pos+' 1 1 1'
ライトの位置と(R, G, B)の強度

self.objfile='model/export_bathroom_small.obj'
シミュレーションを行うobjファイルの指定

self.name='create-simple-python-about5m-light01-bathroom-small'
シミュレーションにつける名前
アンダーバー"_"は避けてください。ファイル名を識別する際に使用していました。

self.hdr_folder = 'scene-results/bathroom-small/00000/hdrs/'
指定しなくてもプログラム中で勝手に指定してくれる

```
---
  
# Note
ソースコード中に具体的な注意点を書いているので
コメントを読んでから変更するとエラーが減ります。
