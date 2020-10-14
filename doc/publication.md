# 研究業績の管理

努力の成果を記録に残しましょう．

## 更新方法の概略

[/tools/import_from_researchmap.py](/tools/import_from_researchmap.py)
を実行すると教員の researchmap から業績データが自動で取り込まれる．

GitHub Actions で取り込みとコミットを行う手動軌道のWorkflowがあるので，これを使っても良い．

## メモ

### 著者名について

 * 名前を間違えると名寄せに失敗するので特に注意する．  
   英語表記の名前と日本語表記の名前の両方が必要である．
 * [/data/members.toml](/data/members.toml), [/data/alimuni.toml](/data/alumni.toml) にある名前だけが  
   [研究業績のページ](https://control.kuaero.kyoto-u.ac.jp/ja/publications/)
   のリストに現れるので，こちらとの表記の一致も重要．

### 書誌情報について

 * 研究室外のデータ用のフラグがある．
   ```
   outside_kuaero = true
   ```
   このフラグが立っているデータは[個人ごとの表示](https://control.kuaero.kyoto-u.ac.jp/ja/publications/#ichiro-maruta)の時のみに表示され，[研究室の業績一覧](https://control.kuaero.kyoto-u.ac.jp/ja/publications/)では表示されない．

### [/data/publications/](/data/publications/) 配下のファイルについて

* [awards.toml](/data/publications/awards.toml) の内容は[受賞のページ](https://control.kuaero.kyoto-u.ac.jp/ja/awards/)にも列挙される．
* それ以外のファイルのどれに記入しても挙動に差はない

## 設計方針のメモ

 * 研究業績のデータは研究者個人にとっても重要かつ更新がめんどくさい．
 * researchmap が V2 になって情報量が増えた＆共著者間でデータをある程度共有できるようになったので
   メンバーの researchmap データを結合して研究室の業績一覧を作る方針に転換
 * 現状では著書の扱いが微妙（researchmapのデータの時点で著者・編者などの属性が不完全）

## 設計方針のメモ(obsoleted)

 * 科研費の応募と京都大学教員のデータベースが researchmap に依存しているので
研究者個人用としては researchmap のデータが出力できると有用．
 * メンバー個人でデータを持つと共著者の分だけ重複が発生し無駄手間が多い  
   メンバー１の業績 ∪ メンバー２の業績 ∪ … ∪ メンバーNの業績 ＝ 全員の業績 ⊇ 研究室の業績  
   なので基本的には「全員の業績」に対応するファイル [/data/publications/current.toml](/data/publications/current.toml) をみんなでアップデートし，  
   「個人の業績」および「研究室の業績」は「全員の業績」をフィルタして生成する．
 * 研究室所属前の成果などが 全員の業績 \ 研究室の業績 となる

### データの操作

データは [TOML形式](https://github.com/toml-lang/toml) で書くのは便利だがツールが少し少ないので，操作時はJSON形式に変換するとよい．

JSON形式への変換には [Remarshal](https://github.com/dbohdan/remarshal) などが使える．

JSON形式のデータの操作には [jq](https://stedolan.github.io/jq/) が便利．
