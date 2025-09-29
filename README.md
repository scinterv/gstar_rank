# ⭐ Github Star Rank

一个基于 GitHub Star 数量的仓库排名系统，完全利用 GitHub 仓库 + Actions 实现自动化排名更新，支持标签筛选和 GitHub Pages 部署。

## ✨ 功能特性

- 🔄 **自动更新**: 每 2 小时自动获取仓库 Star 数据并更新排名
- 🏷️ **标签筛选**: 支持为仓库添加多个标签，可按标签筛选查看
- 📱 **响应式设计**: 支持桌面端和移动端访问
- 🚀 **零成本部署**: 完全基于 GitHub Actions 和 GitHub Pages
- 🎨 **美观界面**: 现代化 UI 设计，支持深色主题

## 📁 项目结构

```
gstar_rank/
├── .github/
│   └── workflows/
│       └── update-rank.yml      # GitHub Action 工作流
├── scripts/
│   └── update_rank.py           # 排名更新脚本
├── repos.txt                    # 仓库配置文件
├── index.html                   # 排名展示页面
├── requirement.md               # 需求文档
└── README.md                    # 项目说明
```

## 🚀 快速开始

### 1. Fork 项目

点击右上角的 "Fork" 按钮，将此项目 fork 到你的 GitHub 账户。

### 2. 配置仓库列表

编辑 `repos.txt` 文件，添加你想要排名的仓库：

```txt
# Github Star Rank 仓库配置
# 每行一个仓库，格式：owner/repo
# 示例：
microsoft/vscode
facebook/react
google/tensorflow
vuejs/vue
nodejs/node
```

### 3. 添加标签（可选）

在仓库名称下方添加标签，每个标签占一行：

```txt
microsoft/vscode
  IDE
  Editor
  Microsoft
facebook/react
  Frontend
  UI
  Facebook
google/tensorflow
  AI
  Machine Learning
  Google
```

### 4. 启用 GitHub Actions

1. 进入你的仓库页面
2. 点击 "Settings" 标签
3. 在左侧菜单中找到 "Actions" → "General"
4. 确保 "Allow all actions and reusable workflows" 被选中
5. 点击 "Save"

### 5. 启用 GitHub Pages

1. 在仓库设置中找到 "Pages" 选项
2. 在 "Source" 下选择 "Deploy from a branch"
3. 选择分支为 "main"（或你的默认分支）
4. 选择文件夹为 "/ (root)"
5. 点击 "Save"

### 6. 手动触发首次运行

1. 进入 "Actions" 标签页
2. 选择 "Update Star Rank" 或 "Test Star Rank" 工作流
3. 点击 "Run workflow" 按钮
4. 等待运行完成
5. 查看运行日志，确认脚本执行成功

### 7. 查看结果

访问你的 GitHub Pages 地址：

```
https://你的用户名.github.io/gstar_rank
```

## ⚙️ 配置说明

### repos.txt 文件格式

```txt
# 注释行以 # 开头
owner/repo-name
  tag1
  tag2
  tag3
owner2/repo-name2
  tag4
  tag5
```

- 仓库格式：`owner/repo-name`
- 标签格式：在仓库名称下方缩进（空格或制表符）
- 支持多行注释，以 `#` 开头

### GitHub Action 配置

工作流文件位于 `.github/workflows/update-rank.yml`，主要配置：

- **触发条件**: 每 2 小时自动运行 + 手动触发
- **运行环境**: Ubuntu Latest
- **Python 版本**: 3.9
- **依赖包**: requests, beautifulsoup4

## 🎨 自定义样式

你可以通过修改 `scripts/update_rank.py` 中的 `generate_html()` 函数来自定义页面样式：

- 修改 CSS 样式
- 调整页面布局
- 添加新的功能特性

## 🔧 故障排除

### 常见问题

1. **GitHub Action 运行失败**

   - 检查 `repos.txt` 文件格式是否正确
   - 确认仓库名称是否存在拼写错误
   - 查看 Action 运行日志获取详细错误信息
   - 使用 "Test Star Rank" 工作流进行调试

2. **页面显示"暂无数据"**

   - 确认 GitHub Action 已成功运行
   - 检查 `index.html` 文件是否已更新
   - 手动触发一次 Action 运行
   - 查看 Action 日志中的 "Check generated files" 步骤

3. **Action 只显示 Pages 部署**

   - 确认 "Update Star Rank" 工作流已启用
   - 检查工作流文件是否在 `.github/workflows/` 目录中
   - 手动触发 "Test Star Rank" 工作流进行测试

4. **权限错误 (403 Forbidden)**

   - 确认仓库设置中 Actions 权限已正确配置
   - 检查工作流文件中的 `permissions` 设置
   - 确保 `GITHUB_TOKEN` 有足够的权限

5. **GitHub Pages 无法访问**

   - 确认 Pages 功能已启用
   - 检查分支和文件夹设置是否正确
   - 等待几分钟让 Pages 生效

6. **API 限制问题**
   - GitHub API 有速率限制，脚本已添加延迟处理
   - 如果仓库数量很多，可能需要调整延迟时间

### 调试模式

在 `scripts/update_rank.py` 中添加调试信息：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 功能扩展

### 添加更多排序选项

可以修改排序逻辑，支持按以下方式排序：

- 按 Star 数量（当前）
- 按更新时间
- 按仓库名称
- 按标签数量

### 添加更多筛选条件

可以扩展筛选功能：

- 按 Star 数量范围
- 按语言筛选
- 按更新时间筛选

### 添加数据导出

可以添加数据导出功能：

- 导出为 CSV 格式
- 导出为 JSON 格式
- 生成统计报告

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 📄 许可证

MIT License

## 🙏 致谢

感谢所有开源项目的贡献者，让这个排名系统成为可能！

---

**注意**: 请确保遵守 GitHub API 的使用条款，避免过于频繁的请求。
