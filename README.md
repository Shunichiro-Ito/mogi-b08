# ShockDawnBackEnd
食堂混雑予測アプリのバックエンド -> SDBが本番環境, testが適当な環境。  
rootEndPoint : <https://shockdawnbackend.onrender.com>  
デプロイ先が[Render](https://render.com/)の都合上, 15分以上アクセスがないと停止してしまい開くのに2分くらいかかりますが仕様です。

# 使用技術
サーバー周り  
Python, FastAPI, uvicorn  
データベース回り  
SQLalchemy, ( postgres )  

# OpenAPI
fastAPIの機能で<https://shockdawnbackend.onrender.com/docs>にAPI仕様とサンプル実行が可能です.

# フォルダ構成
SDB/main.py -> メインファイル APIルーティング等々  
SDB/config.py, SDB/requirements.txt -> その他の環境変数や必要なモジュール記述  
SDB/.env.sample -> 設定すべき環境変数のkeyのみ (外部APIを呼び出すことになった場合の伏線）  
SDB/models/*.py -> データベーススキーマの定義  
SDB/utils/*.py -> 便利なメソッドとかいれれたら  

# localで立ち上げる方法  
Dockerコンテナで立ち上げる方法もサポートしています。その場合のRootEndPoint:<http://localhost:8000>になります.  　
[Render](https://render.com/)の場合全く必要ないがその他のサービスを利用する場合は必要になるとかならないとか.  

SDB/で
```docker-compose up```
を実行すれば立ち上がります。  




