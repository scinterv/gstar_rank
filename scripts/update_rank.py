#!/usr/bin/env python3
"""
Github Star Rank 更新脚本
从 repos.txt 读取仓库列表，获取 Star 数据并生成排名页面
"""

import os
import re
import json
import time
import requests
from datetime import datetime
from typing import List, Dict, Any

# GitHub API 配置
GITHUB_API_BASE = "https://api.github.com"
REPOS_FILE = "repos.txt"
OUTPUT_FILE = "index.html"

class RepoInfo:
    def __init__(self, owner: str, repo: str, tags: List[str] = None):
        self.owner = owner
        self.repo = repo
        self.tags = tags or []
        self.stars = 0
        self.description = ""
        self.html_url = ""
        self.updated_at = ""

def read_repos_file() -> List[RepoInfo]:
    """读取 repos.txt 文件，解析仓库和标签信息"""
    repos = []
    
    if not os.path.exists(REPOS_FILE):
        print(f"警告: {REPOS_FILE} 文件不存在")
        return repos
    
    with open(REPOS_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_repo = None
    for line in lines:
        line = line.strip()
        
        # 跳过空行和注释
        if not line or line.startswith('#'):
            continue
            
        # 检查是否是仓库行 (格式: owner/repo)
        if '/' in line and not line.startswith(' '):
            # 保存上一个仓库
            if current_repo:
                repos.append(current_repo)
            
            # 解析新仓库
            parts = line.split('/')
            if len(parts) == 2:
                current_repo = RepoInfo(parts[0].strip(), parts[1].strip())
            else:
                print(f"警告: 无效的仓库格式: {line}")
                current_repo = None
        else:
            # 标签行
            if current_repo and line:
                current_repo.tags.append(line)
    
    # 添加最后一个仓库
    if current_repo:
        repos.append(current_repo)
    
    return repos

def get_repo_info(owner: str, repo: str) -> Dict[str, Any]:
    """通过 GitHub API 获取仓库信息"""
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"错误: 获取 {owner}/{repo} 信息失败: {e}")
        return None

def update_repo_data(repos: List[RepoInfo]) -> List[RepoInfo]:
    """更新仓库的 Star 数据"""
    print(f"开始获取 {len(repos)} 个仓库的数据...")
    
    for i, repo in enumerate(repos):
        print(f"正在处理 {i+1}/{len(repos)}: {repo.owner}/{repo.repo}")
        
        data = get_repo_info(repo.owner, repo.repo)
        if data:
            repo.stars = data.get('stargazers_count', 0)
            repo.description = data.get('description', '')
            repo.html_url = data.get('html_url', '')
            repo.updated_at = data.get('updated_at', '')
        else:
            repo.stars = 0
            repo.description = "获取失败"
            repo.html_url = f"https://github.com/{repo.owner}/{repo.repo}"
        
        # 避免 API 限制
        time.sleep(0.1)
    
    return repos

