# 研究業績の管理

努力の成果を記録に残しましょう．

## 更新方法の概略

[/data/publications/current.toml](/data/publications/current.toml) に追記する

書き方は過去のデータを参照する

* 国内会議での発表
* 国際会議での発表
* 論文誌での発表

で書き方が違うので，最低限同じカテゴリのデータを，
できれば同じ論文誌/会議のデータを参考にする．

## メモ

### 著者名について

 * 名前を間違えると名寄せに失敗するので特に注意する．  
   英語表記の名前と日本語表記の名前の両方が必要である．
 * [/data/members.toml](/data/members.toml), [/data/alimuni.toml](/data/alumni.toml) にある名前だけが  
   [研究業績のページ](https://control.kuaero.kyoto-u.ac.jp/ja/publications/)
   のリストに現れるので，こちらとの表記の一致も重要．

### 書誌情報について

 * 講演集が電子媒体でページ番号が判然としないときは
   page_begin に識別子となりそうな情報（講演番号など）を入れておく．例えば  
   ```
   page_begin = "311-3" 
   ``` 
   みたいな感じ，page_endは書かなくてよい．

 * publication_date は必須．  
   ```
   publication_date = "20190412"
   ```  
   のような形式で入力する．公開日が判然としないときは  
   ``` 
   publication_date = "20190400"
   publication_date = "20190000"
   ```   
   のように必ず8桁で入力する．

   出版日未決定の場合は
   ``` 
   publication_date = "20xx"
   ```   
   で行けると思うが未確認．Research Map への出力は特に怪しい．

 * 外部のデータベースとの紐づけが欲しいので，  
   1. [DOI](https://ja.wikipedia.org/wiki/デジタルオブジェクト識別子) がついているときは最優先で記入する．  
   2. なければ[NAID](https://ja.wikipedia.org/wiki/CiNii)やJglobalIDがついていないかを確認し，あれば記入する．
   3. それらもない場合，講演情報などが記載された外部のページがあれば URL を記載する．

 * 研究室外のデータ用のフラグがある．
   ```
   outside_kuaero = true
   ```
   このフラグが立っているデータは[個人ごとの表示](https://control.kuaero.kyoto-u.ac.jp/ja/publications/#ichiro-maruta)の時のみに表示され，[研究室の業績一覧](https://control.kuaero.kyoto-u.ac.jp/ja/publications/)では表示されない．

   * Research Map 用の出力に研究室外（研究室加入以前）の業績を入れたい
   * 研究室とは関係ないが個人的に宣伝したい業績がある

   ときの利用を想定．
### [/data/publications/](/data/publications/) 配下のファイルについて

* [awards.toml](/data/publications/awards.toml) の内容は[受賞のページ](https://control.kuaero.kyoto-u.ac.jp/ja/awards/)にも列挙される．
* それ以外のファイルのどれに記入しても挙動に差はない(2020/08/05:old_で始まるファイルの情報が反映されなくなっているのでとりあえずcurrent.tomlの下部にold*.tomlの中身を移しています．更新の際はcurrent.tomlの一番上に追加してください．)．
* autogen_ で始まるファイルは京大のデータベースから自動生成したものなので修正以外の変更は加えない．
* old_ で始まるファイルは管理者が研究室に加入する以前の情報をネットから収集したものなので正確さに注意する．
* その他注意を要するデータを加える時はファイルを分ける．

## Bookmarklet

古典的だが Bookmarklet で書誌情報を抜き出す作業を自動化した．

### IEEE Xplore用
1. 下記のJavaScriptコードをURLとしてブックマークに登録
``` 
javascript:(function(){let data={};data.reviewed=true;data.lang="en";data.en_title=global.document.metadata.title;data.page_begin=global.document.metadata.startPage;data.page_end=global.document.metadata.endPage;if(global.document.metadata.doi){data.doi=global.document.metadata.doi}let authors=[];let en_author="";for(let i=0;i<global.document.metadata.authors.length;i++){authors[i]=global.document.metadata.authors[i].name}data.en_author=authors.join(', ');data.en_booktitle=global.document.metadata.publicationTitle;if(global.document.metadata.isConference){data.type="international_conference"}if(global.document.metadata.isJournal){data.type="journal"}if(global.document.metadata.publicationDate){let datestr=global.document.metadata.publicationDate;let found=datestr.match(/([^\s\.]+)+\.?\s+(\d\d\d\d)/);if(found==null){data.publication_date=datestr}else{function getMonthFromString(mon){return new Date(Date.parse(mon+" 1, 2012")).getMonth()+1}data.publication_date=found[2]+(getMonthFromString(found[1])+"").padStart(2,'0')+"00"}}if(global.document.metadata.htmlLink){data.url="https://ieeexplore.ieee.org"+global.document.metadata.htmlLink}let out="[[record]]\n";for(var k in data){if(data.hasOwnProperty(k)){out+=k+" = "+JSON.stringify(data[k])+"\n"}}alert(out)})();
```
2. 例えば https://ieeexplore.ieee.org/document/6385631 に行く
3. 登録したブックマークをクリックしてコードを実行
4. 出てきたダイアログから文字列をコピペする

Chromeではダイアログから文字列をコピペできない．  
Firefoxを使うか，コードの最後にあるalertをconfirmに書き換える．

## 設計方針のメモ

 * 研究業績のデータは研究者個人にとっても重要かつ更新がめんどくさい．
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

#### 2017年以前の丸田のデータに研究室外フラグを立てる
``` sh
toml2json data_from_researchmap_maruta_20181008.toml > before.json
cat before.json | jq -r '{record: (.record | map_values(if .publication_date > "20170000" then . else . + {outside_kuaero:true} end))}' > after.json
json2toml after.json >  data_from_researchmap_maruta_20181008.toml
rm before.json after.json
```
