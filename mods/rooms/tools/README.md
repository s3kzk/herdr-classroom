# rooms mod の絵を作るスクリプト

`sprites/` と `icons/` の絵、`art.js` は、ここの 3 本で作る。絵を直すときはスクリプトを直して作り直す。

```sh
cd ~/.config/herdr-app/mods/rooms
python3 -I tools/occupants.py sprites   # 住人（15 体 × 小物 4 色 × 4 状態 = 240 枚）
python3 -I tools/scene.py icons        # 校舎（school）の時計塔・木・空の飾り（昼・夜）
python3 -I tools/buildings.py .        # ほかの 5 つの建物の絵と art.js
```

- `buildings.py` は最後に走らせる。`icons/` にある SVG をすべて数えて、大きさを `art.js` に書くため。
- `icons/` の `check`・`clock`・`palette`・`warn` は手で書いた SVG で、スクリプトでは作らない。
- 建物の絵の高さを変えたら、`looks.js` の各建物の `rise` も合わせて直す。fit が高さを計算に使うため。
- 住人は claude と other（表に無いエージェントと Copilot）が Claw'd で、ほかの 13 体は Herdr 同梱のアイコン（`~/.config/herdr-app/icons`）を手本に描いた。アイコンはビルドで読まず、画素をスクリプトに直接書いてある（同梱のアイコンは Herdr の更新で書き換わるため）。
- 住人の体を足したら、`main.js` の `BODIES` にも足す。
