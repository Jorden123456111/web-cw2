# 5分钟视频讲稿（中文）

> 建议你按这个脚本练 1-2 次，控制总时长在 4:45 到 4:58，避免超时扣分。

## 0:00 - 0:15 开场
大家好，这是 COMP/XJCO3011 Coursework 2，我实现的是一个命令行搜索工具。  
它可以爬取 quotes.toscrape.com，建立倒排索引，并支持关键词查询。

## 0:15 - 2:15 Live Demo（2分钟）
1. 运行 `build`：  
   - 展示命令：`python -m src.main build --delay 6 --max-pages 20 --scope quotes`  
   - 说明已实现 politeness window，每次请求至少间隔 6 秒。  
2. 运行 `load`：  
   - 展示载入的文档数、词项数、构建时间。  
3. 运行 `print nonsense`：  
   - 展示该词的 posting list（doc、freq、positions）。  
4. 运行 `find good friends`：  
   - 展示多词查询（AND 语义）和排序结果。  
5. 边界用例：  
   - `find` 空查询（提示错误）；  
   - `print` 不存在词（返回无结果提示）。

## 2:15 - 3:45 代码讲解与设计取舍（1.5分钟）
1. `crawler.py`：BFS 爬取，同域过滤；`scope=quotes` 默认只抓 `/` 与 `/page/N`。  
2. `indexer.py`：构建倒排索引 `word -> doc -> {freq, positions}`，并记录文档长度。  
3. `search.py`：  
   - 不区分大小写；  
   - 多词查询使用 AND；  
   - 结果按 TF-IDF 得分排序。  
4. `storage.py`：保存 JSON，包含 metadata、错误日志、visited 页面和索引数据。  
5. 取舍说明：为了稳定性，默认范围可控，保证演示时间和抓取成功率。

## 3:45 - 4:15 测试展示（0.5分钟）
运行 `pytest -q`。  
说明测试覆盖内容：  
- crawler 的 URL 规范化、范围过滤、错误记录、限速行为；  
- indexer 的词频与位置统计；  
- search 的单词/多词与空查询；  
- storage 的读写回环；  
- CLI 的 load/print/find 主路径。

## 4:15 - 4:45 Git 工作流（0.5分钟）
展示 `git log --oneline --graph`。  
说明是增量开发：先 crawler，再 index/search，再 CLI，再测试和文档，提交信息语义化。

## 4:45 - 5:00 GenAI 批判性反思（0.5分钟）
示例表达（请替换成你的真实经历）：  
- GenAI 帮我快速搭建了 CLI 框架和测试思路；  
- 但给过不适合的索引结构建议（例如不记录 positions），我手动修正；  
- 我验证了 AI 代码的正确性并补了边界测试；  
- 最大学习是：AI 适合加速样板代码，但核心算法与正确性必须自己主导。

