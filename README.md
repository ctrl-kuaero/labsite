# 制御研公開サイトのソース

[京都大学大学院 工学研究科 航空宇宙工学専攻 制御工学研究室のWebサイト](http://control.kuaero.kyoto-u.ac.jp/)

のソースです．[Hugo](https://gohugo.io/)を使っていて，
このレポジトリのmasterブランチにpushすると自動で更新されます．

## コンテンツの更新方法
### メンバーの更新
[members.toml](data/members.toml), [alumni.toml](data/alumni.toml)を更新する．

### 研究業績の更新
[研究業績の管理](/doc/publication.md)を参照

### お知らせ
:construction: 未実装

### アルバム
:construction: 未実装

### その他のページ
[/content/](/content/)の中のそれらしいフォルダを探して
index.{ja|en}.md を編集する．

## 見た目の修正方法
[Bulma](https://bulma.io/)のドキュメントを参考にしつつ
[_variables.scss](/themes/ctrl-lab/assets/sass/_variables.scss)，
[_overrides.scss](/themes/ctrl-lab/assets/sass/_overrides.scss)を編集する．
必要なら[テーマのフォルダ](/themes/ctrl-lab/)の中を修正する．

## 注意事項

1. データファイル全般に全角スペース，全角カンマを混入させないこと

