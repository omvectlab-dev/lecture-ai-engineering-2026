# 第6回 解答_20261123(omvect)

## 演習

- STEP 1 のツールの名前：`glossary_search_glossary`
- STEP 2 の [tool call]：`glossary_search_glossary({'query': '3レベル'})`
- STEP 3 の [tool call]：`fetch_fetch({'url': 'https://modelcontextprotocol.io/'})`
- STEP 4 の [tool call]：
  - `aws_aws___search_documentation({'search_phrase': 'Amazon S3 バージョニング 概要'})`
  - `aws_aws___search_documentation({'search_phrase': '"Using versioning" Amazon S3 overview'})`
- 気づき・疑問：MCPを利用することで、エージェント本体を変更せずに外部ツールを追加できることを確認した。また、ローカルで起動するサーバーと、URLで接続するリモートサーバーの違いを理解した。

## 宿題

- 取り組んだレベル：実装
- やったこと：第3回で作成した `make_quiz` をMCPサーバーに登録した。また、存在しない講義回を指定した場合に、用語集に登録されている講義回を案内するようにエラー処理を改善した。
- 結果：`glossary_make_quiz` がツール一覧に追加された。第99回を指定すると、範囲外であることと指定可能な講義回が返され、その内容をモデルが利用者に案内することを確認した。pytestは25件すべて成功した。
- 気づき・疑問：MCPサーバー側でツールを公開することで、エージェント側を変更せずに機能を追加できた。また、エラー時に分かりやすいメッセージを返すことで、モデルが適切に利用者へ案内できることを確認した。
