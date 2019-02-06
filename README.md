# httpie-aws-authv2

AWS Auth v2 plugin for HTTPie

## Description

[HTTPie](https://httpie.org) で AWS Signature v2 の認証をリクエストに付加するための Auth plugin です。

## Install

```bash
pip install --upgrade git+https://github.com/kzmake/httpie-aws-authv2
```

## Preparation

### 環境変数 ACCESS_KEY_ID / SECRET_ACCESS_KEY を用いてリクエストする場合

```bash
export ACCESS_KEY_ID={払い出されたACCESS_KEY_ID}
export SECRET_ACCESS_KEY={払い出されたSECRET_ACCESS_KEY}
```

```fish
set -gx ACCESS_KEY_ID {払い出されたACCESS_KEY_ID}
set -gx SECRET_ACCESS_KEY {払い出されたSECRET_ACCESS_KEY}
```
で ACCESS_KEY_ID / SECRET_ACCESS_KEY を設定後、リクエストする

### リクエストに直接 ACCESS_KEY_ID / SECRET_ACCESS_KEY を指定してリクエストする場合

```bash
http -v -A aws2 -a {払い出されたACCESS_KEY_ID}:{払い出されたSECRET_ACCESS_KEY} GET https://example.com/api/ Action==DescribeInstances
```
上記のコマンドのように `-a {払い出されたACCESS_KEY_ID}:{払い出されたSECRET_ACCESS_KEY}` を追加してリクエストする

## Usage

`-A aws2` を HTTPie に追加し、リクエスト

### GET の例

Query (`Action==DescribeInstances InstanceId.1==i-HOGEHOGE`) を指定してリクエスト

```bash
http -v -A aws2 GET https://example.com/api/ Action==DescribeInstances
```

### POST の例

Formオプション(`-f`) を指定し、 Form data (`Action=DescribeInstances InstanceId.1=i-HOGEHOGE`) を指定してリクエスト

```bash
http -v -f -A aws2 POST https://example.com/api/ Action=DescribeInstances
```

raw-payload(echo "Action=DescribeInstances InstanceId.1=i-HOGEHOGE") をパイプで渡してリクエスト

```bash
echo "Action=DescribeInstances InstanceId.1=i-HOGEHOGE" | http -v -f -A aws2 POST https://example.com/api/
```

