#### ローカル環境データベース接続

***

##### PostgreSQLコンソール接続コマンド

`docker compose exec postgres psql appdb appuser`

#### `psql` コンソールコマンド

***

##### 現在のスキーマを確認する

`SELECT current_schema();`

##### テーブル作成を実行

`\i /sql/tables/items.sql`

`\i /sql/tables/orders.sql`

`\i /sql/tables/payments.sql`

##### 初期データを登録

`\i /sql/data/items.sql`

##### テーブル定義を確認

`\d items`

`\d orders`

`\d payments`

##### データを確認

`SELECT * FROM public.items ORDER BY id ASC;`

`SELECT * FROM public.orders ORDER BY id ASC;`

`SELECT * FROM public.payments ORDER BY id ASC;`

##### コンソールを終了

`\q`
