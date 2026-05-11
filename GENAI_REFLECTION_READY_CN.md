# GenAI 批判性反思（可直接用于视频 30-40 秒）

> 注意：请把下面内容改成你真实经历后再使用，避免与实际开发记录不一致。

## 可直接口播版本（约 35 秒）
在这次项目里，我把 GenAI 用在三个环节：CLI 参数结构、测试用例补全、以及错误处理思路。  
它最大的帮助是让我更快搭起了初版框架，尤其是 `build/load/print/find` 命令骨架和测试清单。  
但它也给出过不合适建议，比如早期建议的索引结构没有保存 `positions`，不利于解释统计信息，我后来改成了 `word -> doc -> {freq, positions}`。  
另外在网络层面，AI 给的异常处理过于理想化，我在本地遇到代理错误后增加了更保守的处理与离线演示方案。  
我的结论是：GenAI 适合加速样板代码和思路发散，但算法正确性、数据结构取舍和最终质量必须由我自己验证与负责。

## 可展示的证据点（视频里可提 2-3 个）
1. 代码结构建议：AI 帮助快速拆分 `crawler/indexer/search/storage/main` 模块。
2. 错误示例：AI 初版建议未覆盖 `empty query` 与代理异常，我手动补了边界处理。
3. 测试策略：AI 提供了测试方向，但我自己补全了限速逻辑、AND 查询和持久化回环测试。

## 可放在仓库里的简版声明
- Used GenAI for scaffolding, refactoring suggestions, and test brainstorming.
- Manually validated all generated code and revised unsuitable designs.
- Final data structures, edge-case handling, and debugging decisions were made independently.

