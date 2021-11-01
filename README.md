使用手順

1. 開発環境Python3.8以上を確保
2. [Mecab辞書をインストール](https://github.com/ikegami-yukino/mecab/releases)
3. Mecabをインストール：pip3 mecab install
4. zmailをインストール：pip3 install zmail（[説明](https://github.com/zhangyunhao116/zmail)）
5. 全てのINIファイルとtxtファイルはutf-8を使ってください
6. userConfig.iniを改修してください
   |Key|説明|
   |--|--|
   |mailuser|メールアドレス：ABC＠outlook.comとか|
   |mailpwd|パスワード|
   |cmduser|操作アドレス|
   |cmdpwd|操作パスワード（アルファベットのみabcdとか）|
   |finalmailid|最新のメールID|

<br/>

Pythonでのメール操作と自動返事など

• 1　Pythonでのメール自動送信　　　☑️

 • 2　Pythonでのメールの解析　　　☑️ 
 
• 3　MeCabによる日本語文章の分解と解析　　　☑️

 • 4   メールでパソコンの遠隔操作（shutdownとか、restartとか）　　　☑️
 
 • 5　操作時の二重認証（送信メールアドレスと操作パスワード）☑️
 
 • 6　自動返事　　　☑️
