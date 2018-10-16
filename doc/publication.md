# 研究業績の管理

## 更新方法

[/data/publications/current.toml](/data/publications/current.toml) に追記する

書き方は過去のデータを参照する

* 国内会議での発表
* 国際会議での発表
* 論文誌での発表

で書き方が違うので，最低限同じカテゴリのデータを，
できれば同じ論文誌/会議のデータを参考にする．

## Bookmarklet
古典的だが Bookmarklet で書誌情報を抜き出す

* <a href='javascript:(function(){let data={};data.reviewed=true;data.lang="en";data.en_title=global.document.metadata.title;data.page_begin=global.document.metadata.startPage;data.page_end=global.document.metadata.endPage;if(global.document.metadata.doi){data.doi=global.document.metadata.doi}let authors=[];let en_author="";for(let i=0;i<global.document.metadata.authors.length;i++){authors[i]=global.document.metadata.authors[i].name}data.en_author=authors.join(", ");data.en_booktitle=global.document.metadata.publicationTitle;if(global.document.metadata.isConference){data.type="international_conference"}if(global.document.metadata.isJournal){data.type="journal"}if(global.document.metadata.publicationDate){let datestr=global.document.metadata.publicationDate;let found=datestr.match(/([^\s\.]+)+\.?\s+(\d\d\d\d)/);if(found==null){data.publication_date=datestr}else{function getMonthFromString(mon){return new Date(Date.parse(mon+" 1, 2012")).getMonth()+1}data.publication_date=found[2]+(getMonthFromString(found[1])+"").padStart(2,"0")+"00"}}if(global.document.metadata.htmlLink){data.url="https://ieeexplore.ieee.org"+global.document.metadata.htmlLink}let out="[[record]]\n";for(var k in data){if(data.hasOwnProperty(k)){out+=k+" = "+JSON.stringify(data[k])+"\n"}}alert(out)})();'>IEEE Xplore用</a>
## メモ

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
