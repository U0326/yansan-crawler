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
git clone https://github.com/U0326/yansan-web.git
cd yansan-crawler

python -m venv venv
. venv/bin/activate
pip install -r ./require.txt

docker run --rm -p 27017:27017 --name test-mongo mongo
// TODO 要動作確認
python -m crawler.crawler -d
```

## プロジェクト概要
### クローラ覧
|ファイル名|説明|実行タイミング|
|---|---|---|
|crawler.py|動画情報の取得を行います。|毎日2:00|