def generate_html(repos: List[RepoInfo]) -> str:
    """生成 HTML 页面"""
    # 按 Star 数量排序
    sorted_repos = sorted(repos, key=lambda x: x.stars, reverse=True)
    
    # 获取所有标签
    all_tags = set()
    for repo in repos:
        all_tags.update(repo.tags)
    all_tags = sorted(list(all_tags))
    
    # 生成标签筛选器
    tag_filters = ""
    for tag in all_tags:
        tag_filters += f'<button class="tag-filter" data-tag="{tag}">{tag}</button>\n'
    
    # 生成仓库列表
    repo_items = ""
    for i, repo in enumerate(sorted_repos):
        tags_html = ""
        for tag in repo.tags:
            tags_html += f'<span class="tag">{tag}</span>\n'
        
        repo_items += f"""
        <div class="repo-item" data-tags="{','.join(repo.tags)}">
            <div class="rank">#{i+1}</div>
            <div class="repo-info">
                <h3><a href="{repo.html_url}" target="_blank">{repo.owner}/{repo.repo}</a></h3>
                <p class="description">{repo.description}</p>
                <div class="tags">{tags_html}</div>
            </div>
            <div class="stats">
                <div class="stars">⭐ {repo.stars:,}</div>
                <div class="updated">更新: {repo.updated_at[:10] if repo.updated_at else 'N/A'}</div>
            </div>
        </div>
        """
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Github Star Rank</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .filters {{
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .filters h3 {{
            margin-bottom: 15px;
            color: #495057;
        }}
        
        .tag-filters {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .tag-filter {{
            padding: 8px 16px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }}
        
        .tag-filter:hover {{
            background: #667eea;
            color: white;
        }}
        
        .tag-filter.active {{
            background: #667eea;
            color: white;
        }}
        
        .repo-list {{
            padding: 30px;
        }}
        
        .repo-item {{
            display: flex;
            align-items: center;
            padding: 25px;
            margin-bottom: 20px;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }}
        
        .repo-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        
        .rank {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
            margin-right: 25px;
            min-width: 60px;
        }}
        
        .repo-info {{
            flex: 1;
        }}
        
        .repo-info h3 {{
            margin-bottom: 8px;
        }}
        
        .repo-info h3 a {{
            color: #333;
            text-decoration: none;
            font-size: 1.3em;
        }}
        
        .repo-info h3 a:hover {{
            color: #667eea;
        }}
        
        .description {{
            color: #666;
            margin-bottom: 10px;
            line-height: 1.5;
        }}
        
        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }}
        
        .tag {{
            background: #e3f2fd;
            color: #1976d2;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        
        .stats {{
            text-align: right;
            min-width: 120px;
        }}
        
        .stars {{
            font-size: 1.2em;
            font-weight: bold;
            color: #ff6b35;
            margin-bottom: 5px;
        }}
        
        .updated {{
            font-size: 0.9em;
            color: #999;
        }}
        
        .no-results {{
            text-align: center;
            padding: 60px;
            color: #666;
            font-size: 1.2em;
        }}
        
        .last-updated {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
            background: #f8f9fa;
        }}
        
        @media (max-width: 768px) {{
            .repo-item {{
                flex-direction: column;
                text-align: center;
            }}
            
            .rank {{
                margin-right: 0;
                margin-bottom: 15px;
            }}
            
            .stats {{
                text-align: center;
                margin-top: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⭐ Github Star Rank</h1>
            <p>基于 Star 数量的 GitHub 仓库排名</p>
        </div>
        
        <div class="filters">
            <h3>按标签筛选</h3>
            <div class="tag-filters">
                <button class="tag-filter active" data-tag="all">全部</button>
                {tag_filters}
            </div>
        </div>
        
        <div class="repo-list" id="repo-list">
            {repo_items}
        </div>
        
        <div class="last-updated">
            最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>

    <script>
        // 标签筛选功能
        document.querySelectorAll('.tag-filter').forEach(button => {{
            button.addEventListener('click', function() {{
                // 更新按钮状态
                document.querySelectorAll('.tag-filter').forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                const selectedTag = this.getAttribute('data-tag');
                const repoItems = document.querySelectorAll('.repo-item');
                
                repoItems.forEach(item => {{
                    const tags = item.getAttribute('data-tags').split(',');
                    if (selectedTag === 'all' || tags.includes(selectedTag)) {{
                        item.style.display = 'flex';
                    }} else {{
                        item.style.display = 'none';
                    }}
                }});
                
                // 检查是否有结果
                const visibleItems = Array.from(repoItems).filter(item => item.style.display !== 'none');
                const noResults = document.getElementById('no-results');
                if (visibleItems.length === 0) {{
                    if (!noResults) {{
                        const noResultsDiv = document.createElement('div');
                        noResultsDiv.id = 'no-results';
                        noResultsDiv.className = 'no-results';
                        noResultsDiv.textContent = '没有找到匹配的仓库';
                        document.getElementById('repo-list').appendChild(noResultsDiv);
                    }}
                }} else {{
                    if (noResults) {{
                        noResults.remove();
                    }}
                }}
            }});
        }});
    </script>
</body>
</html>"""
    
    return html_content

def main():
    """主函数"""
    print("开始更新 Github Star Rank...")
    
    # 读取仓库配置
    repos = read_repos_file()
    if not repos:
        print("没有找到任何仓库配置")
        return
    
    print(f"找到 {len(repos)} 个仓库")
    
    # 更新仓库数据
    repos = update_repo_data(repos)
    
    # 生成 HTML
    html_content = generate_html(repos)
    
    # 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"排名页面已生成: {OUTPUT_FILE}")
    print("更新完成!")

if __name__ == "__main__":
    main()
