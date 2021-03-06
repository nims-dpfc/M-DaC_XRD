# 「NIMS Materials Data Conversion Tools (M-DaC)」について

国立研究開発法人物質・材料研究機構（以下、NIMS）では、物質・材料研究の一環として、実験データの効率的な収集と高付加価値化の技術開発を行っています。本開発で提供される「NIMS Materials Data Conversion Tools (__M-DaC__)」とは、NIMS が計測機器メーカーの協力を得て開発した実験の主要条件やメタデータの自動抽出とその翻訳作業（可読化）の自動化、ならびに多次元の数値データ行列の Schema on Read 型の可読化を行うことができるプログラムおよびソースコード群を指します。

今回開発した M-DaC を研究者等に広く使用または利用いただき、関連の技術開発をさらに推し進めることができるよう、試験用プログラム、試験用ソースコード及びサンプルデータ等（以下まとめて「本プログラム等」という）を無償で公開します。

<br />

## チュートリアル

  <https://nims-dpfc.github.io/M-DaC_doc/>

<br />

## 対象装置およびメーカー（2020年4月15日現在）

| 測定法 | 略称 | メーカー |
| --- | --- | --- |
| X線光電子分光 | XPS | アルバック・ファイ株式会社 |
| X線回折 | XRD | 株式会社リガク |
| オージェ電子分光 | AES | 日本電子株式会社、アルバック・ファイ株式会社 |

<br />

## 動作環境

* python 3.X
* Jupyter Notebook (<http://jupyter.org/>)

<br />

## 操作方法

* 作業ディレクトリに一式をダウンロードしてから、以下のチュートリアルのサンプルデータで一連のフローを試してください。  
 <https://nims-dpfc.github.io/M-DaC_doc/>
* 各メーカーのお手持ちのデータがあれば、同様に処理を進めることができます。

<br />

## 利用ルールおよびライセンス

* 本プログラム等のうち、サンプルデータおよび記事コンテンツについては、「__クリエイティブ・コモンズ・ライセンスの表示 - 非営利4.0国際__」のもとで「__CC-BY-NC__」での利用ができます。
* 本プログラム等のうち、ライセンス欄に「MITライセンス」の表記のある試験用ソースコードは、別に示される『__LICENSE_MIT.txt__』MITライセンスのもと利用できます。
* 詳細は『__Terms of Use and License_JP.md__』をお読みください。

<br />

## 論文などにおける引用の表記

* M-DaCを使った研究や開発では、下記の引用例を参照してください。

日本語引用文例）

- 長尾浩子, 松波成行, 鈴木峰晴, 吉川英樹：”NIMS Materials Data Conversion Tools (M-DaC) ver 1.1”

英語引用文例）

- H. Nagao, S. Matsunami, M. Suzuki, and H. Yoshikawa: "NIMS Materials Data Conversion Tools (M-DaC) ver 1.1"

### M-DaCに関するお問い合わせ

ライセンスや本プログラム等の利用方法やライセンスに関することで不明な点につきましては、以下にお問い合わせください。

<br />

国立研究開発法人物質・材料研究機構

 　統合型材料開発・情報基盤部門  材料データプラットフォームセンター

　 M-DaC代表窓口  E-mail: m-dac@ml.nims.go.jp

<br />

2019.1.30 初版  
2020.4.15 第2版  
2020.5.07 第3版  
