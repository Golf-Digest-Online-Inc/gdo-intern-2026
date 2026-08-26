### SSH鍵を作成（パスフレーズなし）

`ssh-keygen -t ed25519`

### SSH鍵をシステムに登録

`eval “$(ssh-agent -s)“ && ssh-add ~/.ssh/id_ed25519`

### 公開鍵をクリップボードにコピー

`cat ~/.ssh/id_ed25519.pub | clip.exe && echo "copied!"`
