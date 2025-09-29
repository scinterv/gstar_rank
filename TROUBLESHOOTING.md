# 故障排除指南

## 权限错误 (403 Forbidden)

如果遇到以下错误：

```
remote: {"auth_status":"access_denied_to_user","body":"Permission to scinterv/gstar_rank.git denied to github-actions[bot]."}
fatal: unable to access 'https://github.com/scinterv/gstar_rank/': The requested URL returned error: 403
```

### 解决方案

#### 方法 1: 检查仓库 Actions 权限设置

1. 进入你的 GitHub 仓库
2. 点击 "Settings" 标签
3. 在左侧菜单中找到 "Actions" → "General"
4. 滚动到 "Workflow permissions" 部分
5. 选择 "Read and write permissions"
6. 勾选 "Allow GitHub Actions to create and approve pull requests"
7. 点击 "Save"

#### 方法 2: 使用 Personal Access Token (推荐)

如果方法 1 不起作用，可以创建一个 Personal Access Token：

1. 进入 GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 点击 "Generate new token (classic)"
3. 选择以下权限：
   - `repo` (完整仓库访问)
   - `workflow` (更新 GitHub Action 工作流)
4. 复制生成的 token
5. 在仓库设置中添加 Secret：
   - 进入仓库 Settings → Secrets and variables → Actions
   - 点击 "New repository secret"
   - Name: `PERSONAL_ACCESS_TOKEN`
   - Value: 粘贴你的 token
6. 修改工作流文件，将 `GITHUB_TOKEN` 替换为 `PERSONAL_ACCESS_TOKEN`

#### 方法 3: 检查分支保护规则

1. 进入仓库 Settings → Branches
2. 检查是否有分支保护规则阻止 Actions 推送
3. 如果有，添加例外规则允许 Actions 推送

### 验证修复

修复后，重新运行 Action：

1. 进入 "Actions" 标签页
2. 选择 "Update Star Rank" 工作流
3. 点击 "Re-run all jobs"
4. 查看运行日志，确认没有权限错误

## 其他常见问题

### Action 运行但页面没有更新

1. 检查 Action 日志中的 "Check generated files" 步骤
2. 确认 `index.html` 文件被正确生成
3. 检查文件大小是否大于 0 字节
4. 查看文件内容是否包含仓库数据

### 页面显示"暂无数据"

1. 确认 `repos.txt` 文件格式正确
2. 检查仓库名称是否存在拼写错误
3. 查看 Action 日志中的错误信息
4. 手动触发 "Test Star Rank" 工作流进行调试

### GitHub Pages 无法访问

1. 确认 Pages 功能已启用
2. 检查分支和文件夹设置
3. 等待几分钟让 Pages 生效
4. 清除浏览器缓存后重试

## 调试技巧

### 查看详细日志

在 Action 运行日志中，重点关注：

- "Run ranking script" 步骤的输出
- "Check generated files" 步骤的结果
- 任何错误或警告信息

### 本地测试

在本地运行脚本进行测试：

```bash
# 安装依赖
pip install requests beautifulsoup4

# 运行脚本
python scripts/update_rank.py

# 检查生成的文件
ls -la index.html
head -20 index.html
```

### 检查文件格式

确保 `repos.txt` 文件格式正确：

```txt
# 注释行
owner/repo-name
  tag1
  tag2
  tag3
```

- 仓库名称不能有缩进
- 标签必须有缩进（空格或制表符）
- 空行会被忽略
