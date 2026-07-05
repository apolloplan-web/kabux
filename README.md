このコードはgithub actionsのcron実行機能を利用したpythonコードの定時実行を行なっています。
yfinanceモジュールを使って取得した前日終値をgoogle spreadsheetへ自動で書き出します。

使われている機能群
github actions
　-settings repository secretにJSONの内容を登録
　-requirements.txtの配置 リポジトリのトップディレクトリにテキストファイル
google spreadsheet
 -共有 ワークシートの共有機能を使いサービスアカウントとして登録されたメールアドレスを編集者として登録
Google Cloud
 -APIとサービス　sheets.googleapis.com, drive.googleapis.com を有効化
 -認証情報-サービスアカウント　認証情報を作成しJSON取得

 ここまで準備できたら、あとはcron実行前に「Actions」タブから実行させたいymlをクリックして実行ダイアログ
