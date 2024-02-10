# 研究内容の管理

制御研の研究内容を幅広く伝えよう．

## 概観
### 研究室の取り組み概要
- 大まかに研究内容をまとめている
- 研究室前の廊下に貼られているポスターと同様の内容
### 研究カード
- 上記概要よりは詳しくそれぞれの研究をまとめる
- More Details ボタン（もしくは画像）でポップアップ（Modal）を表示
### ギャラリー
- 実験やシミュレーションなど，動画や写真のギャラリー

## ファイル構成
```
labsite
├── archetypes
├── config.toml
├── content
│   ├── _index.en.md
│   ├── _index.ja.md
│   ├── access
:   :
│   └── research                   <- 研究内容に関する編集は基本ここ
│       ├── _index.en.md           <- 研究概要（英語）
│       ├── _index.ja.md           <- 　　　　（日本語）
│       ├── img1                   <- 研究概要用画像
│       ├── img2
:       :
│       ├── detail1                <- 研究カード1
│       │   ├── _index.en.md       <- 説明文（英語）
│       │   ├── _index.ja.md       <- 　　　（日本語）
│       │   ├── img1.png           <- 画像
│       │   └── img2.svg
│       ├── detail2                <- 研究カード2
│       │   ├── _index.en.md
│       │   ├── _index.ja.md
:       :   :
│       └── gallery                <- ギャラリー
│           ├── _index.en.md       <- ギャラリー情報（英語）
│           ├── _index.ja.md       <- 　　　　　　　（日本語）
│           ├── mov.mp4            <- 動画
│           ├── img.png
:           :
├── themes
│   └── ctrl-lab
│       ├── LICENSE
│       ├── archetypes
│       ├── assets
│       ├── layouts
│       │   ├── index.html
│       │   ├── _default
│       │   │   ├── awards.html
│       │   │   ├── baseof.html
│       │   │   ├── members.en.html
│       │   │   ├── members.ja.html
│       │   │   ├── publications.html
│       │   │   ├── research.html        <- 研究内容のレイアウトはここ
│       │   │   └── single.html
│       │   └── partials
:       :
```

## 編集方法

### 研究概要の編集方法
- `content/research` 内の `_index.ja.md` と `_index.en.md` を編集する
- markdown 内の `content` を追加すれば，新たなブロックができる
- `content/research` 内に画像を追加し，markdown 内の `fig_name` に画像ファイル名を追加すれば，対応して画像が表示される

### 研究カードの追加方法
- `content/research` 内に新しくフォルダ `hoge` を作成
  - フォルダ名はわかりやすければなんでもよい
- 作成したフォルダ `hoge` 内に，次の形式の`_index.ja.md` と `_index.en.md` を作成する  
  markdown の書き方は[他サイト](https://qiita.com/oreo/items/82183bfbaac69971917f#:~:text=Markdown%EF%BC%88%E3%83%9E%E3%83%BC%E3%82%AF%E3%83%80%E3%82%A6%E3%83%B3%EF%BC%89%E3%81%AF%E3%80%81,%E3%82%82%E9%96%8B%E7%99%BA%E3%81%95%E3%82%8C%E3%81%A6%E3%81%84%E3%82%8B%E3%80%82)参照
    ```
    ---
    title: "タイトル"
    date: 日付(yyyy-mm-dd) # ソート用
    author: "著者名"
    ---
    本文（markdown）
    ```
- （必要なら）画像を `hoge` フォルダに追加する（png, jpg, svg あたりは動く．動画はギャラリーへ）

### ギャラリーの追加方法
- `content/research/gallery` にファイルを追加する
- `content/research/gallery` 内の `_index.ja.md` と `_index.en.md` にキャプション `caption` と画像ファイル名 `src`，日付（ソート用） `date` を追加する
- jpg, png, svg, mp4 などが動く

## メモ
### 研究カード
- 表示順は日付順（降順）
- 画像の内ひとつを勝手に選んでサムネにする
  - svg ファイルはサムネにできない（トリミングができないため）
  - 表示するものがなければ，No Image と表記
- Modal では一律，本文記述後に画像がすべて表示される
- 画像の表示順序は現状ファイル名順
- サイズや形状に依存せず出力
### ギャラリー
- 画像・動画の表示順序は日付順（降順）
- 基本は3列，画面幅に合わせて2列や1列になる

## 設計方針・小技
- 更新の際に変更するファイルがなるべくまとまっているように
  - 各研究カードの説明文・画像の追加は同一フォルダ内で完結
- 画像やフォルダの名前をたいして気にしなくても，出力がなされる
- 文章の情報を toml などで記述するのはあまり見やすくないため，直で markdown を編集
- md ファイルを作るようにしたことで，html 中での言語に関する条件分岐などが不要に
- ~~研究概要・後半のギャラリーは無駄にファイル・フォルダが増えないように `data/research.toml` で管理~~ 
- 内容の編集はすべて `content/research` 内で完結
- 奇偶で図の位置を割り振る場合，スマホで見た時に文章と画像の順番に一貫性があるように（文章の後ろに画像），内部的な順序は固定
- 画像の指定がない/ファイル名タイポの場合にバグらないように，minipage 解除や No Image 表示などで対応
- カードには画像の内1枚をトリミングしてサムネ表示
  - サムネを押しても Modal が出る

