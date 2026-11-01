# 编译前保留完整来源

源代码和必要输入放source/，每次尝试放并列builds/<新ID>/，二者不能互相嵌套。源目录不放将要生成的同名产物：程序拒绝，否则旧PDF可能被误当成功的新构建。原输入PDF若必须作为资源使用，保留独立资源路径；不要为了通过检查删除旧证据。使用项目内相对路径的构建器；外部输出也应按实际来源另存，不把工具当沙箱。

```bash
python /path/to/skill/scripts/build_archive.py run --source source --attempt builds/draft01 --artifact paper.pdf --timeout 120 -- python build.py
python /path/to/skill/scripts/build_archive.py verify builds/draft01 --expected-manifest-sha256 SAVED_HASH
python /path/to/skill/scripts/build_archive.py select --attempt builds/draft01 --artifact paper.pdf --output final01.pdf --receipt selection01.json --expected-manifest-sha256 SAVED_HASH
```

示例120秒仅是单次命令超时，实际从原总预算中分配，不延长作者钟。命令返回的archive_manifest_sha256保存到构建目录外的账本，连同实际开始/结束、原退出码、PDF页数和用途。每次全新尝试目录；无PDF的编译失败也保留原日志，超页稿保留原PDF与源码。源码先快照，再在workspace副本运行。完成后全文件清单核验；候选选择只复制到新的终稿路径，外部清单哈希绑定原尝试。使用旧快照回放时，在新的source-only目录仅复制完整必要源和输入，不携带旧目标产物。

复制成功、退出0或PDF存在不证明内容/布局/页数合格；实际看完PDF再选择用于评审。论文引用、评委和最终封包绑定同一选定PDF。对照构建账本核验所有已实际看过/审过的失败与成功版本。错误或后续篡改不能通过重写清单隐藏。该工具只检查有记录的文件；未走工具的编译不能追溯制造原字节。保留缺口。

工具不约束恶意脱离进程组的子进程、绝对路径外部写入、网络或外部依赖，也不认证来源真实性；只运行已审查、授权的构建命令。哈希不证明科学有效性。工具虽保留现有源码和输出，仍需确保编译真正执行并检查实际结果。


## 固定HTML页面的可选全页预检

采用PyMuPDF `insert_htmlbox` 固定页构建时，可先用 `scripts/layout_preflight.py` 检查全部页，避免只知道第一个异常。pages.json是按页排列的非空HTML字符串数组，CSS单独存文件；宽高是实际内容框，单位pt，按原格式填写，不照搬示例尺寸。该可选工具依赖PyMuPDF，已有其他可靠构建器时无需切换。

```bash
python scripts/layout_preflight.py --pages pages.json --css paper.css --width 522 --height 695 --output preflight01.json
```

退出0表示本引擎中全部页在scale=1时排入，1表示存在溢出，2表示非法输入或拒绝覆盖旧结果。报告包括所有页的返回值与有上限的高度搜索；高度端点不保证任意HTML/CSS全局单调，超上限也可能是宽度问题。它不生成交付PDF，也不认证文字/图片/字体资源完整或可读性。

根据真实溢出调整合法留白、结构或内容，保持原题页数、字体和实质要求；每份源与失败继续按构建账本保存。允许更改内容时复核全部要求、结果与引用，不用隐藏裁切或无界缩字获取“通过”。最后仍查看选定PDF的全部页和必要放大；小余量不证明换字体或版本后的稳定性。当前原型仅在本地PyMuPDF1.28.0和限定输入上检验。
