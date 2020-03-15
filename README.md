# yansan-crawler
[ヤンサンNavi](http://yansan-navi.garaku.work)のクローラを構成するプロジェクトです。プロジェクトの全容は[こちら](https://github.com/U0326/yansan-integration)をご覧ください。

## 要求事項
以下を事前にインストールしておく必要があります。
* Docker Engine: 1.13.0以上
* Python: 3.8以上

## ローカルでの実行方法
事前に`/video/youtube/const.py`ファイルの以下記載を修正する必要があります。
```
API_KEY = 'dummy_text'
```

```
$ git clone https://github.com/U0326/yansan-web.git
$ cd yansan-crawler

$ python -m venv venv
$ . venv/bin/activate
$ pip install -r ./require.txt

$ docker run --rm -p 27017:27017 --name test-mongo mongo

$ python -m src.main.bootstrap.video_info_crawler -d
```

## プロジェクト説明
### 処理一覧
※ 処理のエントリポイントは、`src.main.bootstrap`に配置しています。

|エントリポイント|説明|実行タイミング|
|---|---|---|
|video_info_crawler.py|動画情報の取得を行います。|毎日2:00|

### 内部で使用するAPI
* [YouTube Data api](https://developers.google.com/youtube/v3/getting-started?hl=ja): YouTubeの動画情報を取得する為に使用しています。
* [getthumbinfo](https://w.atwiki.jp/nicoapi/pages/16.html): ニコニコ動画の動画情報を取得する為に使用しています。
