# @kaiun_hikkoshi 投稿画像の作り方（Claude用）

- 画像：`python3 ig/tool/render.py spec.json ig/wN` で 1080×1350 のJPGを作る（要 playwright・Noto CJKフォント）。
- spec.json の形：`{"slides":[{"id":"k1","cat":"金運","sub":"保存版","title":"金運が<br>上がる方角は<br><em>どっち？</em>","size":72,"navi":"n2","body":{"type":"duo","a":"西","at":"お金が<br>入ってくる","b":"北西","bt":"仕事で<br>成功する","warn":true}}]}`
  - body.type：`lead`（html）／`list`（items=[[見出し,説明],...]、red/tight/big）／`duo`（2方角の比較＋注意書き）／`banner`
  - navi：n1 満面の笑顔・n2 ウインク・n3 驚き・n4 考える・n5 ほほえみ・02 指さし・04 鍵を差し出す
  - 見出しは3行まで。`<em>` がオレンジ＋黄マーカー。NG(はみ出し) が出たら文字を減らすか size を下げる
- 公開URL：https://motonory-a.github.io/kippoui-hikkoshi/ig/wN/xxx.jpg（push後1分ほどで有効）

## 決まり（本人と決めたこと）
- 案内役はナビ子。明るい女性。基本はバストアップ
- 文章は短く言い切る。むずかしい言葉を使わない（方違え→寄り道引越し、吉方位→いい方角）。締めは「サイトで確認しましょう」「プロフィールのリンクから無料で」
- 九星気学の内容は「〜と言われています」。予言のような断定はしない。でたらめを書かない
- 金運・恋愛運は人気なので1週7本のうち各2本、残り3本は引越しの基本・季節の話題
- AI画像なので instagramData.isAiGenerated=true。毎晩21:30（Asia/Tokyo）に投稿
- ハッシュタグ6〜7個（#吉方位 #引越し #開運 #九星気学 など。不動産向けに #住み替え #物件探し も）
